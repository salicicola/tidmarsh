#!/bin/bash
sudo docker build -f Dockerfile --no-cache --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t salicicola/tidmarsh . 
