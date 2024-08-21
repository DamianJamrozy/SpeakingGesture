from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageDraw, ImageFont
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

model = load_model('scripts/python/best_model.h5')
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('scripts/python/classes.npy')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)

buffer_size = 240
prediction_interval = 10
frame_count = 0
num_features = 1725
frame_buffer = []
detected_gestures = []
sorted_gestures = []  # Globalna zmienna do przechowywania posortowanych gestów

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

def draw_text_with_pil(image, text, position, font_path="scripts/python/calibri.ttf", font_size=20, color=(0, 255, 0)):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def gen_frames():
    global frame_count, sorted_gestures
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

                if len(frame_buffer) == buffer_size and frame_count % prediction_interval == 0:
                    keypoints_array = pad_sequences([frame_buffer], maxlen=buffer_size, num_features=num_features)
                    keypoints_array = keypoints_array.reshape(1, buffer_size, num_features)

                    prediction = model.predict(keypoints_array)
                    probabilities = prediction[0]
                    sorted_indices = np.argsort(probabilities)[::-1]
                    sorted_gestures = [(label_encoder.classes_[i], probabilities[i] * 100) for i in sorted_indices[:5]]

                    if probabilities[sorted_indices[0]] > 0.6:
                        detected_gestures.append((label_encoder.classes_[sorted_indices[0]], probabilities[sorted_indices[0]] * 100))
                        if len(detected_gestures) > 3:
                            detected_gestures.pop(0)

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

            for i, (gesture, probability) in enumerate(detected_gestures):
                text = f"{gesture}: {probability:.2f}%"
                frame = draw_text_with_pil(frame, text, (10, 40 + i * 30))

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            frame_count += 1

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_details')
def gesture_details():
    global sorted_gestures
    details = [{"gesture": gesture, "probability": probability} for gesture, probability in sorted_gestures]
    return jsonify(details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
