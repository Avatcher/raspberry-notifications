#!/usr/bin/bash

for service in $(ls *.service); do
	echo $service
	cp "./$service" /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable "$service"
done
