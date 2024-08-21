import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os
from tkinter import Tk, filedialog, Toplevel, Button, Label, IntVar
from tkinter.ttk import Progressbar

# Wczytaj model i etykiety z nowych lokalizacji
model = load_model('../../scripts/python/best_model.h5')
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('../../scripts/python/classes.npy')

# Ustawienia Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh


# Funkcje pomocnicze
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
                padded_sequences[i, j, :len(frame)] = frame
    return padded_sequences


def pad_keypoints(keypoints, num_features):
    if len(keypoints) < num_features:
        keypoints.extend([0] * (num_features - len(keypoints)))
    return keypoints


def predict_gesture_from_video(video_path, progress_var, progress_window, video_paths, buffer_size=240,
                               num_features=1725):
    cap = cv2.VideoCapture(video_path)
    frame_buffer = []
    all_predictions = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
            mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
            mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(frame_rgb)
            hands_results = hands.process(frame_rgb)
            face_results = face_mesh.process(frame_rgb)

            keypoints = extract_keypoints(pose_results, hands_results, face_results)
            keypoints = pad_keypoints(keypoints, num_features)

            if keypoints:
                frame_buffer.append(keypoints)
                if len(frame_buffer) > buffer_size:
                    frame_buffer.pop(0)

        cap.release()

        if len(frame_buffer) == buffer_size:
            keypoints_array = pad_sequences([frame_buffer], maxlen=buffer_size, num_features=num_features)
            keypoints_array = keypoints_array.reshape(1, buffer_size, num_features)

            prediction = model.predict(keypoints_array)
            all_predictions.append(prediction[0])

            # Zaktualizuj pasek postępu i okno
            progress_var.set(progress_var.get() + int(100 / len(video_paths)))
            progress_window.update()

    return np.array(all_predictions)


def plot_gesture_predictions(predictions, file_names, progress_var):
    if len(predictions) == 0:
        print("No predictions were made.")
        return

    save_path = filedialog.askdirectory(title="Wybierz miejsce do zapisu wykresów")
    if not save_path:
        return

    overall_avg_predictions = np.zeros_like(predictions[0])

    for i, (prediction, file_name) in enumerate(zip(predictions, file_names)):
        avg_predictions = prediction
        sorted_indices = np.argsort(avg_predictions[0])[::-1]
        sorted_gestures = [(label_encoder.classes_[i], avg_predictions[0][i] * 100) for i in sorted_indices]

        # Pobierz nazwę gestu z nazwy katalogu
        gesture_name = os.path.basename(os.path.dirname(file_name))

        # Utwórz katalog o nazwie gestu, jeśli nie istnieje
        gesture_save_path = os.path.join(save_path, gesture_name)
        os.makedirs(gesture_save_path, exist_ok=True)

        most_likely_gesture = label_encoder.classes_[sorted_indices[0]]
        max_probability = avg_predictions[0][sorted_indices[0]] * 100

        plt.figure(figsize=(12, 10))  # Zwiększona wysokość grafiki
        bars = plt.bar(label_encoder.classes_, avg_predictions[0] * 100, color='#32A7E2')
        plt.ylabel('Pewność predykcji (%)')
        plt.xlabel('')
        plt.xticks(rotation=45, ha="right")
        plt.title(f'Testowany gest: {gesture_name} (Próbka nr {i + 1})')

        # Dodanie tekstu na słupki wykresu
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        # Dodanie tekstu na dole wykresu
        plt.figtext(0.5, 0.01, f"Wykryto gest: {most_likely_gesture} z pewnością {max_probability:.2f}%",
                    ha="center", fontsize=12, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5})

        # Przeniesienie etykiety "Gesty" do prawego dolnego rogu
        plt.annotate('Gesty', xy=(1, 0), xycoords='axes fraction', fontsize=14,
                     ha='right', va='bottom')

        plt.tight_layout()
        plt.savefig(
            os.path.join(gesture_save_path, f'plot_{gesture_name}_{i + 1}.png'))  # Zapisz wykres w katalogu gestu
        plt.close()

        overall_avg_predictions += avg_predictions

    overall_avg_predictions /= len(predictions)

    # Podsumowanie dla wszystkich plików
    gesture_name_summary = os.path.basename(os.path.dirname(file_names[0]))  # Pobranie nazwy gestu z pierwszego pliku
    plt.figure(figsize=(12, 10))  # Zwiększona wysokość grafiki
    colors = ['#B548C6' if i == np.argmax(overall_avg_predictions[0]) else '#32A7E2' for i in
              range(len(overall_avg_predictions[0]))]
    bars = plt.bar(label_encoder.classes_, overall_avg_predictions[0] * 100, color=colors)
    plt.ylabel('Średnia pewność predykcji (%)')
    plt.xticks(rotation=45, ha="right")
    plt.title(f'Podsumowanie predykcji dla wszystkich plików gestu {gesture_name_summary}')

    # Dodanie tekstu na słupki wykresu
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

    # Dodanie tekstu na dole wykresu
    plt.figtext(0.5, 0.01,
                f"Wykryto gest: {label_encoder.classes_[np.argmax(overall_avg_predictions)]} z pewnością {np.max(overall_avg_predictions[0]) * 100:.2f}%",
                ha="center", fontsize=12, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5})

    # Przeniesienie etykiety "Gesty" do prawego dolnego rogu
    plt.annotate('Gesty', xy=(1, 0), xycoords='axes fraction', fontsize=14,
                 ha='right', va='bottom')

    # Zapis wykresu podsumowującego w katalogu gestu
    plt.tight_layout()
    plt.savefig(os.path.join(gesture_save_path, 'summary_plot.png'))
    plt.close()

    print("Wykresy zapisane.")
    progress_var.set(100)


def create_progress_window():
    progress_window = Toplevel()
    progress_window.title("Przetwarzanie")

    progress_var = IntVar()
    progress_bar = Progressbar(progress_window, variable=progress_var, maximum=100, length=400)
    progress_bar.pack(pady=20)

    progress_label = Label(progress_window, text="Przetwarzanie w toku...")
    progress_label.pack()

    close_button = Button(progress_window, text="Zamknij", command=lambda: os._exit(0))
    close_button.pack(side='right', padx=20, pady=20)

    return progress_var, progress_window


def main():
    try:
        print("Starting the file selection process...")
        root = Tk()
        root.withdraw()  # Ukryj główne okno Tkintera
        video_paths = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")],
            multiple=True
        )
        print("Files selected:", video_paths)
        if not video_paths:
            print("No files selected.")
            return

        progress_var, progress_window = create_progress_window()
        progress_window.update()

        predictions = []
        for video_path in video_paths:
            prediction = predict_gesture_from_video(video_path, progress_var, progress_window, video_paths)
            if prediction.size > 0:
                predictions.append(prediction)

        plot_gesture_predictions(predictions, video_paths, progress_var)

        progress_label = Label(progress_window, text="Przetwarzanie zakończone!")
        progress_label.pack(pady=10)

        progress_window.mainloop()

        print("Processing complete.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    print("Program started.")
    main()
