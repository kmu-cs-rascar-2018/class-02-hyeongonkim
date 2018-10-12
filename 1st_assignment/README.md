## 1st_assignment_main

## 1. 초음파센서 이니셜라이징에 큐를 사용하기 위해 deque를 import하여 사용하였습니다.
    from collections import deque

## 2. 전후진 조건에서 정확한 타겟거리 정지를 위해 차량이 출발하기 전 본인의 정확한 거리를 측정한 뒤 출발하도록 하였습니다.
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

    1) 초음파센서 이니셜라이징 값은 센서의 신뢰도를 감안하여 10cm ~ 70cm까지만 유의미한 값으로 인지합니다.(초과 값은 모두 70으로 저장)
    2) 전진하며 0.1초 간격으로 현재 초음파센서 측정 값을 불러오고, 그 값이 0.1초 전에 측정한 이전 값보다 커지거나 20이상 작아지면 튀는 값으로 판단하고 무시합니다. 20으로 둔 이유는 차량의 최대 속도를 감안했을 때 정지해있는 장애물에 0.3초(2회 튀는 값이 발생시) 동안 20cm이상 가까워질 수 없다고 판단했기 때문입니다.

## 3. 브레이크 시작 시점을 연산하기 위하여 속도와 타겟거리를 입력받는 함수를 만들었습니다.
    def brake_distance(speed, target):
        brake = target + (speed + 5) * 0.3
        return brake

    1) 각각의 속도당 10회 반복 실시한 결과를 기록 후 수식을 세웠습니다.
    2) 타겟거리 + (전진속도 + 5) * 0.3 값을 리턴합니다.

## 4. 전진과 후진코드는 함수화하여 속도와 타겟거리(전진) 또는 시간(후진)을 입력하면 호출하여 사용할 수 있습니다.
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

    1) 0.1초 간격으로 현재 초음파센서 측정값을 계산하고, 유의미한 값일 경우 사용합니다.

    def back_straight(speed, move_time):
        rear_wheels_drive.backward_with_speed(speed)
        time.sleep(move_time)
        rear_wheels_drive.stop()

    1) 시간만큼 후진합니다.