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
    return "{}_{}".format(dateTime, onlyTime)

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


@app.route('/camera', methods=["GET", "POST"])
def picturesapi():
    try:
        if request.method == "POST":
            cmd   = request.args['cmd']
            
            if(cmd == "start_recording"):
                current_date_time = getDateTime()
                camera.startRecording(current_date_time)

            if(cmd == "stop_recording"):
                camera.stopRecording()

            if(cmd == "take_picture"):
                current_date_time = getDateTime()
                camera.takePicture(current_date_time)

            if(cmd == "settings"):
                data = c.settings()
                print(data)
                return jsonify(data)

            if(cmd == "editsettings"):
                new_settings = request.json
                new_settings['fps']        = int(new_settings['fps'])
                new_settings['resolution'] = tuple([int(x) for x in new_settings['resolution'].split("x")])
                new_settings['fps_range']  = tuple([float(x) for x in new_settings['fps_range'].split(",")])
                 
                print(new_settings['rotation'])
                print(type(new_settings['rotation']))

                new_settings['rotation']   = int(new_settings['rotation'])      
                
                if(new_settings['h_flip'] == "True"):
                    new_settings['h_flip'] = True
                else:
                    new_settings['h_flip'] = False

                if(new_settings['v_flip'] == "True"):
                    new_settings['v_flip'] = True
                else:
                    new_settings['v_flip'] = False   

                print(new_settings['rotation'])
                print(type(new_settings['rotation']))

                camera.changeSettings(new_settings)
            if(cmd == "status"):
                return str(camera.recordingState())
            return "Success"
        else: 
            return "3"

    except Exception as e:
        print(str(e))
        return "0"
		

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, threaded=True)
