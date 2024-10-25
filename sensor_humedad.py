import RPi.GPIO as GPIO
import time

# Configurar el modo de numeracion de pines (BCM o BOARD)
GPIO.setmode(GPIO.BCM)

# Definir el pin donde se conecta el sensor
pin_sensor = 17  # Pin GPIO 17 (cambia esto si usas otro pin)

# Configurar el pin como entrada
GPIO.setup(pin_sensor, GPIO.IN)

try:
    while True:
        # Leer el estado del sensor (LOW = humedo, HIGH = seco)
        if GPIO.input(pin_sensor) == GPIO.LOW:
            print("El suelo esta humedo")
        else:
            print("El suelo esta seco")
        
        # Pausa de 1 segundo
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa interrumpido. Limpiando GPIO...")
    GPIO.cleanup()  # Limpiar la configuracion de GPIO