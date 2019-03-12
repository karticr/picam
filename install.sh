apt-get update
apt-get upgrade

# installing dependencies
apt-get install python3 python3-pip 
pip3 install flask flask-socketio picamera

# moving the source to var
cp -R server /var/PiCamServer

# setting up the service for auto launch
cp picamServer.service /etc/systemd/system/picamServer.service
systemctl start picamServer.service
systemctl enable picamServer.service