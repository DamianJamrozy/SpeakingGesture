import os
import cv2
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import ttk
import threading
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from multiprocessing import Pool, Manager, cpu_count
from PIL import Image, ImageTk
import warnings
import random
import time

# Inicjalizacja MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

# Ignorowanie ostrzeżeń dotyczących SymbolDatabase.GetPrototype()
warnings.filterwarnings("ignore", category=UserWarning, message="SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead.")

def extract_keypoints(pose_results, hands_results, face_results):
    keypoints = []

    if pose_results.pose_landmarks:
        for res in pose_results.pose_landmarks.landmark:
            keypoints.extend([res.x, res.y, res.z, res.visibility])

    if hands_results.multi_hand_landmarks:
        for hand_landmarks in hands_results.multi_hand_landmarks:
            for res in hand_landmarks.landmark:
                keypoints.extend([res.x, res.y, res.z])

    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            for res in face_landmarks.landmark:
                keypoints.extend([res.x, res.y, res.z])

    return keypoints

def pad_sequences(sequences, maxlen, num_features):
    padded_sequences = np.zeros((len(sequences), maxlen, num_features))
    for i, seq in enumerate(sequences):
        for j, frame in enumerate(seq):
            if j < maxlen:
                if len(frame) < num_features:
                    frame.extend([0] * (num_features - len(frame)))
                padded_sequences[i, j, :] = frame
    return padded_sequences

def process_video(args):
    video_path, gesture, data, labels, current_progress, total_videos, lock, queue = args
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        queue.put(f"Nie można otworzyć pliku: {video_path}")
        return

    frames = []
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
         mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
         mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(frame_rgb)
            hands_results = hands.process(frame_rgb)
            face_results = face_mesh.process(frame_rgb)
            keypoints = extract_keypoints(pose_results, hands_results, face_results)
            frames.append(keypoints)

    cap.release()
    if len(frames) == 240:
        with lock:
            data.append(frames)
            labels.append(gesture)
            current_progress.value += 1
            progress = (current_progress.value / total_videos) * 100
            queue.put(f"{video_path} - Przetworzono, Postęp: {progress:.2f}%")
    else:
        queue.put(f"{video_path} - Niepełne nagranie, pominięto")

