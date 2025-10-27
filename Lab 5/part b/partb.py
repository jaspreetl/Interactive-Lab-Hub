"""
Gesture interaction using Teachable Machine model (Shush / Scratch)

This script loads a Teachable Machine TensorFlow Lite model trained to
recognize two gestures:
1. Index finger to lips (Shush)
2. Head scratch (Scratch)

When a gesture is detected, it prints and overlays a corresponding
reaction message on the webcam feed.
"""

import cv2
import numpy as np
import tensorflow as tf
import time

MODEL_PATH = "model.tflite"
LABELS_PATH = "labels.txt"
CONF_THRESHOLD = 0.7  # confidence threshold for predictions

# Load class labels
with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Get input shape
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera ready. Press 'q' to quit.")

prev_gesture = None
last_action_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame.")
        break

    # Mirror image for natural webcam view
    frame = cv2.flip(frame, 1)

    # Preprocess the image for model input
    img = cv2.resize(frame, (width, height))
    img = np.expand_dims(img, axis=0).astype(np.uint8)  # uint8, no normalization

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]


    # Find top prediction
    top_index = np.argmax(output_data)
    confidence = output_data[top_index]
    prediction = labels[top_index] if top_index < len(labels) else "Unknown"

    if confidence > CONF_THRESHOLD:
        cv2.putText(frame, f"{prediction} ({confidence*100:.1f}%)", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        if prediction.lower().startswith("shush"):
            message = "Quiet mode activated"
        elif prediction.lower().startswith("scratch"):
            message = "Thinking mode..."
        else:
            message = ""

        # Prevent rapid message spamming
        if prediction != prev_gesture or time.time() - last_action_time > 2:
            if message:
                print(message)
                last_action_time = time.time()
                prev_gesture = prediction

            if message:
                cv2.putText(frame, message, (30, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 0), 2)

    else:
        cv2.putText(frame, "Detecting...", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)

    cv2.imshow("Gesture Detector", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Exiting gracefully.")
