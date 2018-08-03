# Import the device reading library
import atexit
from evdev import InputDevice, categorize, ecodes, KeyEvent, list_devices
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

mh = Adafruit_MotorHAT(addr=0x60)

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

lmotor = mh.getMotor(1)
rmotor = mh.getMotor(2)

# speed = -32768 to 32768
# motor.setSpeed(mspd), mspd 0 to 255
# motor.run(dir), dir BACKWARD, FORWARD, RELEASE, BRAKE
def runMotor(motor, speed):
    if speed<-32768:
        motor.setSpeed(255)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    elif speed>32768:
        motor.setSpeed(255)
        motor.run(Adafruit_MotorHAT.FORWARD)
    elif speed>=-32768 and speed<0:
        motor.setSpeed(int(-speed/129.0))
        motor.run(Adafruit_MotorHAT.BACKWARD)
    elif speed>0 and speed<=32768:
        motor.setSpeed(int(-speed/129.0))
        motor.run(Adafruit_MotorHAT.FORWARD)
    else:
        motor.setSpeed(0)
        motor.run(Adafruit_MotorHAT.BRAKE)
    




# Get the name of the Logitech Device
def getInputDeviceByName(name):
  devices = [InputDevice(fn) for fn in list_devices()]
  for device in devices:
    if device.name == name:
      return InputDevice(device.fn)
  return None

# Import our gamepad.
gamepad = getInputDeviceByName('Logitech Gamepad F710')

# Loop over the gamepad's inputs, reading it.
for event in gamepad.read_loop():
  if event.type == ecodes.EV_KEY:
    keyevent = categorize(event)
    if keyevent.keystate == KeyEvent.key_down:
      print(keyevent.keycode)
      # example key detection code
      if 'BTN_A' in keyevent.keycode:
        # Do something here when the A button is pressed
        pass
      elif 'BTN_START' in keyevent.keycode:
        # Do something here when the START button is pressed
        pass
  elif event.type == ecodes.EV_ABS:
    if event.code == 0:
      print('PAD_LR '+str(event.value))
    elif event.code == 1:
      print('PAD_UD '+str(event.value))
    elif event.code == 2:
      print('TRIG_L '+str(event.value))
    elif event.code == 3:
      print('JOY_LR '+str(event.value))
      runMotor(lmotor,event.value)
    elif event.code == 4:
      print('JOY_UD '+str(event.value))
      runMotor(rmotor,event.value)
    elif event.code == 5:
      print('TRIG_R '+str(event.value))
    elif event.code == 16:
      print('HAT_LR '+str(event.value))
    elif event.code == 17:
      print('HAT_UD '+str(event.value))
    else:
      pass