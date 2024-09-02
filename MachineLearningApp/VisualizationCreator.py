import cv2
import numpy as np
import mediapipe as mp
from tkinter import filedialog, Tk, Label, Button, StringVar, ttk
import os
import threading
import queue

# Inicjalizacja MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

def process_frame(frame, pose, hands, face_mesh):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_results = pose.process(frame_rgb)
    hands_results = hands.process(frame_rgb)
    face_results = face_mesh.process(frame_rgb)

    frame_with_landmarks = frame.copy()
    frame_skeleton = np.zeros_like(frame)

    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame_with_landmarks, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(frame_skeleton, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if hands_results.multi_hand_landmarks:
        for hand_landmarks in hands_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_with_landmarks, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(frame_skeleton, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame_with_landmarks, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)
            mp_drawing.draw_landmarks(frame_skeleton, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

    return frame_with_landmarks, frame_skeleton

def create_visualization(video_path, output_video_path, output_images_path, progress_queue):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Nie można otworzyć pliku wideo.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width * 3, frame_height))

    second_intervals = [int(fps * i) for i in range(5)]  # Klatki odpowiadające zerowej, pierwszej, drugiej, trzeciej i czwartej sekundzie
    images_saved = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
            mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
            mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_with_landmarks, frame_skeleton = process_frame(frame, pose, hands, face_mesh)
            combined_frame = np.hstack((frame, frame_with_landmarks, frame_skeleton))
            out_video.write(combined_frame)

            # Zapisz obrazek co sekundę (w tym zerowa sekunda)
            if frame_count in second_intervals:
                image_path = os.path.join(output_images_path, f"frame_{images_saved}.png")
                cv2.imwrite(image_path, combined_frame)
                images_saved += 1

            # Aktualizacja paska postępu przez dodanie komunikatu do kolejki
            progress_queue.put((frame_count, total_frames))

            frame_count += 1
            if images_saved >= 5:  # Zatrzymaj zapis obrazków po zapisaniu pięciu
                break

    cap.release()
    out_video.release()

    # Wysłanie sygnału zakończenia
    progress_queue.put("DONE")

def update_progress(root, progress_var, progress_label, progress_queue):
    try:
        while True:
            msg = progress_queue.get_nowait()
            if msg == "DONE":
                progress_var.set(100)
                progress_label.set("Przetwarzanie zakończone")
                Button(root, text="Zakończ", command=root.quit).pack(pady=10)
                return
            else:
                frame_count, total_frames = msg
                progress_var.set((frame_count / total_frames) * 100)
                progress_label.set(f"Przetwarzanie: {frame_count}/{total_frames} klatek")
    except queue.Empty:
        root.after(100, update_progress, root, progress_var, progress_label, progress_queue)

def run_visualization(video_path, output_video_path, output_images_path, progress_var, progress_label, progress_queue):
    threading.Thread(target=create_visualization, args=(video_path, output_video_path, output_images_path, progress_queue)).start()

def main():
    # Ukrywanie pustego okna Tkinter
    root = Tk()
    root.withdraw()

    video_path = filedialog.askopenfilename(title="Wybierz plik wideo", filetypes=[("Pliki wideo", "*.mp4;*.avi")])
    if not video_path:
        print("Nie wybrano pliku.")
        return

    root.deiconify()  # Odtwórz okno po wybraniu pliku
    output_video_path = "visualization.mp4"
    output_images_path = "output_images"

    # Upewnij się, że katalog na obrazki istnieje
    if not os.path.exists(output_images_path):
        os.makedirs(output_images_path)

    # Tworzenie okna z paskiem postępu
    root.title("Przetwarzanie wideo")
    root.geometry("400x150")

    progress_var = StringVar()
    progress_var.set(0)

    progress_label = StringVar()
    progress_label.set("Rozpoczęcie przetwarzania")

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)
    progress_bar.pack(pady=20)

    label = Label(root, textvariable=progress_label)
    label.pack(pady=10)

    # Kolejka do komunikacji między wątkami
    progress_queue = queue.Queue()

    threading.Thread(target=run_visualization, args=(video_path, output_video_path, output_images_path, progress_var, progress_label, progress_queue)).start()

    # Aktualizacja paska postępu
    root.after(100, update_progress, root, progress_var, progress_label, progress_queue)

    root.mainloop()

if __name__ == "__main__":
    main()
