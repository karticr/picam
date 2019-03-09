import io
import time
import picamera
from base_camera import BaseCamera
import threading

class cameraObject():
    def __init__(self, *args, **kwargs):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.framerate       = 30
        self.camera.framerate_range = (10, 30)
        self.camera.resolution      = (1920, 1080)
        self.camera.rotation        = 0
        self.camera.vflip           = False
        self.camera.hflip           = False
        self.rec_state              = False
        self.video_dir              = "/home/pi/picam/server/static/share/videos"
        self.picture_dir            = "/home/pi/picam/server/static/share/pictures"

    def takePicture(self, filename):
        take_pic = self.camera.capture('{}/{}.jpg'.format(self.picture_dir, filename))
        print(take_pic)
        return take_pic

    def startRecording(self, filename):
        start_rec = self.camera.start_recording('{}/{}.h264'.format(self.video_dir, filename), format='h264')
        self.rec_state = True
        print(start_rec)
        return start_rec

    def recordingStatus(self):
        curr_rec_state = self.rec_state
        print(curr_rec_state)
        return curr_rec_state
    
    def stopRecording(self):
        rec_stop = self.camera.stop_recording()
        self.rec_state = False
        print(rec_stop)
        return rec_stop

    def changeSettings(self, settingsDict):
        self.camera.framerate       = settingsDict['fps']
        self.camera.framerate_range = settingsDict['fps_range']
        self.camera.resolution      = settingsDict['resolution']
        self.camera.rotation        = settingsDict['rotation']
        self.camera.hflip           = settingsDict['h_flip']
        self.camera.vflip           = settingsDict['v_flip']
        self.video_dir              = settingsDict['video_dir']
        self.picture_dir            = settingsDict['pic_dir']
        
    def recordingState(self):
        return self.rec_state

    def settings(self):      
        data = {
            "fps"       : str(self.camera.framerate), 
            "fps_range" : str(self.camera.framerate_range).replace("(","").replace(")",""),
            "resolution": str(self.camera.resolution),
            'rotation'  : str(self.camera.rotation),
            "h_flip"    : str(self.camera.hflip),
            "v_flip"    : str(self.camera.vflip),
            "video_dir" : str(self.video_dir),  
            "pic_dir"   : str(self.picture_dir) 
        }
        return data

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