import adafruit_dht
import board
import time
import RPi.GPIO as GPIO
from github import Github

# Configurar el modo de numeracion de pines (BCM o BOARD)
GPIO.setmode(GPIO.BCM)

# Definir los pines donde se conectan los sensores
pin_dht = 27  # Pin GPIO para el sensor DHT
pin_suelo = 17  # Pin GPIO para el sensor de humedad del suelo

# Configurar el sensor DHT
sensor_dht = adafruit_dht.DHT11(board.D27)

# Configurar el pin del sensor de humedad del suelo como entrada
GPIO.setup(pin_suelo, GPIO.IN)

# Nombre del archivo donde se guardaron las lecturas
file_name = "lecturas_sensores.txt"

# Autenticacion con GitHub
token = "xxxxxxx"  # Reemplaza esto con tu token personal de GitHub
repo_name = "test-1"  # Nombre del repositorio
g = Github(token)
repo = g.get_user().get_repo(repo_name)

try:
    while True:
        with open(file_name, "a") as f:
            # Leer el sensor DHT
            try:
                humedad = sensor_dht.humidity
                temperatura = sensor_dht.temperature
                if humedad is not None and temperatura is not None:
                    lectura = f'Temperatura={temperatura:.2f}*C  Humedad={humedad:.2f}%\n'
                    print(lectura)
                    f.write(lectura)
                else:
                    print('Fallo la lectura del sensor DHT. Intentar de nuevo')
            except RuntimeError as error:
                print(f'Error al leer el sensor DHT: {error}')

            # Leer el estado del sensor de humedad del suelo
            if GPIO.input(pin_suelo) == GPIO.LOW:
                lectura_suelo = "El suelo esta humedo\n"
            else:
                lectura_suelo = "El suelo esta seco\n"
            print(lectura_suelo)
            f.write(lectura_suelo)

        # Leer el contenido del archivo y subirlo a GitHub
        with open(file_name, "r") as file:
            content = file.read()
            try:
                contents = repo.get_contents(file_name, ref="main")
                repo.update_file(contents.path, "Actualizar lecturas de sensores", content, contents.sha, branch="main")
            except:
                repo.create_file(file_name, "Actualizar lecturas de sensores", content, branch="main")

        # Pausa de 1 segundo
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa interrumpido. Limpiando GPIO...")
    GPIO.cleanup()  # Limpiar la configuracion de GPIO

