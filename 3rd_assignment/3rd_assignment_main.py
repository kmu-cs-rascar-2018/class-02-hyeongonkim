#########################################################################
# Date: 2018/10/02
# file name: 2nd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 2ND_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def car_startup(self):
        # 출발 전 차량세팅
        self.car.steering.center_alignment()
        time.sleep(1)
        self.car.accelerator.ready()
        self.car.accelerator.stop()

        # do-while의 구조를 취하기 위해 while True 사용
        while True:
            # 라인감지 시작
            detector = self.car.line_detector.read_digital()
            ultrasonic = self.car.distance_detector.get_distance()

            determine_left = True
            verylittle_turn = 5
            little_turn = 10
            midium_turn = 30
            heavy_turn = 35

            if ultrasonic > 30 or ultrasonic == -1:
                continue
            else:
                # 장애물 회피 코드

            # 라인이 정중앙에 있을 때 직진
            if detector == [0, 0, 1, 0, 0]:
                self.car.steering.center_alignment()
                self.car.accelerator.go_forward(100)

            # 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
            elif detector == [0, 0, 0, 0, 0] or detector == [1, 1, 1, 1, 1]:
                self.car.accelerator.stop()
                if determine_left == True:
                    self.car.steering.turn_right(125)
                    self.car.accelerator.go_backward(50)
                elif determine_left == False:
                    self.car.steering.turn_left(55)
                    self.car.accelerator.go_backward(50)

            # 좌회전을 위한 코드
            elif detector[3] == 0 and detector[4] == 0:
                if detector[2] == 1 and detector[1] == 1:
                    angle = verylittle_turn
                    speed = 100
                elif detector[2] == 0:
                    if detector[1] == 1:
                        if detector[0] == 0:
                            angle = little_turn
                            speed = 100
                        elif detector[0] == 1:
                            angle = midium_turn
                            speed = 60
                    elif detector[1] == 0:
                        if detector[0] == 1:
                            angle = heavy_turn
                            speed = 30
                self.car.accelerator.go_forward(speed)
                self.car.steering.turn_left(90 - angle)
                determine_left = True

            # 우회전을 위한 코드
            elif detector[0] == 0 and detector[1] == 0:
                if detector[2] == 1 and detector[3] == 1:
                    angle = verylittle_turn
                    speed = 100
                elif detector[2] == 0:
                    if detector[3] == 1:
                        if detector[4] == 0:
                            angle = little_turn
                            speed = 100
                        elif detector[4] == 1:
                            angle = midium_turn
                            speed = 60
                    elif detector[3] == 0:
                        if detector[4] == 1:
                            angle = heavy_turn
                            speed = 30
                self.car.accelerator.go_forward(speed)
                self.car.steering.turn_right(90 + angle)
                determine_left = False

            # 그 외 값이 튀었을 경우 현재 주행경로를 유지
            else: continue

        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()