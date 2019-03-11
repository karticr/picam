from flask import Flask, render_template, flash, request, url_for, redirect, Response, jsonify, flash, session	
from flask_socketio import SocketIO, send, emit
from threading import Thread
from camera_pi import * 											    
from time import sleep
import datetime
import os
from random import randint

app = Flask(__name__)		
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
																		
cam = Camera()	

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
def index():
	return render_template('index.html')

@app.route('/raw_output')
def cameraOnlyOutput():
	return render_template('cameraonly.html')

@app.route('/video_feed')
def videoFeed():
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

@socketio.on('connect', namespace='/chat')
def test_connect():
        print("why?")
        emit('my response', {'data': 'Connected'})

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('/control')
def camControl(msg):
    print('control msg,', msg)
    if (msg == "recState"):
        cur_state = camera.recordingState()
        socketio.emit('/recstate', str(cur_state), broadcast=True)



def threader():
    last_state = False
    while True:
        cur_state = camera.recordingState()
        if (cur_state != last_state):
            socketio.emit('/recstate', str(cur_state), broadcast=True)
            last_state = camera.recordingState()
        sleep(2)

if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=80, threaded=True)
    # Thread(target= threader).start()
    socketio.run(app, host='0.0.0.0', port = 80)
