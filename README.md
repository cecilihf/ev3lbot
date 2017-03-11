# ev3lbot

Our goal is to let ev3lbot be your personal trainer as well as body guard.
ev3lbot will track your movements, tell you when you've been inactive for
too long, or drinking too much coffee. If he sees any intruders, he will
take appropriate measures to get rid of the intruders. ev3lbot is your
own personal little sister.

# Pre-requisites #

- You need an ev3 (duh)
- And a computer with Python 3 installed


# Getting started

## 1. Install ev3dev ##

To get started controlling your ev3lbot, install
[ev3dev](http://www.ev3dev.org/) on it, [detailed instructions are found here](http://www.ev3dev.org/docs/getting-started/)

## 2. Install RPyC ##

Now install [RPyC](http://python-ev3dev.readthedocs.io/en/latest/rpyc.html) and
start an RPyC server. 

For security reasons we recommend letting the servers
only accept connections over localhost, and then use an SSH tunnel to talk
to it.

## 3. Run it! ##

Run tracker_bot.py to let your Robot start roaming around. For now it will
only move around peacefully and try to avoid crashing into walls, but new
features will be added continuously throughout ev3lbot's lifetime. 

Should the robot be refusing to stop in an emergency, you can run
stop_bot.py to safely bring it to a halt.

  python tracker_bot.py
