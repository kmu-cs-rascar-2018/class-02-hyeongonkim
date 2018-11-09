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
        lap_cnt = 0
        obstacle_detect = False
        self.car.steering.turning_max = 40
        stopback_time = 0
        lastultrasonic_time = 0
        ultrasonic = -1

        strat_time = time.time()

        # do-while의 구조를 취하기 위해 while True 사용
        while True:
            # 라인감지 시작
            detector = self.car.line_detector.read_digital()
            nowtime = time.time()
            ultrasonic_ontime = nowtime - lastultrasonic_time
            ultrasonic = 0
            if ultrasonic_ontime > 6:
                ultrasonic = self.car.distance_detector.get_distance()

            determine_left = True
            verylittle_turn = 10
            little_turn = 25
            medium_turn = 30
            heavy_turn = 40

            # 초음파 센서가 장애물을 감지하고 튀는 값을 필터링
            if 10 < ultrasonic < 30 and obstacle_detect == False:
                n_ultrasonic = self.car.distance_detector.get_distance()
                while n_ultrasonic == -1 or n_ultrasonic > 30:
                    n_ultrasonic = self.car.distance_detector.get_distance()
                distance = (ultrasonic + n_ultrasonic) / 2
                # 장애물을 감지했다고 최종 판단하고 좌측으로 회피 조향
                if distance < 30:
                    print("obstacle detected")
                    obstacle_detect == True
                    self.car.accelerator.go_forward(70)
                    self.car.steering.turn_left(50)
                    time.sleep(0.6)
                    self.car.steering.center_alignment()
                    while True:
                        self.car.accelerator.go_forward(70)
                        detector = self.car.line_detector.read_digital()
                        if detector[0] == 1:
                            print("guideline detected")
                            self.car.accelerator.go_forward(70)
                            self.car.steering.turn_right(130)
                            time.sleep(0.7)
                            self.car.steering.center_alignment()
                            break
                    while True:
                        detector = self.car.line_detector.read_digital()
                        if detector[1] == 1:
                            print("on main street")
                            lastultrasonic_time = time.time()
                            obstacle_detect = False
                            self.car.steering.turn_left(50)
                            time.sleep(0.4)
                            break

            # 라인이 정중앙에 있을 때 직진
            if detector == [0, 0, 1, 0, 0]:
                self.car.steering.center_alignment()
                self.car.accelerator.go_forward(70)

            # 정지조건이 감지되었을 때 lap_cnt를 증가시키고, 2랩 완주 후 정지
            elif detector[0] == 1 and detector[3] == 1:
                lapcnt_time = time.time()
                if 2 > lapcnt_time - stopback_time > 0.3:
                    lap_cnt += 1
                    print("+1 lap")
                if lap_cnt == 2:
                    end_time = time.time()
                    self.car.drive_parking()
                    print("완주시간 : ", end_time - strat_time)
                    break
                while detector[0] == 1 and detector[3] == 1:
                    detector = self.car.line_detector.read_digital()

            # 장애물을 감지하지 않은 상황에서 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
            elif detector == [0, 0, 0, 0, 0] and obstacle_detect == False:
                self.car.accelerator.stop()
                while determine_left == True:
                    self.car.steering.turn_right(130)
                    self.car.accelerator.go_backward(50)
                    detector = self.car.line_detector.read_digital()
                    if detector[2] == 1:
                        stopback_time = time.time()
                        break
                while determine_left == False:
                    self.car.steering.turn_left(50)
                    self.car.accelerator.go_backward(50)
                    detector = self.car.line_detector.read_digital()
                    if detector[2] == 1:
                        stopback_time = time.time()
                        break

            # 좌회전을 위한 코드
            elif detector[3] == 0 and detector[4] == 0:
                if detector[2] == 1 and detector[1] == 1:
                    angle = verylittle_turn
                    speed = 60
                elif detector[2] == 0:
                    if detector[1] == 1:
                        if detector[0] == 0:
                            angle = little_turn
                            speed = 50
                        elif detector[0] == 1:
                            angle = medium_turn
                            speed = 45
                    elif detector[1] == 0:
                        if detector[0] == 1:
                            angle = heavy_turn
                            speed = 40
                self.car.accelerator.go_forward(speed)
                self.car.steering.turn_left(90 - angle)
                determine_left = True

            # 우회전을 위한 코드
            elif detector[0] == 0 and detector[1] == 0:
                if detector[2] == 1 and detector[3] == 1:
                    angle = verylittle_turn
                    speed = 60
                elif detector[2] == 0:
                    if detector[3] == 1:
                        if detector[4] == 0:
                            angle = little_turn
                            speed = 50
                        elif detector[4] == 1:
                            angle = medium_turn
                            speed = 45
                    elif detector[3] == 0:
                        if detector[4] == 1:
                            angle = heavy_turn
                            speed = 40
                self.car.accelerator.go_forward(speed)
                self.car.steering.turn_right(90 + angle)
                determine_left = False
            
            # 값이 튀면 현재 경로 유지
            else:
                continue

        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()