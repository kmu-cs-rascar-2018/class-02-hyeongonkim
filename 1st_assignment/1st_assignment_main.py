#########################################################################
# Date: 2018/08/09
# file name: 1st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################


# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
import time
from collections import deque

# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking as Tracking_Sensor

# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB as RGB_Sensor

# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Ultrasonic as Ultrasonic_Sensor

# =======================================================================
# import ALL method in the rear/front Motor Module
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)


class Car(object):

    def __init__(self):
        self.moduleInitialize()

    def drive_parking(self):
        # front wheels center allignment
        self.front_steering.turn_straight()

        # power down both wheels
        self.rear_wheels_drive.stop()
        self.rear_wheels_drive.power_down()

    # =======================================================================
    # 1ST_ASSIGNMENT_CODE
    # Complete the code to perform First Assignment
    # =======================================================================
    def assignment_main(self):
        # Implement the assignment code here.
        distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)
        front_steering = front_wheels.Front_Wheels()
        rear_wheels_drive = rear_wheels.Rear_Wheels()


        # ready for move
        front_steering.turn_straight()
        time.sleep(1)
        rear_wheels_drive.ready()
        rear_wheels_drive.stop()


        # 전진 직전 현재 위치에서 정확한 거리값을 연산, 단 70cm 이상일 경우 70을 리턴
        def ultrasonic_init():
            a = deque([])
            i = 0
            final = 0
            while len(a) <= 3:
                dis = distance_detector.get_distance()
                if 10 < dis < 70 and dis != -1:
                    a.append(dis)
                    time.sleep(0.1)
                    next = distance_detector.get_distance()
                    if abs(a[i] - next) > 10:
                        del a[i]
                    else:
                        a.append(next)
                        i = i + 1
                elif dis >= 70 or dis == -1:
                    a.append(70)
                    i = i + 1
                time.sleep(0.1)

            for i in range(3):
                final = final + a[i]
            final = final / 3
            return final


        # 속도와 타겟거리를 입력하여 실제 브레이크 시작 위치를 계산
        def brake_distance(speed, target):
            brake = target + (speed + 5) * 0.3
            return brake


        # 속도와 타겟거리를 입력받아 전진
        def go_straight(speed, stop_target):
            final = ultrasonic_init()
            rear_wheels_drive.forward_with_speed(speed)
            while (1):
                nowdis = distance_detector.get_distance()
                if nowdis < final and abs(nowdis - final) < 20:
                    final = nowdis
                    if nowdis < stop_target:
                        rear_wheels_drive.stop()
                        break
                time.sleep(0.1)


        # 속도와 시간을 입력받아 후진
        def back_straight(speed, move_time):
            rear_wheels_drive.backward_with_speed(speed)
            time.sleep(move_time)
            rear_wheels_drive.stop()


        # speed 30 test
        go_straight(30, brake_distance(30, 15))
        time.sleep(1)
        back_straight(30, 4)
        time.sleep(1)


        # speed 50 test
        go_straight(50, brake_distance(50, 20))
        time.sleep(1)
        back_straight(50, 4)
        time.sleep(1)


        # speed 70 test
        go_straight(70, brake_distance(70, 25))
        time.sleep(1)
        back_straight(70, 4)

        rear_wheels_drive.power_down()

        pass

    def moduleInitialize(self):
        try:
            # ================================================================
            # ULTRASONIC MODULE DRIVER INITIALIZE
            # ================================================================
            self.distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)

            # ================================================================
            # TRACKING MODULE DRIVER INITIALIZE
            # ================================================================
            self.line_detector = Tracking_Sensor.SEN040134_Tracking([16, 18, 22, 40, 32])

            # ================================================================
            # RGB MODULE DRIVER INITIALIZE
            # ================================================================
            # self.color_getter = RGB_Sensor.TCS34725()

            # ================================================================
            # FRONT WHEEL DRIVER SETUP
            # ================================================================
            self.front_steering = front_wheels.Front_Wheels(db='config')
            self.front_steering.ready()

            # ================================================================
            # REAR WHEEL DRIVER SETUP
            # ================================================================
            self.rear_wheels_drive = rear_wheels.Rear_Wheels(db='config')
            self.rear_wheels_drive.ready()

            # ================================================================
            # SET LIMIT OF TURNING DEGREE
            # ===============================================================
            self.front_steering.turning_max = 35

            # ================================================================
            # SET FRONT WHEEL CENTOR ALLIGNMENT
            # ================================================================
            self.front_steering.turn_straight()

            # ================================================================
            # DISABLE RGB MODULE INTERRUPTION
            # ================================================================
            # self.color_getter.set_interrupt(False)

        except:
            print("MODULE INITIALIZE ERROR")
            print("CONTACT TO Kookmin Univ. Teaching Assistant")


if __name__ == "__main__":
    try:
        car = Car()
        car.assignment_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        car.drive_parking()
