from flask import Blueprint, Response, render_template
from app.model.camera_manager import CameraManager

bp = Blueprint('camera', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    def generate():
        while True:
            frame = CameraManager.get_frame(camera_index)
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
