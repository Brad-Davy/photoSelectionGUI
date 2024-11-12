<<<<<<< HEAD
FROM python:3.10

=======
FROM python3

FROM python
>>>>>>> e432466bbbac8fad3c69b597f5c3c5f898a6efc4

WORKDIR /app

COPY . /app

<<<<<<< HEAD
RUN apt-get update && apt-get install -y x11-apps libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev libgl1-mesa-glx libglib2.0-0

=======
RUN pip3 install numpy
RUN pip3 install pyqt6
RUN pip3 install ultralytics
RUN pip3 install opencv-python
RUN pip3 install matplotlib

RUN apt-get update 
>>>>>>> e432466bbbac8fad3c69b597f5c3c5f898a6efc4
RUN apt-get install -y libgl1-mesa-glx 
RUN apt-get install -y libxkbcommon0
RUN apt-get install -y libegl1-mesa
RUN apt-get install -y libdbus-1-3
RUN apt-get install -y libxcb-cursor0
<<<<<<< HEAD
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0 libxcb-xinerama0 libxcb-cursor0 

RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

ENV DISPLAY=:0

CMD ["python3", "/app/app.py"]

=======

CMD ["python3", "app.py"]
>>>>>>> e432466bbbac8fad3c69b597f5c3c5f898a6efc4
