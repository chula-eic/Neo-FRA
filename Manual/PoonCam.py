#!/usr/bin/env python3
from cheroot.wsgi import Server, PathInfoDispatcher
from flask import Flask, send_file, Response, request, abort
import cv2
import io
import platform
from turbojpeg import TurboJPEG
import threading
import time
import sys

stream_framerate = 0
stream_target_size = (0, 99999)

jpeg = TurboJPEG(
    lib_path='turbojpeg.dll' if platform.system() == 'Windows' else '/opt/libjpeg-turbo/lib32/libturbojpeg.so.0')

app = Flask(__name__, static_url_path='', template_folder='static')

new_img_ev = threading.Condition()


@app.route('/now.jpg')
def img_now():
    if cur_image is None:
        abort(500)
    buf = jpeg.encode(cur_image)
    return send_file(io.BytesIO(buf), mimetype='image/jpeg')


@app.route('/new.jpg')
def img_new():
    with new_img_ev:
        new_img_ev.wait()
    if cur_image is None:
        abort(500)
    buf = jpeg.encode(cur_image)
    return send_file(io.BytesIO(buf), mimetype='image/jpeg')


@app.route('/stream.mjpg')
def stream():
    try:
        request_height = int(request.args.get('h', 0))
        request_width = int(request.args.get('w', 0))
        if request_height == 0 and request_width == 0:
            request_width, request_height = stream_target_size
        framerate = int(request.args.get('fps', stream_framerate))
    except ValueError:
        abort(400)

    def generate():
        while running:
            img = cur_image
            if img is None:
                return

            height, width, ch = img.shape
            if height > request_height or width > request_width:
                target_width = min(width, request_width)
                target_height = min(height, request_height)
                if target_width == 0:
                    target_width = int(target_height / height * width)
                elif target_height == 0:
                    target_height = int(target_width / width * height)
                img = cv2.resize(img, (target_width, target_height))

            buf = jpeg.encode(img)
            yield ("--jpgboundary\r\n")
            yield ('Content-type: image/jpeg\r\n')
            yield ('Content-length: %s\r\n' % str(len(buf)))
            yield ('\r\n')
            yield buf

            with new_img_ev:
                if framerate:
                    time.sleep(1 / framerate)
                new_img_ev.wait()

    return Response(generate(), mimetype='video/x-motion-jpeg',
                    content_type='multipart/x-mixed-replace; boundary=--jpgboundary')


cur_image = None
running = True


def worker():
    global cur_image
    if len(sys.argv) > 1:
        cam = cv2.VideoCapture(int(sys.argv[1]))
    else:
        cam = cv2.VideoCapture(0)
    if len(sys.argv) > 3:
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, int(sys.argv[2]))
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, int(sys.argv[3]))
    print('Start Capturing...')
    while running:
        ret, img = cam.read()
        if not ret:
            cam.release()
            raise Exception('Cannot get image')
        cur_image = img
        with new_img_ev:
            new_img_ev.notify_all()
    with new_img_ev:
        new_img_ev.notify_all()
    cam.release()


def stop_capture():
    global running
    running = False
    print('Stop Capturing...')


d = PathInfoDispatcher({'/': app})
server = None

if __name__ == '__main__':
    print('Usage: python cam.py [src] [width height]')

    server = Server(('0.0.0.0', 8081 + (int(sys.argv[1]) if len(sys.argv) > 1 else 0)), d)

    t = threading.Thread(target=worker)
    t.start()
    try:
        server.start()
    except KeyboardInterrupt:
        stop_capture()
        server.stop()
    print('Terminated.')
