from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

# Datos de configuración
config = configparser.ConfigParser()
config.read("pipeline.cfg")
system = config["db"]["system"]
name = config["db"]["name"]

# Crear la clase base de la tabla
Base = declarative_base()


# Definir los modelos
class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String)
    country_code = Column(String)
    datetime = Column(String)  # Usa String para mantener el formato de la API
    lat = Column(Float)
    lon = Column(Float)
    temp = Column(Float)
    app_temp = Column(Float)
    aqi = Column(Integer)
    clouds = Column(Integer)
    dewpt = Column(Float)
    wind_spd = Column(Float)
    wind_dir = Column(Integer)
    pres = Column(Float)
    rh = Column(Float)
    ob_time = Column(String)


# Crear la conexión a la base de datos
engine = create_engine(f"{system}:///{name}")
Session = sessionmaker(bind=engine)
session = Session()

# Crear la(s) tabla(s) en la base de datos
Base.metadata.create_all(engine)
