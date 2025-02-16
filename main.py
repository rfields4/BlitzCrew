import io
from picamera2 import Picamera2
from flask import Flask, Response

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)