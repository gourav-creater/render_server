from flask import Flask, request, Response
import cv2
import numpy as np
 
app = Flask(__name__)
 
latest_frame = None
 
 
# Receive frames from laptop
@app.route("/upload", methods=["POST"])
def upload():
    global latest_frame
 
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    latest_frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
 
    return "OK"
 
 
# Stream frames to viewers
def generate():
    global latest_frame
 
    while True:
        if latest_frame is None:
            continue
 
        _, buffer = cv2.imencode('.jpg', latest_frame)
        frame = buffer.tobytes()
 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
 
@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
 
 
@app.route("/")
def home():
    return {
        "status": "Live Camera Server Running",
        "endpoints": {
            "upload": "/upload",
            "stream": "/video_feed"
        }
    }
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)