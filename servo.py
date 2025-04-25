import RPi.GPIO as GPIO
import time
import threading

SERVO_PIN = 12  # BCM pin number
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

servo_lock = threading.Lock()
last_action_time = 0

def angle_to_duty_cycle(angle):
    return 2.5 + (angle + 90) * (10 / 180)

def perform_servo_action(bean_type):
    global last_action_time

    with servo_lock:
        if time.time() - last_action_time < 6:
            return
        last_action_time = time.time()

        if bean_type == 'trinitario':
            pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(6)
            pwm.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)

        elif bean_type == 'criollo':
            pwm.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(6)

        elif bean_type == 'forastero':
            pwm.ChangeDutyCycle(angle_to_duty_cycle(-90))
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(6)
            pwm.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)

def cleanup():
    pwm.stop()
    GPIO.cleanup()