def preprocess_videos_with_progress(data_path='MP_Data'):
    manager = Manager()
    data = manager.list()
    labels = manager.list()
    current_progress = manager.Value('i', 0)
    lock = manager.Lock()
    video_files = []
    queue = manager.Queue()

    for gesture in os.listdir(data_path):
        gesture_path = os.path.join(data_path, gesture)
        if os.path.isdir(gesture_path):
            for video_file in os.listdir(gesture_path):
                video_path = os.path.join(gesture_path, video_file)
                if video_file.endswith('.avi'):
                    video_files.append((video_path, gesture))

    total_videos = len(video_files)
    if total_videos == 0:
        print("Brak nagrań do przetworzenia.")
        return

    def display_visualization():
        vis_root = tk.Toplevel()
        vis_root.title("Wizualizacja przetwarzania")
        vis_root.geometry("800x400")  # Zwiększono wysokość okna
        vis_root.attributes('-topmost', True)

        header_text = tk.Label(vis_root, text="", anchor="n")
        header_text.pack(side=tk.TOP, pady=5)

        vis_frame = tk.Frame(vis_root)
        vis_frame.pack(fill='both', expand=True)

        vis_label_left = tk.Label(vis_frame)
        vis_label_left.pack(side=tk.LEFT, fill='both', expand=True)

        vis_label_right = tk.Label(vis_frame)
        vis_label_right.pack(side=tk.RIGHT, fill='both', expand=True)

        footer_text = tk.Label(vis_root, text="Autor: Damian Jamroży", anchor="se")
        footer_text.pack(side=tk.BOTTOM, pady=5)

        random_video_path, gesture = random.choice([(vf[0], vf[1]) for vf in video_files])
        cap = cv2.VideoCapture(random_video_path)

        header_text.config(text=f"Wizualizacja gestu {gesture}, nagranie nr {os.path.basename(random_video_path)}")

        def update_visualization():
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
                 mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
                 mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_left = frame.copy()

                    pose_results = pose.process(frame_rgb)
                    hands_results = hands.process(frame_rgb)
                    face_results = face_mesh.process(frame_rgb)

                    if pose_results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame_left, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    if hands_results.multi_hand_landmarks:
                        for hand_landmarks in hands_results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame_left, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    if face_results.multi_face_landmarks:
                        for face_landmarks in face_results.multi_face_landmarks:
                            mp_drawing.draw_landmarks(frame_left, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

                    frame_right = np.zeros_like(frame_left)
                    if pose_results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame_right, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    if hands_results.multi_hand_landmarks:
                        for hand_landmarks in hands_results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame_right, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    if face_results.multi_face_landmarks:
                        for face_landmarks in face_results.multi_face_landmarks:
                            mp_drawing.draw_landmarks(frame_right, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

                    img_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)
                    img_left = cv2.resize(img_left, (400, 300))  # Zmniejszenie podglądu 2x
                    img_left = ImageTk.PhotoImage(image=Image.fromarray(img_left))
                    vis_label_left.config(image=img_left)
                    vis_label_left.image = img_left

                    img_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
                    img_right = cv2.resize(img_right, (400, 300))  # Zmniejszenie podglądu 2x
                    img_right = ImageTk.PhotoImage(image=Image.fromarray(img_right))
                    vis_label_right.config(image=img_right)
                    vis_label_right.image = img_right

                    vis_root.update_idletasks()
                    time.sleep(1/30)  # Odtwarzanie wideo w 30 FPS
                cap.release()

        threading.Thread(target=update_visualization).start()

    root, main_progress, progress_text, details_text, button_frame, footer_label = create_progress_bar(total_videos, "Autor: Damian Jamroży", display_visualization)

    def update_progress():
        while True:
            result = queue.get()
            if result == "DONE":
                break
            if result:
                details_text.config(state='normal')
                details_text.insert('end', f"{result}\n")
                details_text.yview('end')
                details_text.config(state='disabled')
                progress_text.set(f"Przetworzono {current_progress.value}/{total_videos} nagrań ({(current_progress.value / total_videos) * 100:.2f}%)")
                root.update_idletasks()
            progress = (current_progress.value / total_videos) * 100
            main_progress['value'] = current_progress.value
            progress_text.set(f"Przetworzono {current_progress.value}/{total_videos} nagrań ({progress:.2f}%)")
            root.update_idletasks()

    def process_videos():
        pool_args = [(video_path, gesture, data, labels, current_progress, total_videos, lock, queue) for video_path, gesture in video_files]
        with Pool(min(cpu_count(), 25)) as pool:  # Użyj maksymalnie 25 procesów
            pool.map(process_video, pool_args)

        queue.put("DONE")

        if len(data) > 0:
            num_features = max(len(frame) for seq in data for frame in seq)
            data_array = pad_sequences(list(data), maxlen=240, num_features=num_features)
            save_preprocessed_data(data_array, np.array(labels))
            print(f"Przetworzono {len(data)} nagrań.")
        else:
            print("Brak przetworzonych nagrań.")

        finish_label = tk.Label(root, text="Zakończono przetwarzanie danych")
        finish_label.pack(pady=10)

        start_training_button = tk.Button(button_frame, text="Rozpocznij uczenie maszynowe", command=lambda: start_training(data_array, np.array(labels), root))
        start_training_button.pack(side=tk.RIGHT, padx=5)

        close_button = tk.Button(button_frame, text="Zakończ", command=root.quit)
        close_button.pack(side=tk.LEFT, padx=5)

    threading.Thread(target=update_progress).start()
    threading.Thread(target=process_videos).start()
    root.mainloop()

def save_preprocessed_data(data, labels, filename='preprocessed_data.npz'):
    np.savez_compressed(filename, data=data, labels=labels)
    print(f"Dane zapisane do pliku: {filename}")

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f'{width}x{height}+{x}+{y}')

def create_progress_bar(total, footer_text, display_visualization):
    root = tk.Tk()
    root.title("Progres Przetwarzania")
    width, height = 600, 200
    center_window(root, width, height)
    root.attributes('-topmost', True)

    main_progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", maximum=total)
    main_progress.pack(pady=20)

    details_frame = tk.Frame(root)
    details_frame.pack(fill='both', expand=True)
    details_frame.pack_forget()

    details_text = tk.Text(details_frame, wrap='word', height=10, state='disabled')
    details_text.pack(fill='both', expand=True)

    details_button = tk.Button(root, text="Pokaż szczegóły", command=lambda: toggle_details(details_frame, details_button, vis_button, width, height))
    details_button.pack(pady=10)

    vis_button = tk.Button(root, text="Wyświetl wizualizację", command=display_visualization)

    progress_text = tk.StringVar()
    progress_text.set("Trwa weryfikacja plików...")  # Dodanie domyślnego napisu
    progress_label = tk.Label(root, textvariable=progress_text)
    progress_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    footer_label = tk.Label(root, text=footer_text)
    footer_label.pack(side=tk.BOTTOM, pady=5)

    root.update_idletasks()

    def toggle_details(frame, button, vis_button, width, height):
        if frame.winfo_ismapped():
            frame.pack_forget()
            vis_button.pack_forget()
            root.geometry(f'{width}x{height}')
            button.config(text="Pokaż szczegóły")
        else:
            frame.pack(fill='both', expand=True)
            vis_button.pack(pady=10)
            vis_button.pack()
            root.geometry(f'{width}x{450}')
            button.config(text="Ukryj szczegóły")

    return root, main_progress, progress_text, details_text, button_frame, footer_label

