# Libraries
from machine import ADC, Pin
import ujson
import network
import utime as time
import dht
import urequests as requests

# Ubidots configs
DEVICE_ID = "rpl-maalma-3-esp"
TOKEN = "BBUS-vPrY4JjuPuLa7uCmklaNEfx3naItpV"

# WIFI configs
WIFI_SSID = "Hiro Hayama "
WIFI_PASSWORD = "12345678"

# DHT pin
DHT_PIN = Pin(4)
dht_sensor = dht.DHT11(DHT_PIN)

# LDR pin and configs
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)
    

# Send data to ubidots
def send_data(temperature, humidity, lux):
    # HTTP post
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity" : humidity,
        "lux" : lux
    }
    response = requests.post(url, json=data, headers=headers)
    print("Respon:", response.text)
    print("Telah mengirim data ke ubidots!")

# Save data to database
def save_data(temperature, humidity, lux):
    # Convert local time to readable format
    localtime = time.localtime()
    hours = str(localtime[3])
    minutes = str(localtime[4])
    seconds = str(localtime[5])
    if(len(hours) < 2):
        hours = "0"+hours
    if(len(minutes) < 2):
       minutes = "0"+minutes
    if(len(seconds) < 2):
       seconds = "0"+seconds
    
    currenttime = f"{hours}:{minutes}:{seconds}"
    currentdate = f"{localtime[2]}-{localtime[1]}-{localtime[0]}"
    url = "http://192.168.250.146:5000/v1/com_database" 
    headers = {"Content-Type": "application/json"}
    data = {
        "temp": temperature,
        "humidity" : humidity,
        "lux" : lux,
        "time-stamp" : f"{currentdate} | {currenttime}",
    }
    # HTTP post
    response = requests.post(url, json=data, headers=headers)
    print("Respon:", response.text)
    print("Telah mengirim data ke database!")
    
def get_data():
    url = "http://192.168.250.146:5000/v1/com_database" 
    headers = {"Content-Type": "application/json"}
    # HTTP get
    response = requests.get(url, headers=headers)
    responseload = ujson.loads(response.text)
    print("Telah mengambil data dari database!")
    print("Jumlah data diambil :", len(responseload["data"]))
    
    for i in responseload["data"]:
        print(i)

# Get switch button data from ubidots
def Check_ButtonAct():
    # Ubidots button switch variable name
    button_var = "button_act"
    # HTTP get
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}/{button_var}/lv"
    headers = {"X-Auth-Token": TOKEN}
    response = requests.get(url, headers=headers);
    return response.text;
    
# Connect to WIFI
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Menghubungkan ESP 32 ke WIFI")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)
test = 0
while not wifi_client.isconnected():
    print("Menghubungkan")
    time.sleep(0.1)
    test+=1;
    
print("WIFI Terhubung!")

curr_button_value = "";


while True:
    
    # Measure sensors
    try:
        dht_sensor.measure()
        time.sleep(1)
        ldr_value = ldr.read()
    except:
        ldr_value = -1
    
    # Check current button status
    try:
        curr_button_value = Check_ButtonAct()
    except:
        print("Error ketika mengecek value tombol")
    
    # If button is on, then send data
    if(curr_button_value.find("1") != -1):
        print("tombol_menyala")
        ldr_value = ldr.read()
        # Send data to ubidots and database
        try:
            print("mengirim data ke ubidots dan database")
            save_data(dht_sensor.temperature(), dht_sensor.humidity(), ldr_value)
            time.sleep(0.5)
            send_data(dht_sensor.temperature(), dht_sensor.humidity(), ldr_value)
        except:
            pass
    else:
        print("tombol_mati")
    
    time.sleep(0.5)
    try:
        get_data()
    except:
        print("Error tidak dapat mengambil data")
    
    time.sleep(6)