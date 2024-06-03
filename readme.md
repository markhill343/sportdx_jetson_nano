sudo docker build -t yolov8-pose-estimation-jupyter .



sudo docker run --runtime nvidia --device=/dev/video0 --privileged --rm -it -p 8080:8080 -p 8888:8888 --name yolov8-pose-estimation-jupyter yolov8-pose-estimation-jupyter /bin/bash


http://192.168.178.94:8080/video_feed