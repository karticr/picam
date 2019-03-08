from flask import Flask, render_template, Response, flash, redirect, url_for, session, logging, request			# Python Libraries
import threading
from camera_pi import * 																						# Custom Libraries
from time import sleep
import datetime
import os

dir = "/home/pi/FlaskSite/static/videos"																	    # Location for storing videos

app = Flask(__name__)																							# Flask Object
cam = Camera()																								  	# Camera Control Object

record_bool = False

def getDateTime():
    dateTime = '{0:%Y-%m-%d}'.format(datetime.datetime.now())
    onlyTime = '{0:%H:%M:%S}'.format(datetime.datetime.now())
    return "/"+dateTime+"_"+onlyTime+'.h264'

def gen(camera):
		while True:
			frame = camera.get_frame()
			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def Podglad_Wideo():
	return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# path to the archive. for now there is nothing there
@app.route('/archive')
def Archiwum():
    list_of_videos  = os.listdir('/home/pi/FlaskSite/static/videos')													# Directory for saving the videos
    print(list_of_videos)
    return render_template('dirs.html', list_of_videos = list_of_videos)



@app.route('/startrec')                                          # Modal Form to fetch the timer to run the recording for.
def startRecording():
	try:
		print("recording started")
		file_name = dir+getDateTime()
		print(file_name)
		camera.startRecording(file_name)
	except:
		print("fudge 1")
		pass

	return redirect("/")

@app.route('/stoprec')                                          # Modal Form to fetch the timer to run the recording for.
def stopRecording():
	try:
		camera.stopRecording()
		print("recording ended")
	except:
		print("fudge 2")
		pass
	return redirect("/")

if __name__ == '__main__':

	app.run(host='0.0.0.0', port=80, threaded=True)
