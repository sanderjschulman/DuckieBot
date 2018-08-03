from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
mh = Adafruit_MotorHAT(addr=0x60)
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
 
atexit.register(turnOffMotors)
myMotor = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
myMotor.setSpeed(150)
while (True):
    print("Forward!")
    myMotor.run(Adafruit_MotorHAT.FORWARD)
    myMotor2.run(Adafruit_MotorHAT.FORWARD) 
    print("\tSpeed up...")
    for i in range(255):
    	    myMotor.setSpeed(i)
    	    time.sleep(0.01)
    	    myMotor2.setSpeed(i)
    	    time.sleep(0.01)
     
    print("\tSlow down...")
    for i in reversed(range(255)):
    	    myMotor.setSpeed(i)
    	    time.sleep(0.01)
    	    myMotor2.setSpeed(i)
    	    time.sleep(0.01)
     
    print("Backward! ")
    myMotor.run(Adafruit_MotorHAT.BACKWARD)
    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
     
    print("\tSpeed up...")
    for i in range(255):
    	    myMotor.setSpeed(i)
    	    time.sleep(0.01)
    	    myMotor2.setSpeed(i)
    	    time.sleep(0.01)
     
    print("\tSlow down...")
    for i in reversed(range(255)):
    	    myMotor.setSpeed(i)
    	    time.sleep(0.01)
    	    myMotor2.setSpeed(i)
    	    time.sleep(0.01)
     
    print("Release")
    myMotor.run(Adafruit_MotorHAT.RELEASE)
    time.sleep(1.0)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    time.sleep(1.0)