import asyncio
import io
import tankControl
from picamera2 import Picamera2
from flask import Flask, Response
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
app = Flask(__name__)

def generate_frames():
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (640, 400)})
    picam2.configure(config)
    picam2.start()

    while True:
        frame = picam2.capture_array()
        stream = io.BytesIO()
        from PIL import Image
        image = Image.fromarray(frame)
        #convert from RGB to JPEG
        image = image.convert("RGB")
        image.save(stream, format='JPEG')
        stream.seek(0)
        
        # Yield frame with proper headers
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Function to run the Flask app
def run_flask_app():
    app.run(host='192.168.69.69', port=5000, threaded=True)

# Function to run tankControl.cameraAngleControl asynchronously
def run_camera_angle_control():
    tankControl.cameraAngleControl()

# Main function to start tasks in parallel
def startup():
    flask_process = multiprocessing.Process(target=run_flask_app)
    flask_process.start()
    run_camera_angle_control()
    print("BLAH")

    # Run a blocking call (multiprocessing) asynchronously

if __name__ == '__main__':
    startup()
    
