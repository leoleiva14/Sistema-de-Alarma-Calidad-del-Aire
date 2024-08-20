from celery import Celery
from celery.schedules import timedelta
import requests
import json
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import session, WeatherData

# Leer configuración
config = configparser.ConfigParser()
config.read("pipeline.cfg")

# Configuraciones de las APIs
apis = [
    {"url": config["api1"]["url"], "token": config["api1"]["token"]},
    {"url": config["api2"]["url"], "token": config["api2"]["token"]},
    {"url": config["api3"]["url"], "token": config["api3"]["token"]}
]


# Tarea para evaluar AQI y enviar correos electrónicos
def send_email(subject, body, to_email):
    from_email = "andreyleiva96@gmail.com"
    password = "mypassword"  # Para correrlo necesita la contraseña real

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Error al enviar correo: {e}")


# Crear "app" de Celery
app = Celery("tasks", broker="redis://localhost")


# Función para procesar datos y guardarlos en la base de datos
def process_and_save(data):
    for record in data["data"]:
        new_record = WeatherData(
            city_name=record["city_name"],
            country_code=record["country_code"],
            datetime=record["datetime"],
            lat=record["lat"],
            lon=record["lon"],
            temp=record["temp"],
            app_temp=record["app_temp"],
            aqi=record["aqi"],
            clouds=record["clouds"],
            dewpt=record["dewpt"],
            wind_spd=record["wind_spd"],
            wind_dir=record["wind_dir"],
            pres=record["pres"],
            rh=record["rh"],
            ob_time=record["ob_time"]
        )
        session.add(new_record)
    session.commit()


# Tarea para obtener y procesar datos de una API
@app.task
def fetch_and_store(api_url, api_token):
    headers = {"X-Auth-Token": api_token}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        process_and_save(data)
    else:
        print(f"Error fetching data from {api_url}: {response.status_code}")


# Tarea para evaluar AQI y enviar correos electrónicos
@app.task
# Función para procesar datos y guardarlos en la base de datos
def evaluate_aqi_and_alert():
    data = session.query(WeatherData).all()
    for record in data:
        aqi = record.aqi
        if 101 <= aqi <= 150:
            subject = "Alerta de AQI: No saludable para grupos sensibles"
            body = (
                f"El índice de calidad del aire (AQI) en {record.city_name} "
                f"es {aqi}. "
                "Las personas con enfermedades respiratorias, "
                "niños y ancianos "
                "deben tomar precauciones."
            )
            send_email(subject, body, "andrelvps4@gmail.com")
        elif 151 <= aqi <= 200:
            subject = "Alerta de AQI: No saludable"
            body = (
                f"El índice de calidad del aire (AQI) en {record.city_name} "
                f"es {aqi}. "
                "Todos pueden experimentar efectos para la salud; los grupos "
                "sensibles pueden experimentar efectos más graves."
            )
            send_email(subject, body, "andrelvps4@gmail.com")
        elif 201 <= aqi <= 300:
            subject = "Alerta de AQI: Muy no saludable"
            body = (
                f"El índice de calidad del aire (AQI) en {record.city_name} "
                f"es {aqi}. "
                "Advertencias sanitarias de condiciones de emergencia. "
                "Toda la población se vería afectada."
            )
            send_email(subject, body, "andrelvps4@gmail.com")
        elif 301 <= aqi <= 500:
            subject = "Alerta de AQI: Peligroso"
            body = (
                f"El índice de calidad del aire (AQI) en {record.city_name} "
                f"es {aqi}. "
                "Alerta sanitaria: todos pueden experimentar efectos más "
                "graves para la salud."
            )
            send_email(subject, body, "andrelvps4@gmail.com")


# Tarea para actualizar datos de todas las APIs
@app.task
def update_weather_data():
    for api in apis:
        fetch_and_store(api["url"], api["token"])


# Configurar el planificador de tareas de Celery
app.conf.beat_schedule = {
    # Tarea para obtener los datos del api yguardarlos en la base de datos.
    "update-weather-data": {
        "task": "tasks.update_weather_data",
        "schedule": timedelta(seconds=int(config["scheduler"]["period"])),
    },
    # Tarea para activar la alerta en caso de niveles altos en el aqi.
    "evaluate-aqi-and-alert": {
        "task": "tasks.evaluate_aqi_and_alert",
        "schedule": timedelta(seconds=120),
    }
}
