FROM python3

FROM python

WORKDIR /app

COPY . /app

RUN pip3 install numpy
RUN pip3 install pyqt6
RUN pip3 install ultralytics
RUN pip3 install opencv-python
RUN pip3 install matplotlib

RUN apt-get update 
RUN apt-get install -y libgl1-mesa-glx 
RUN apt-get install -y libxkbcommon0
RUN apt-get install -y libegl1-mesa
RUN apt-get install -y libdbus-1-3
RUN apt-get install -y libxcb-cursor0

CMD ["python3", "app.py"]
