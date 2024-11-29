import adafruit_dht
import board
import time

# Configura el sensor DHT
sensor = adafruit_dht.DHT11(board.D27)  # Asegurate de que el pin sea el correcto

while True:
    try:
        # Lee la humedad y la temperatura
        humedad = sensor.humidity
        temperatura = sensor.temperature
        if humedad is not None and temperatura is not None:
            print(f'Temperatura={temperatura:.2f}*C  Humedad={humedad:.2f}%')
        else:
            print('Fallo la lectura del sensor. Intentar de nuevo')
    except RuntimeError as error:
        # Muestra errores de lectura
        print(f'Error de lectura en el sensor: {error}')
    
    time.sleep(5)
