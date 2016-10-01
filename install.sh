#!/bin/bash

USER=energymon
NAME=energymon

BIN_FILE=/usr/local/bin/$NAME

SERVICE_NAME=$NAME.service
SERVICE_FILE=/etc/systemd/system/$SERVICE_NAME

useradd --system -G gpio,kmem $USER

cp bin/monitor.py $BIN_FILE

chown $USER $BIN_FILE
chmod +x $BIN_FILE

cp service/energymon.service $SERVICE_FILE
chmod 664 $SERVICE_FILE

systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
