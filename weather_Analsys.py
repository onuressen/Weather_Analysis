import requests # HTTP istekleri göndermek için gerekli kütüphane
import json # JSON verilerini işlemek için gerekli kütüphane
import datetime # Tarih ve saat işlemleri için gerekli kütüphane
import psychrolib # Hava koşulları hesaplamaları için gerekli kütüphane
import pypyodbc # SQL Server veritabanına bağlanmak için gerekli kütüphane

# OpenWeatherMap'ten API anahtarınızı kullanarak hava durumu verilerini almak için gerekli URL'yi oluşturun
api_key   = "" # OpenWeatherMap API anahtarı
latitude  =  # Enlem
longitude =  # Boylam

weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude, longitude, api_key)

# API'ye istek gönderin
response = requests.get(weather_url)

if response.status_code == 200:
    # Başarılıysa, yanıttan hava durumu bilgilerini çıkarın
    weather_data = response.json() # Yanıt verisini JSON formatında alın
    temperature = weather_data["main"]["temp"] # Sıcaklık verisi
    humidity = weather_data["main"]["humidity"] # Bağıl nem verisi
    wind_speed = weather_data["wind"]["speed"] # Rüzgar hızı verisi
    description = weather_data["weather"][0]["description"] # Hava durumu açıklaması
    pressure = weather_data["main"]["pressure"] # Basınç verisi
    feels_like = weather_data["main"]["feels_like"] # Hissedilen sıcaklık verisi
    sea_level = weather_data["main"]["feels_like"] # Deniz seviyesi verisi

    temperature = round(temperature - 273.15, 2) # Kelvin cinsinden sıcaklık verisini Celsius'a dönüştürün ve virgülden sonra iki haneli olacak şekilde yuvarlayın
    feels_like1 = round(feels_like - 273.15, 2) # Kelvin cinsinden hissedilen sıcaklık verisini Celsius'a dönüştürün ve virgülden sonra iki haneli olacak şekilde yuvarlayın
    date_time = datetime.datetime.now() # Şu anki zaman ve tarih bilgisini alın

    psychrolib.SetUnitSystem(psychrolib.SI) # Hava koşulları hesaplamaları için SI birim sistemini ayarlayın

    # Hesaplamalar için gerekli hava koşulları verilerini tanımlayın
    TDryBulb = temperature # Kuru termometre sıcaklık verisi
    RelHumt = humidity # Bağıl nem verisi
    Pressure = pressure*10 # Basınç verisini


    # Bağıl nem değerini dönüştür
    RelHum = RelHumt / 100

    # Nemli hava özelliklerini hesapla
    TDewPoint = psychrolib.GetTDewPointFromRelHum(TDryBulb, RelHum)
    TWetBulb = psychrolib.GetTWetBulbFromRelHum(TDryBulb, RelHum, Pressure)
    HumRatio = psychrolib.GetHumRatioFromRelHum(TDryBulb, RelHum, Pressure)
    MoistAirEnthalpy = psychrolib.GetMoistAirEnthalpy(TDryBulb, HumRatio)
    MoistAirDensity = psychrolib.GetMoistAirDensity(TDryBulb, HumRatio, Pressure)
    MoistAirVolume = psychrolib.GetMoistAirVolume(TDryBulb, HumRatio, Pressure)

    # Hesaplanan değerleri virgülden sonra iki hane ile yuvarlayın
    TDewPoint = round(TDewPoint, 2)
    TWetBulb = round(TWetBulb, 2)
    HumRatio = round(HumRatio, 5)
    MoistAirEnthalpy = round(MoistAirEnthalpy, 2)
    MoistAirDensity = round(MoistAirDensity, 6)
    MoistAirVolume = round(MoistAirVolume, 6)

else:
    # If the request was unsuccessful, print an error message
    print("Failed to retrieve weather information. Response code: {}".format(response.status_code))

print(TDewPoint,HumRatio,HumRatio  )

# SQL Server'a bağlan
connection = pypyodbc.connect('Driver={SQL Server};''Server=.\SQLEXPRESS;''Database=weather_table;''Trusted_Connection=True')
cursor = connection.cursor()

#Veri ekleme fonksiyonu
def veriekle():
    cursor.execute("insert into izmir values(?,?,?,?,?,?,?,?,?,?,?,?,?)",

        (date_time, description, wind_speed, pressure,feels_like1, temperature,humidity,TDewPoint,TWetBulb,HumRatio,MoistAirEnthalpy,MoistAirDensity,MoistAirVolume))
    connection.commit()

#Veri ekleme fonksiyonunu çağırarak SQL Server'a veri ekleyin
veriekle()

#Veritabanı bağlantısını kapat
connection.close()
