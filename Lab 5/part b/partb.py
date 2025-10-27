"""
Real-time hand gesture classification using a Teachable Machine model.
Detects 'peace sign', 'wave', and 'I love you' gestures through the webcam.
"""

import cv2
import numpy as np
import tensorflow as tf
import time

# Path to your Teachable Machine model (.h5 or converted TFLite)
MODEL_PATH = "gesture_model.tflite"
LABELS_PATH = "labels.txt"

# Load labels
with open(LABELS_PATH, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Get expected input size
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

last_logged = time.time()
frame_count = 0

print("Starting gesture detection...")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip image horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    image = cv2.resize(frame, (width, height))
    image = np.expand_dims(image.astype(np.float32) / 255.0, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    top_idx = np.argmax(output_data)
    confidence = output_data[top_idx]

    label = f"{classes[top_idx]} ({confidence*100:.1f}%)"
    cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show frame
    cv2.imshow("Gesture Classifier", frame)
    frame_count += 1

    # Print FPS every second
    now = time.time()
    if now - last_logged > 1:
        print(f"{frame_count / (now - last_logged):.1f} FPS")
        frame_count = 0
        last_logged = now

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
