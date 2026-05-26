from flask import Flask, request, Response
import cv2
import numpy as np
 
app = Flask(__name__)
 
latest_frame = None
latest_frame_1 = None
latest_frame_2 = None
latest_frame_3 = None
latest_frame_4 = None


 
# Receive frames from laptop
@app.route("/upload_1", methods=["POST"])
def upload_1():
    global latest_frame_1
 
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    latest_frame_1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
 
    return "OK"

# Receive frames from laptop
@app.route("/upload_2", methods=["POST"])
def upload_2():
    global latest_frame_2
 
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    latest_frame_2 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
 
    return "OK"

# Receive frames from laptop
@app.route("/upload_3", methods=["POST"])
def upload_3():
    global latest_frame_3
 
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    latest_frame_3 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
 
    return "OK"

# Receive frames from laptop
@app.route("/upload_4", methods=["POST"])
def upload_4():
    global latest_frame_4
 
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    latest_frame_4 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
 
    return "OK"
 
 
# Stream frames to viewers
def generate(camera_no):
    global latest_frame_1, latest_frame_2, latest_frame_3, latest_frame_4
 
    if(camera_no == "1"):
        while True:
            if latest_frame_1 is None:
                continue
    
            _, buffer = cv2.imencode('.jpg', latest_frame_1)
            frame = buffer.tobytes()
    
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    elif(camera_no == "2"):
        while True:
            if latest_frame_2 is None:
                continue
    
            _, buffer = cv2.imencode('.jpg', latest_frame_2)
            frame = buffer.tobytes()
    
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    elif(camera_no == "3"):
        while True:
            if latest_frame_3 is None:
                continue
    
            _, buffer = cv2.imencode('.jpg', latest_frame_3)
            frame = buffer.tobytes()
    
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    elif(camera_no == "4"):
        while True:
            if latest_frame_4 is None:
                continue
    
            _, buffer = cv2.imencode('.jpg', latest_frame_4)
            frame = buffer.tobytes()
    
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
 
@app.route("/video_feed")
def video_feed():
    value = request.args.get("video_feed")
    return Response(generate(value),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
 
 
@app.route("/")
def home():
    return {
        "status": "Live Camera Server Running",
        "endpoints": {
            "First upload": "/upload_1",
            "Second upload": "/upload_2",
            "Third upload": "/upload_3",
            "Forth upload": "/upload_4",
            "stream": "/video_feed"
        }
    }

 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
