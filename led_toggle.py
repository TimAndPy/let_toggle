import Jetson.GPIO as GPIO
import keyboard
import time

# Stel de GPIO-pin in (D13 komt overeen met fysieke pin 13 op de Jetson Nano)
LED_PIN = 13  # Fysieke pin 13 is D2 op het Waveshare-bord

# GPIO initialiseren
GPIO.setmode(GPIO.BOARD)  # Gebruik BOARD-nummering (pin-nummers op het Waveshare-bord)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)  # Stel pin als output en begin met LED uit

# Variabele om de status van de LED bij te houden
led_state = False

print("Druk op de spatiebalk om de LED aan/uit te zetten. Druk op 'q' om te stoppen.")

try:
    while True:
        # Wacht op een spatiebalkdruk
        if keyboard.is_pressed('space'):
            led_state = not led_state  # Wissel de status
            GPIO.output(LED_PIN, GPIO.HIGH if led_state else GPIO.LOW)  # Zet LED aan/uit
            print("LED is nu", "AAN" if led_state else "UIT")
            # Wacht kort om meerdere toggles bij één druk te voorkomen
            while keyboard.is_pressed('space'):
                time.sleep(0.1)
        
        # Stop het programma als 'q' wordt ingedrukt
        if keyboard.is_pressed('q'):
            break

except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker.")

finally:
    # Schoon GPIO op
    GPIO.output(LED_PIN, GPIO.LOW)  # Zet LED uit bij afsluiten
    GPIO.cleanup()
    print("GPIO schoongemaakt.")