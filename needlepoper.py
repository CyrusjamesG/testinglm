
import time
from time import sleep
from machine import Pin, PWM


servo1_PWM = PWM(Pin(28))
servo2_PWM = PWM(Pin(20))
servo1_PWM.freq(50)
servo2_PWM.freq(50)


firstState = 1
secondState = 2
thirdState = 3
currentState = firstState


while True:
    if currentState is firstState:
        servo1_PWM.duty_u16(1500)
        servo2_PWM.duty_u16(1500)
        sleep(1)
        servo1_PWM.duty_u16(8150)
        servo2_PWM.duty_u16(8150)
        sleep(1)
print('Hi')
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.slidecontainer {
  width: 100%;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 15px;
  border-radius: 5px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #04AA6D;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #04AA6D;
  cursor: pointer;
}
</style>
</head>
<body>

<h1>Round Range Slider</h1>

<div class="slidecontainer">
  <input type="range" min="1" max="100" value="50" class="slider" id="myRange">
  <p>Value: <span id="demo"></span></p>
</div>

<script>
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}
</script>

</body>
</html>
