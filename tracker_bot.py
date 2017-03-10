#!/usr/bin/env python3


import rpyc

from ssl import CERT_NONE

#conn = rpyc.classic.connect('10.59.2.16') # host name or IP address of the EV3

conn = rpyc.classic.connect('127.0.0.1', port=12345)

#conn = rpyc.ssl_connect('10.59.2.16', port=18821, keyfile="/home/cecilie/scripts/ev3/client.key",
#                        certfile="/home/cecilie/scripts/ev3/client.crt", ca_certs="/home/cecilie/scripts/ev3/ca.crt")

ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely

right_motor = ev3.LargeMotor('outA')
left_motor = ev3.LargeMotor('outD')
#right_motor.run_timed(time_sp=1000, speed_sp=600)


ev3.Sound.set_volume(100)
#ev3.Sound.speak('Volume is %d' % ev3.Sound.get_volume()).wait()

ultrasonic = ev3.UltrasonicSensor()
rc = ev3.RemoteControl()
ir = ev3.InfraredSensor()


def run_bot():
    try:
        while True:
            right_motor.run_forever(speed_sp=200)
            left_motor.run_forever(speed_sp=200)
            try:
                distance = ultrasonic.distance_centimeters
                print(distance)
            except:
                distance = ultrasonic.distance_centimeters
                print("got an exception, tried to get the distance again")
                print(distance)
            if distance <= 18:
                right_motor.stop()
                left_motor.stop()
                right_motor.run_timed(time_sp=1000, speed_sp=600)
                
                left_motor.polarity = 'inversed'
                left_motor.run_timed(time_sp=1000, speed_sp=600)
                right_motor.wait_while('running')
                left_motor.wait_while('running')
                left_motor.polarity = 'normal'
    except Exception as e:
        print(e)
        stop_and_exit()
        
    
def stop_and_exit():
    print("stop me!!")
    right_motor.stop()
    left_motor.stop()
    #exit(1);
    


rc.on_red_up = stop_and_exit
run_bot()
