import io
import time
import picamera
from base_camera import BaseCamera
import threading

class cameraObject():
    def __init__(self, *args, **kwargs):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)

    def startRecording(self,fileName):
        self.camera.start_recording(fileName)
        
    def stopRecording(self):
        self.camera.stop_recording()

class Camera(BaseCamera):
    @staticmethod
    def frames():
        #with picamera.PiCamera() as camera:
        # let camera warm up
        time.sleep(2)

        #camera = cameraObject()
        #picamera.PiCamera()
        stream = io.BytesIO()
        #camer = camera.camera
        for _ in camera.camera.capture_continuous(stream, 'jpeg',
                                                use_video_port=True):
            # return current frame
            stream.seek(0)
            yield stream.read()

            # reset stream for next frame
            stream.seek(0)
            stream.truncate()


camera = cameraObject()