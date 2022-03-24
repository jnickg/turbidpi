# Set up Temp Sensor
1. Connect temp sensor using wiring diagrams found online
2. Change `/boot/config.txt to include the following line:
```
dtoverlay=w1-gpio
```
3. Run `main.py`