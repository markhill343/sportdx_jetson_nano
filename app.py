from flask import Flask, Response
import cv2
from ultralytics import YOLO
import logging
import sys

app = Flask(__name__)

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

# Load the YOLOv8 model
model = YOLO('yolov8n-pose.pt')

# Initialize the USB webcam
cap = cv2.VideoCapture('/dev/video0')

if not cap.isOpened():
    logger.error("Error: Could not open video stream.")
    raise RuntimeError("Error: Could not open video stream.")
else:
    logger.info("Video stream opened successfully.")

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture image")
            continue

        logger.debug(f"Captured a frame: shape={frame.shape}, dtype={frame.dtype}")

        # Perform pose estimation
        try:
            results = model(frame)
            logger.debug("Pose estimation completed")
        except Exception as e:
            logger.error(f"Pose estimation failed: {e}")
            continue

        # Render the pose on the frame
        try:
            for result in results:
                if hasattr(result, 'plot'):
                    frame = result.plot()
                else:
                    frame = result.render()
            logger.debug("Rendering completed")
        except Exception as e:
            logger.error(f"Rendering failed: {e}")
            continue

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            logger.error("Failed to encode frame")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    logger.info("Video feed requested")
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=8080)
