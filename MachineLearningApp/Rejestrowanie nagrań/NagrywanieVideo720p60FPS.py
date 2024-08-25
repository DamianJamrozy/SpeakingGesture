import cv2
import os
import time

# Path for exported data, numpy arrays
DATA_PATH = os.path.join('MP_Data')

def countdown_timer(cap, seconds, message):
    start_time = time.time()
    while time.time() - start_time < seconds:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, f"{message} {int(seconds - (time.time() - start_time))}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def record_gesture_video(gesture_name, num_videos, video_length_seconds):
    cap = cv2.VideoCapture(0)

    # Setup camera properties
    desired_fps = 60
    cap.set(cv2.CAP_PROP_FPS, desired_fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("Actual FPS:", actual_fps)

    video_length = actual_fps * video_length_seconds

    # Create directories if not exist
    gesture_path = os.path.join(DATA_PATH, gesture_name)
    try:
        os.makedirs(gesture_path)
    except FileExistsError:
        pass

    # Find the next available sequence number
    existing_files = [f for f in os.listdir(gesture_path) if f.endswith('.avi')]
    highest_sequence = max([int(f.split('.')[0]) for f in existing_files], default=-1)
    sequence_start = highest_sequence + 1

    # Create a named window and set it to be always on top
    cv2.namedWindow('Recording', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Recording', cv2.WND_PROP_TOPMOST, 1)

    for sequence in range(sequence_start, sequence_start + num_videos):
        if sequence == sequence_start:
            message = "Przyjmij pierwszą pozycję wyjściową."
            countdown_timer(cap, 15, message)
        if sequence == sequence_start + 25 or sequence == sequence_start + 75:
            message = "Przyjmij drugą pozycję wyjściową." if sequence == sequence_start + 25 else "Przyjmij ostatnią pozycję wyjściową."
            countdown_timer(cap, 20, message)

        out = cv2.VideoWriter()
        video_filename = os.path.join(gesture_path, f"{sequence}.avi")
        out.open(video_filename, cv2.VideoWriter_fourcc(*'MJPG'), actual_fps, (1280, 720))

        start_time = time.time()
        for frame_num in range(video_length):
            ret, frame = cap.read()

            if frame_num == 0:
                cv2.putText(frame, f"STARTING RECORDING {gesture_name} Video {sequence + 1 - sequence_start}/{num_videos}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Recording', frame)
                cv2.waitKey(2000)

            cv2.imshow('Recording', frame)
            out.write(frame)

            while time.time() - start_time < frame_num / actual_fps:
                time.sleep(0.001)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.release()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_name = 'Brak ruchu'
    num_videos = 100
    video_length_seconds = 4

    record_gesture_video(gesture_name, num_videos, video_length_seconds)