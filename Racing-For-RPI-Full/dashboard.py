import pygame
import math
import json
from flask import Flask, render_template
import threading

app = Flask(__name__)

speed = 0
rpm = 0

# Load controller config
try:
    with open("controller_config.json") as f:
        config = json.load(f)
        STEERING_AXIS = config.get("steering_axis", 0)
        THROTTLE_AXIS = config.get("throttle_axis", 2)
        BRAKE_AXIS = config.get("brake_axis", 3)
        DEADZONE = config.get("deadzone", 0.05)
except FileNotFoundError:
    STEERING_AXIS = 0
    THROTTLE_AXIS = 2
    BRAKE_AXIS = 3
    DEADZONE = 0.05

def controller_loop():
    global speed, rpm
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller found.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()

        steer = joystick.get_axis(STEERING_AXIS)
        throttle = joystick.get_axis(THROTTLE_AXIS)
        brake = joystick.get_axis(BRAKE_AXIS)

        if abs(throttle) < DEADZONE:
            throttle = 0
        if abs(brake) < DEADZONE:
            brake = 0

        speed = max(0, int((1 - throttle) * 340))
        rpm = max(0, int((1 - throttle) * 10000))

        print(f"Steering: {steer:.2f} | Throttle: {throttle:.2f} | Brake: {brake:.2f} | Speed: {speed} | RPM: {rpm}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return {"speed": speed, "rpm": rpm}

if __name__ == "__main__":
    threading.Thread(target=controller_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)