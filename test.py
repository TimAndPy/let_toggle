import Jetson.GPIO as GPIO
import time

LED_PIN = 31  # D2, fysieke pin 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

print("LED zou nu UIT moeten zijn. Wacht 5 seconden...")
time.sleep(5)

print("LED gaat nu AAN...")
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(5)

print("LED gaat nu UIT...")
GPIO.output(LED_PIN, GPIO.LOW)
time.sleep(5)

GPIO.cleanup()
print("Klaar.")