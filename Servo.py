import RPi.GPIO as GPIO
import time


def servo_run():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    p = GPIO.PWM(12, 50)
    STEP=15
    def angle_to_duty_cycle(angle=0):
        duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
        return duty_cycle
    
    p.start(0)
    try:
        print('[INFO]Motion 1 activate')
        dc = angle_to_duty_cycle(0)
        p.ChangeDutyCycle(dc)
        time.sleep(1)
        print('[INFO]Motion 2 activate')
        dc = angle_to_duty_cycle(100)
        p.ChangeDutyCycle(dc)
        time.sleep(1)
        print('[INFO]Back original angle activate')
        dc = angle_to_duty_cycle(0)
        p.ChangeDutyCycle(dc)
        time.sleep(1)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
