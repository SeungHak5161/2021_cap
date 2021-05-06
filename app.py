from flask import Flask
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
#GPIO.setup(6, GPIO.OUT)

GPIO.output(17, GPIO.LOW)
#GPIO.output(6, GPIO.LOW)

app = Flask(__name__)

@app.route('/')
def index():
        return 'Hello world'

@app.route('/on')
def led_on():
        GPIO.output(17, GPIO.HIGH)
        #GPIO.output(6, GPIO.LOW)
        return 'LED ON'
        
@app.route('/off')
def led_off():
        GPIO.output(17, GPIO.LOW)
        #GPIO.output(6, GPIO.LOW)
        return 'LED OFF'

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
