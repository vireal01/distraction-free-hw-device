import network
import time
import wifi_config


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Режим станции (клиента)
    wlan.active(True)  # Включение Wi-Fi модуля
    
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(wifi_config.SSID, wifi_config.PASSWORD)

        # Ожидание подключения с таймаутом 10 секунд
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print("Waiting for connection...")
            time.sleep(1)
            timeout -= 1

        if wlan.isconnected():
            print("Connected!")
            print("Network config:", wlan.ifconfig())
        else:
            print("Failed to connect")
            wlan.active(False)
    else:
        print("Already connected!")
        print("Network config:", wlan.ifconfig())

# Автоматически подключаемся к Wi-Fi при загрузке
connect_wifi()