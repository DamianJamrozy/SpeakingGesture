import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from keras.models import load_model
from tkinter import Tk, Label, Frame, Button, BOTH, BOTTOM, LEFT, RIGHT
from PIL import Image, ImageTk, ImageDraw, ImageFont
from sklearn.preprocessing import LabelEncoder
from tkinter.ttk import Progressbar

# Wczytanie wyuczonego modelu
model = load_model('best_model.h5')

# Wczytanie etykiet
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('classes.npy')

# MediaPipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh


# Extract keypoints using MediaPipe
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


# Lista gestów
gestures = label_encoder.classes_

# Inicjalizacja kamery
cap = cv2.VideoCapture(0)

# Pobranie rozmiaru obrazu z kamery
ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape

# Inicjalizacja okna Tkinter
root = Tk()
root.title("Gesture Recognition")
root.geometry(f"{frame_width}x{frame_height + 60}")  # Dostosowanie rozmiaru okna do obrazu kamery
root.attributes('-topmost', True)

# Frame do obrazu z kamery i przycisku
main_frame = Frame(root)
main_frame.pack(side=LEFT)

# Label do wyświetlania obrazu
lbl = Label(main_frame)
lbl.pack()

# Frame na szczegóły
details_frame = Frame(root)


# Funkcja do aktualizacji listy podobnych gestów
def update_similar_gestures(predictions):
    for widget in details_frame.winfo_children():
        widget.destroy()

    for i, (gesture, probability) in enumerate(predictions):
        if i >= 10:
            break
        label_text = f"{gesture}: {probability:.2f}%"
        label = Label(details_frame, text=label_text, font=("Calibri", 12))
        label.pack()

        progress = Progressbar(details_frame, length=200, mode='determinate')
        progress['value'] = probability
        progress.pack()


# Funkcja do pokazania szczegółów
def show_details():
    root.geometry(f"{frame_width + 300}x{frame_height + 60}")  # Rozszerzenie okna po lewej stronie
    details_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    details_button.config(text="Ukryj szczegóły", command=hide_details)


# Funkcja do ukrycia szczegółów
def hide_details():
    details_frame.pack_forget()
    root.geometry(f"{frame_width}x{frame_height + 60}")  # Przywrócenie rozmiaru okna
    details_button.config(text="Pokaż szczegóły", command=show_details)


# Przycisk "Pokaż szczegóły"
details_button = Button(main_frame, text="Pokaż szczegóły", command=show_details)
details_button.pack(pady=5)

# Stopka z autorem
footer = Frame(root)
footer.pack(side=BOTTOM, fill=BOTH)
footer_label = Label(footer, text="Autor: Damian Jamroży", font=("Calibri", 12))
footer_label.pack()

# Lista do przechowywania ostatnich trzech wykrytych gestów
detected_gestures = []

# Bufor na kluczowe punkty z klatek
frame_buffer = []
buffer_size = 240  # Ustawienie rozmiaru bufora na 240 klatek (4 sekundy przy 60 fps)
prediction_interval = 10  # Przewidywanie co 10 klatek
frame_count = 0  # Licznik ramek

num_features = 1725  # Określenie liczby cech na podstawie liczby kluczowych punktów


def draw_text_with_pil(image, text, position, font_path="calibri.ttf", font_size=32, color=(0, 255, 0)):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def update_frame():
    global frame_count
    try:
        ret, frame = cap.read()
        if not ret:
            root.after(10, update_frame)
            return

        # Przetwarzanie obrazu
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(frame_rgb)
        hands_results = hands.process(frame_rgb)
        face_results = face_mesh.process(frame_rgb)

        keypoints = extract_keypoints(pose_results, hands_results, face_results)
        keypoints = pad_keypoints(keypoints, num_features)

        if keypoints:
            frame_buffer.append(keypoints)

            # Utrzymanie rozmiaru bufora na maksymalnie 240 klatek
            if len(frame_buffer) > buffer_size:
                frame_buffer.pop(0)

            # Przewidywanie gestu co 10 klatek
            if len(frame_buffer) == buffer_size and frame_count % prediction_interval == 0:
                keypoints_array = pad_sequences([frame_buffer], maxlen=buffer_size, num_features=num_features)
                keypoints_array = keypoints_array.reshape(1, buffer_size, num_features)

                # Przewidywanie gestu
                prediction = model.predict(keypoints_array)
                probabilities = prediction[0]
                sorted_indices = np.argsort(probabilities)[::-1]
                sorted_gestures = [(gestures[i], probabilities[i] * 100) for i in sorted_indices]

                # Dodaj wynik do listy wykrytych gestów tylko, jeśli prawdopodobieństwo jest większe niż próg
                if probabilities[sorted_indices[0]] > 0.6:  # Możesz dostosować próg według potrzeb
                    detected_gestures.append((gestures[sorted_indices[0]], probabilities[sorted_indices[0]] * 100))
                    if len(detected_gestures) > 3:
                        detected_gestures.pop(0)

                # Aktualizacja listy podobnych gestów
                update_similar_gestures(sorted_gestures)

        # Rysowanie kluczowych punktów na obrazie
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

        # Wyświetlanie ostatnich trzech wykrytych gestów na obrazie
        for i, (gesture, probability) in enumerate(detected_gestures):
            text = f"{gesture}: {probability:.2f}%"
            frame = draw_text_with_pil(frame, text, (10, 40 + i * 30))

        # Konwersja obrazu OpenCV do formatu Tkinter
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)

        frame_count += 1
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        root.after(10, update_frame)


# MediaPipe processing context
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
        mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
        mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    update_frame()
    root.mainloop()

cap.release()
