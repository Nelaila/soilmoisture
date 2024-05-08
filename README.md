# soilmoisture

Mimosa plants are very sensitive to the right amount of water.
For this reason, I have set up a system to measure soil moisture.
The data is read and saved to a file with the pyserial package.
A web app based on Dash is created in order to visualize the data in real-time.


## Hardware:
- Arduino Uno R3
- Capacitive Soil Moisture Sensor
- USB B to USB A cable

## Software:
- Arduino IDE

## Future developments:
- Change to a wi-fi compatible board
  - perform long-term measurements, no laptop required
  - create access via mobile devices
- Add a camera module
  - create time-lapse videos
  - monitor health state of the plant, correlation to soil moisture
