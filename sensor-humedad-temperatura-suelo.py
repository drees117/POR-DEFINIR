import adafruit_dht
import board
import time
import RPi.GPIO as GPIO

# Configurar el modo de numeracion de pines (BCM o BOARD)
GPIO.setmode(GPIO.BCM)

# Definir los pines donde se conectan los sensores
pin_dht = 27  # Pin GPIO para el sensor DHT
pin_suelo = 17  # Pin GPIO para el sensor de humedad del suelo

# Configurar el sensor DHT
sensor_dht = adafruit_dht.DHT11(board.D27)

# Configurar el pin del sensor de humedad del suelo como entrada
GPIO.setup(pin_suelo, GPIO.IN)

try:
    while True:
        # Leer el sensor DHT
        try:
            humedad = sensor_dht.humidity
            temperatura = sensor_dht.temperature
            if humedad is not None and temperatura is not None:
                print(f'Temperatura={temperatura:.2f}*C  Humedad={humedad:.2f}%')
            else:
                print('Fallo la lectura del sensor DHT. Intentar de nuevo')
        except RuntimeError as error:
            print(f'Error al leer el sensor DHT: {error}')

        # Leer el estado del sensor de humedad del suelo
        if GPIO.input(pin_suelo) == GPIO.LOW:
            print("El suelo esta humedo")
        else:
            print("El suelo esta seco")

        # Pausa de 1 segundo
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa interrumpido. Limpiando GPIO...")
    GPIO.cleanup()  # Limpiar la configuracion de GPIO
