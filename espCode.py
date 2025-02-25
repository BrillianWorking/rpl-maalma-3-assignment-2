# Libraries
from machine import ADC, Pin
import ujson
import network
import utime as time
import dht
import urequests as requests

# Ubidots configs
DEVICE_ID = "pakdengklek-esp"
TOKEN = "BBUS-vPrY4JjuPuLa7uCmklaNEfx3naItpV"

# WIFI configs
WIFI_SSID = "Hiro Hayama "
WIFI_PASSWORD = "12345678"

# DHT pin
DHT_PIN = Pin(4)

#ADC.atten(ADC.ATTN_11DB)
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)
#ldr_value = ldr.read()
#time.sleep(1);



#def create_json_data(temperature, humidity):
#    data = ujson.dumps({
#        "device_id": DEVICE_ID,
#        "temp": temperature,
#        "humidity" : humidity,
#        "type": "sensor"
#    })
#    return data
    

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
    print("Telah mengirim data!")

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
while test < 50:
    print("Menghubungkan")
    time.sleep(0.1)
    test+=1;
    
print("WIFI Terhubung!")

dht_sensor = dht.DHT11(DHT_PIN)
#telemetry_data_old = ""

# LDR pin


curr_button_value = "";


while True:
    
    try:
        dht_sensor.measure()
        time.sleep(1)
        ldr_value = ldr.read()
    except:
        ldr_value = -1
    print(ldr_value)

    #time.sleep(0.5)
    
    if(curr_button_value.find("1") != -1):
        print("tombol_menyala", dht_sensor.humidity())
        ldr_value = ldr.read()
        try:
            
            #telemetry_data_new = create_json_data(dht_sensor.temperature(), dht_sensor.humidity())
            
            send_data(dht_sensor.temperature(), dht_sensor.humidity(), ldr_value)
        except:
            pass
    else:
        print("tombol_mati")
        
    try:
        curr_button_value = Check_ButtonAct()
    except:
        print("Error ketika mengecek value tombol")
    
    time.sleep(6)
