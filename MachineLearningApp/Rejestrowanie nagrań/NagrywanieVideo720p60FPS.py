import cv2
import os
import time
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# Path for exported data, numpy arrays
DATA_PATH = os.path.join('MP_Data')


def initialize_camera():
    # Use DSHOW backend for faster camera initialization on Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        raise RuntimeError("Error: Could not open video capture")

    # Setup camera properties
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("Actual FPS:", actual_fps)

    return cap, actual_fps


def put_text_with_polish_characters(image, text, position, font_path='arial.ttf', font_size=32, color=(0, 0, 255)):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return image


def countdown_timer(cap, seconds, message):
    start_time = time.time()
    while time.time() - start_time < seconds:
        ret, frame = cap.read()
        if not ret:
            break
        frame = put_text_with_polish_characters(frame, f"{message} {int(seconds - (time.time() - start_time))}",
                                                (50, 50))
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def record_gesture_video(gesture_name, num_videos, video_length_seconds, cap, actual_fps):
    gesture_path = os.path.join(DATA_PATH, gesture_name)
    try:
        os.makedirs(gesture_path)
    except FileExistsError:
        pass

    existing_files = [f for f in os.listdir(gesture_path) if f.endswith('.avi')]
    highest_sequence = max([int(f.split('.')[0]) for f in existing_files], default=-1)
    sequence_start = highest_sequence + 1

    cv2.namedWindow('Recording', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Recording', cv2.WND_PROP_TOPMOST, 1)

    for sequence in range(sequence_start, sequence_start + num_videos):
        if sequence == sequence_start:
            message = "Przyjmij pierwszą pozycję wyjściową."
            countdown_timer(cap, 15, message)
        if sequence % 25 == 0 and sequence != sequence_start:
            message = "Przygotuj się do kolejnego gestu."
            countdown_timer(cap, 1, message)

        out = cv2.VideoWriter()
        video_filename = os.path.join(gesture_path, f"{sequence}.avi")
        out.open(video_filename, cv2.VideoWriter_fourcc(*'MJPG'), 60, (1280, 720))

        frames = []
        target_frame_count = video_length_seconds * 30  # 4 seconds * 30 FPS = 120 frames
        frame_count = 0

        while frame_count < target_frame_count:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame")
                break

            if frame_count < 60:  # 2 sekundy to 60 klatek przy 30 FPS
                frame = put_text_with_polish_characters(frame,
                                                        f"ROZPOCZYNAM NAGRYWANIE {gesture_name} Video {sequence + 1 - sequence_start}/{num_videos}",
                                                        (50, 50), font_size=24, color=(0, 255, 0))

            cv2.imshow('Recording', frame)
            frames.append(frame)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Powielanie każdej klatki, aby uzyskać 60 FPS
        for frame in frames:
            out.write(frame)
            out.write(frame)

        out.release()

        # 1-sekundowa przerwa z komunikatem
        message = "Przygotuj się na kolejny gest..."
        countdown_timer(cap, 1, message)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    gesture_name = 'Dzięki'
    num_videos = 100
    video_length_seconds = 4

    cap, actual_fps = initialize_camera()
    record_gesture_video(gesture_name, num_videos, video_length_seconds, cap, actual_fps)
