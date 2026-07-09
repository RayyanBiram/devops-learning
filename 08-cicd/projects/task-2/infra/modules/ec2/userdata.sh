#!/bin/bash

apt-get update -y
apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

usermod -aG docker ubuntu

cd /home/ubuntu

systemctl enable docker.service
systemctl start docker.service
systemctl enable containerd.service
systemctl start containerd.service