def create_training_progress_bar(total):
    root = tk.Tk()
    root.title("Progres Uczenia Maszynowego")
    width, height = 600, 300
    center_window(root, width, height)
    root.attributes('-topmost', True)

    main_progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", maximum=total)
    main_progress.pack(pady=20)

    details_frame = tk.Frame(root)
    details_frame.pack(fill='both', expand=True)
    details_frame.pack_forget()

    details_text = tk.Text(details_frame, wrap='word', height=10, state='disabled')
    details_text.pack(fill='both', expand=True)

    details_button = tk.Button(root, text="Pokaż szczegóły", command=lambda: toggle_details(details_frame, details_button, width, height))
    details_button.pack(pady=10)

    progress_text = tk.StringVar()
    progress_label = tk.Label(root, textvariable=progress_text)
    progress_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    finish_label = tk.Label(root, text="Proces uczenia maszynowego zakończony")
    finish_label.pack()
    finish_label.pack_forget()  # Ukryj na początku

    close_button = tk.Button(root, text="Zakończ", command=root.quit)
    close_button.pack()
    close_button.pack_forget()  # Ukryj na początku

    footer_label = tk.Label(root, text="Autor: Damian Jamroży")
    footer_label.pack(side=tk.BOTTOM, pady=10)

    root.update_idletasks()

    def toggle_details(frame, button, width, height):
        if frame.winfo_ismapped():
            frame.pack_forget()
            root.geometry(f'{width}x{height}')
            button.config(text="Pokaż szczegóły")
        else:
            frame.pack(fill='both', expand=True)
            root.geometry(f'{width}x{550}')
            button.config(text="Ukryj szczegóły")

    return root, main_progress, progress_text, details_text, button_frame, footer_label, finish_label, close_button

def train_model(data, labels):
    total_epochs = 150

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

    # Zapisz klasy do pliku classes.npy
    np.save('classes.npy', label_encoder.classes_)

    num_samples, num_timesteps, num_features = data.shape
    data = data.reshape((num_samples, num_timesteps, num_features))

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(num_timesteps, num_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(np.unique(labels)), activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=20, restore_best_weights=True)

    root, main_progress, progress_text, details_text, button_frame, footer_label, finish_label, close_button = create_training_progress_bar(total_epochs)

    root.update_idletasks()

    def on_epoch_end(epoch, logs):
        main_progress['value'] = epoch + 1
        progress_text.set(f"Przetworzono {epoch + 1}/{total_epochs} epok")
        details_text.config(state='normal')
        details_text.insert('end', f"Epoka {epoch + 1} - Strata: {logs['loss']:.4f}, Dokładność: {logs['accuracy']:.4f}, Walidacja Strata: {logs['val_loss']:.4f}, Walidacja Dokładność: {logs['val_accuracy']:.4f}\n")
        details_text.yview('end')
        details_text.config(state='disabled')
        root.update_idletasks()

    def train_model_thread():
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=total_epochs, batch_size=32,
                  callbacks=[checkpoint, early_stopping, tf.keras.callbacks.LambdaCallback(on_epoch_end=on_epoch_end)])
        finish_label.pack()  # Pokaż po zakończeniu
        close_button.pack(pady=5)  # Pokaż po zakończeniu
        root.update_idletasks()

    threading.Thread(target=train_model_thread).start()
    root.mainloop()

def start_training(data, labels, existing_root):
    if existing_root:
        existing_root.destroy()
    threading.Thread(target=lambda: train_model(data, labels)).start()

def main():
    data_path = 'MP_Data'
    preprocessed_file = 'preprocessed_data.npz'

    if not os.path.exists(preprocessed_file):
        preprocess_videos_with_progress(data_path)

    if os.path.exists(preprocessed_file):
        npzfile = np.load(preprocessed_file)
        data = npzfile['data']
        labels = npzfile['labels']
        print(f"Wczytano dane: {data.shape}, etykiety: {labels.shape}")
    else:
        print("Błąd: Plik przetworzonych danych nie został utworzony.")
        return

    if len(data) > 0 and len(labels) > 0:
        print("Rozpoczynanie trenowania modelu...")
        start_training(data, labels, None)
    else:
        print("Brak danych do trenowania modelu.")

if __name__ == "__main__":
    main()
