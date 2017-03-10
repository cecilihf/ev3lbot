#!/usr/bin/env python3


import rpyc

conn = rpyc.classic.connect('10.59.2.16') # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely

right_motor = ev3.LargeMotor('outA')
left_motor = ev3.LargeMotor('outD')

right_motor.stop()
left_motor.stop()
    