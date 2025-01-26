import network
import socket
import time
from machine import Pin, PWM
from time import sleep

# Motor pins
motor1_a = Pin(2, Pin.OUT)  
motor1_b = Pin(3, Pin.OUT)
motor1_PWM = PWM(Pin(0))

motor2_a = Pin(4, Pin.OUT)  
motor2_b = Pin(5, Pin.OUT)
motor2_PWM = PWM(Pin(1))
motor1_PWM.freq(1000)
motor2_PWM.freq(1000)

# WiFi details
ssid = 'CYBERTRON'
password = 'Mr.LamYo'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    sleep(1)
    print("Connecting to WiFi...")
print("Connected! IP:", wlan.ifconfig()[0])

# Drive function
def drive(direction):
    global prevDrive  # Declare prevDrive as global
    
    if direction == "stop":
        motor1_PWM.duty_u16(0)
        motor2_PWM.duty_u16(0)  # Stop motor 2
        motor1_a.off()
        motor1_b.off()
        motor2_a.off()
        motor2_b.off()
        prevDrive = 'stop'
    
    elif direction == "foward":
        motor1_a.on()
        motor1_b.off()
        motor2_a.on()
        motor2_b.off()
        motor1_PWM.duty_u16(65535)
        motor2_PWM.duty_u16(65535)
        prevDrive = 'foward'
    
    elif direction == "backward":
        motor1_a.off()
        motor1_b.on()
        motor2_a.off()
        motor2_b.on()
        motor1_PWM.duty_u16(65535)
        motor2_PWM.duty_u16(65535)
        prevDrive = 'backward'
    
    elif direction == "left":
        motor1_a.off()
        motor1_b.on()
        motor2_a.on()
        motor2_b.off()
        motor1_PWM.duty_u16(50000)
        motor2_PWM.duty_u16(50000)
        prevDrive = 'left'
    
    elif direction == "right":
        motor1_a.on()
        motor1_b.off()
        motor2_a.off()
        motor2_b.on()
        motor1_PWM.duty_u16(50000)
        motor2_PWM.duty_u16(50000)
       #prevDrive = 'right'

# HTML for web control interface
html = """ 
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico W Web Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f21120 }
        .button { padding: 20px; font-size: 20px; background-color: #3b3a59; color: white; border: none; cursor: pointer; }
        .button:active { background-color: #45a049; }
        .button.disabled { background-color: #d3d3d3; cursor: not-allowed; }
        .status { margin-top: 20px; font-size: 18px; color: green; }
        .error { margin-top: 20px; font-size: 18px; color: red; }
    </style>
</head>
<body>
    <h1>Gargant</h1>
    <h3>We’ve got our Gargantz an’ we’ve got our weapons. Wot ain't we got? We ain’t got anyfing for target practice iz wot! So I'll tell you wot we're gonna do. We’re gonna give da Humies a taste of ‘ot metal death is wot. We’s gonna take Big Gork and Big Mork ‘ere an’ we’s gonna stomp Hummie!</h3>
    <table>
    <tr><th></th><th><button id="fowardButton" class="button" onclick="movefoward()">foward</button></th></tr>
    <tr>
        <th><button id="leftButton" class="button" onclick="turnLeft()">Left</button></th>
        <th><button id="stopButton" class="button" onclick="stop()">Stop</button></th>
        <th><button id="rightButton" class="button" onclick="turnRight()">Right</button></th>
    </tr>
    <tr><th></th><th><button id="backwardButton" class="button" onclick="moveBackward()">Backward</button></th></tr>
    </table>
    <div id="statusMessage" class="status"></div>
    <div id="errorMessage" class="error"></div>

    <script>
        async function updateStatus(message, isError = false) {
            const statusMessage = document.getElementById('statusMessage');
            const errorMessage = document.getElementById('errorMessage');
            if (isError) { errorMessage.textContent = message; statusMessage.textContent = ''; }
            else { statusMessage.textContent = message; errorMessage.textContent = ''; }
        }

        async function disableButtons() {
            document.getElementById('fowardButton').classList.add('disabled');
            document.getElementById('leftButton').classList.add('disabled');
            document.getElementById('stopButton').classList.add('disabled');
            document.getElementById('rightButton').classList.add('disabled');
            document.getElementById('backwardButton').classList.add('disabled');
        }

        async function enableButtons() {
            document.getElementById('fowardButton').classList.remove('disabled');
            document.getElementById('leftButton').classList.remove('disabled');
            document.getElementById('stopButton').classList.remove('disabled');
            document.getElementById('rightButton').classList.remove('disabled');
            document.getElementById('backwardButton').classList.remove('disabled');
        }

        async function fetchDirection(url) {
            try {
                disableButtons();
                const response = await fetch(url);
                if (!response.ok) throw new Error('Network response was not ok');
                await updateStatus('Command executed successfully');
            } catch (error) {
                await updateStatus(`Error: ${error.message}`, true);
            } finally {
                enableButtons();
            }
        }

        function movefoward() { fetchDirection('/foward'); }
        function moveBackward() { fetchDirection('/backward'); }
        function turnLeft() { fetchDirection('/left'); }
        function turnRight() { fetchDirection('/right'); }
        function stop() { fetchDirection('/stop'); }
    </script>
</body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request_str = str(request)  # Convert the request to string
        
        if '/foward' in request_str:
            drive('foward')
        elif '/backward' in request_str:
            drive('backward')
        elif '/left' in request_str:
            drive('left')
        elif '/right' in request_str:
            drive('right')
        elif '/stop' in request_str:
            drive('stop')
        
        # Send response
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')

