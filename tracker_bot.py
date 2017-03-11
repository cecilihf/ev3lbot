#!/usr/bin/env python3


import rpyc
from time import sleep


#conn = rpyc.classic.connect('10.59.2.16') # host name or IP address of the EV3

conn = rpyc.classic.connect('127.0.0.1', port=12345)

#conn = rpyc.ssl_connect('10.59.2.16', port=18821, keyfile="/home/cecilie/scripts/ev3/client.key",
#                        certfile="/home/cecilie/scripts/ev3/client.crt", ca_certs="/home/cecilie/scripts/ev3/ca.crt")

ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely

state_stopped = False

right_motor = ev3.LargeMotor('outA')
left_motor = ev3.LargeMotor('outD')
#right_motor.run_timed(time_sp=1000, speed_sp=600)


ev3.Sound.set_volume(100)
#ev3.Sound.speak('Volume is %d' % ev3.Sound.get_volume()).wait()

ultrasonic = ev3.UltrasonicSensor()
rc = ev3.RemoteControl()
ir = ev3.InfraredSensor()
touch = ev3.TouchSensor()
gyro = ev3.GyroSensor()
gyro.mode = 'GYRO-ANG'



def run_bot():
    try:
        while True:
            print (state_stopped)
            if state_stopped:
                print("Should be stopped, breaking out")
                break
            left_motor.polarity = 'normal'
            right_motor.polarity = 'normal'

            right_motor.run_forever(speed_sp=200)
            left_motor.run_forever(speed_sp=200)
            rc.process()
            crash = touch.is_pressed
            if crash:
                back_up()
                turn_around()
                
            try:
                distance = ultrasonic.distance_centimeters
                print(distance)
                
            except:
                distance = ultrasonic.distance_centimeters
                print("got an exception, tried to get the distance again")
                print(distance)
            if distance <= 18:
                angle = gyro.angle
                print("starting at angle %d" % angle)
                turn_around()
                angle_moved = gyro.angle
                print("rotated %d degrees" % angle)
                
    except Exception as e:
        print(e)
        
        
def turn_around():
    angle_in = gyro.angle
    print("angle in: %d" % angle_in)
    desired_angle_move = -30
    angle_to_stop_at = angle_in - desired_angle_move
    print("angle to stop at: %d" % angle_to_stop_at)
    right_motor.stop()
    left_motor.stop()
    
    left_motor.polarity = 'inversed'
    
    #right_motor.run_forever(speed_sp=400)
    #left_motor.run_forever(speed_sp=400)
    total_angle_moved = 0
    while True:
        print (state_stopped)
        if state_stopped:
            print ("Should be stopped. Breaking out")
            break
        rc.process()
        right_motor.run_timed(time_sp=1000, speed_sp=100)
        left_motor.run_timed(time_sp=1000, speed_sp=100)
        right_motor.wait_while('running')
        left_motor.wait_while('running')
    
    
        angle_moved = gyro.angle
        total_angle_moved += angle_moved
        print("moved %d degrees" % angle_moved)
        print("moved %d degrees total" % total_angle_moved)
        if total_angle_moved <= desired_angle_move:
             right_motor.stop()
             left_motor.stop()
             break       
    
    #right_motor.wait_while('running')
    #left_motor.wait_while('running')
    left_motor.polarity = 'normal'

def back_up():
    right_motor.stop()
    left_motor.stop()
    
    right_motor.polarity = 'inversed'
    left_motor.polarity = 'inversed'
    
    right_motor.run_timed(time_sp=2000, speed_sp=200)
    left_motor.run_timed(time_sp=2000, speed_sp=200)
    
    right_motor.wait_while('running')
    left_motor.wait_while('running')
    
    left_motor.polarity = 'normal'
    right_motor.polarity = 'normal'


def stop(self):
    print("stop me!!")
    global state_stopped
    state_stopped = True
    right_motor.stop()
    left_motor.stop()
    
    
def start(self):
    print("start me!!")
    global state_stopped
    state_stopped = False
    run_bot()
    
    
def idle():
    print("idling")
    while True:
        rc.process()
        sleep(0.01)
        
def turn_around_button(self):
    global state_stopped
    state_stopped = False
    turn_around()
    state_stopped = True

def back_up_button(self):
    back_up()

rc.on_red_up = stop
rc.on_blue_up = start
rc.on_red_down = turn_around_button
rc.on_blue_down = back_up_button
run_bot()
idle()


#while True:
#    print ("moving angle: %d" % gyro.angle)


