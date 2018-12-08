## AD_assignment
    20163103 김현곤
    20133218 류정주
    
    최종 발표 동영상 링크
    https://drive.google.com/open?id=1KnSS000NvejFT-XfrlENPENWZt7lHF-h

## 0. 수행한 미션에 관하여
    1) 필수 미션으로 T자 주차를 수행하였습니다.
    
    2) 자율 미션 1로 또다른 필수 미션인 RGB 일시정차를 수행하였습니다.
    
    3) 자율 미션 2로 차량 간 추월과 양보를 수행하였습니다.

## 1. 미션 수립과 실제 수행에 관하여
    1) 원 계획은 T자 주차, 제한속도, 추월의 3가지 미션을 수행할 계획이었으나, 차량의 연산능력과 구조적 한계에 따라 제한속도 개념 대신 빨간불에서 3초간 정지하는 미션으로 변경 수행하였습니다.

    2) 변경된 미션과 기존 미션의 소프트웨어적 구현 난이도는 같은 수준입니다.

    3) 아울러 트랙의 미션수행을 위한 장치들을 차량이 제대로 감지하지 못하는 상황이 굉장히 자주 발생함에 따라 트랙의 직선주로를 늘리고 감지조건들의 위치를 이동조치하였습니다.

    4) 미션에 사용한 차량과 소프트웨어가 두개인 만큼 본 마크다운에서는 각 코드의 공통된 요소에 대해서 먼저 설명하고, 양보 차량과 추월 차량의 특화 코드를 따로 기술합니다.

## 2. 공통 요소에 관하여
    # 출발 전 차량세팅
    self.car.steering.center_alignment()
    time.sleep(1)
    self.car.accelerator.ready()
    self.car.accelerator.stop()
    
    1) 출발 전 차량의 조향축과 추진모터를 초기화합니다.


    # do-while의 구조를 취하기 위해 while True 사용
    while True:
        # 라인감지 시작
        detector = self.car.line_detector.read_digital()
        ultrasonic = self.car.distance_detector.get_distance()

    1) do-while 구조를 취하기 위하여 while True를 사용하여 센서값들을 호출합니다.


    # 라인이 정중앙에 있을 때 직진
    if detector == [0, 0, 1, 0, 0]:
        self.car.steering.center_alignment()
    # 좌회전을 위한 코드
    elif detector == [0, 1, 1, 0, 0]:
        self.car.steering.turn_left(75)
    elif detector == [0, 1, 0, 0, 0]:
        self.car.steering.turn_left(70)
    elif detector == [1, 1, 0, 0, 0]:
        self.car.steering.turn_left(60)
    elif detector == [1, 0, 0, 0, 0]:
        self.car.steering.turn_left(55)

    # 우회전을 위한 코드
    elif detector == [0, 0, 1, 1, 0]:
        self.car.steering.turn_right(105)
    elif detector == [0, 0, 0, 1, 0]:
        self.car.steering.turn_right(110)
    elif detector == [0, 0, 0, 1, 1]:
        self.car.steering.turn_right(120)
    elif detector == [0, 0, 0, 0, 1]:
        self.car.steering.turn_right(125)

    # 값이 튀면 현재 경로 유지
    else: continue

    1) 라인트레이싱을 수행하기 위한 기본 코드입니다.
    2) Step-Turn은 15, 20, 30, 35도 총 4단계로 되어 있습니다.


    # 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
    elif detector == [0, 0, 0, 0, 0]:
        self.car.accelerator.stop()
        while True:
            self.car.steering.turn_left(55)
            time.sleep(0.1)
            self.car.accelerator.go_backward(60)
            detector = self.car.line_detector.read_digital()
            if detector[4] == 1 or detector[3] == 1:
                self.car.accelerator.stop()
                self.car.steering.turn_right(130)
                time.sleep(0.1)
                self.car.accelerator.go_forward(50)
                break
    
    1) 라인이 사라지면 반대방향으로 조향 후 후진하여 라인이 감지될 수 있도록 합니다.

## 3. 양보 차량 특화 코드에 관하여
    # 초음파센서가 앞차량을 감지
    if 10 < ultrasonic < 35:
        # 앞차량을 감지했다고 최종 판단하면 정지
        self.car.accelerator.stop()
        while True:
            ultrasonic = self.car.distance_detector.get_distance()
            if ultrasonic > 35:
                break
    
    1) 초음파센서를 활용, 추월 차량이 감지되면 그자리에 정차합니다.


    # 추월구간시작(1번, 4번 센서에 라인이 동시감지)이 감지되었을 때 양보
    elif detector[0] == 1 and detector[4] == 1:
        self.car.steering.center_alignment()
        time.sleep(1.5)
        self.car.accelerator.stop()
        while True:
            ultrasonic = self.car.distance_detector.get_distance()
            if 10 < ultrasonic < 50:
                break
    
    1) 추월구간이 감지되면 일정 거리를 더 직진한 후 그자리에 정차합니다.
    2) 정차 후 추월차량이 본인을 앞질러갔음을 확인하고 뒤를 따라 출발합니다.

## 4. 추월 차량 특화 코드에 관하여
    target_distance = 30
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.OUT)
    rgb = self.car.color_getter.get_raw_data()
    GPIO.output(31, False)

    1) target_distance = 양보 차량을 만났을 때 유지할 안전거리입니다.
    2) GPIO관련 소스 = 추월시 사용할 LED를 제어합니다.
    3) rgb = RGB센서 값을 불러옵니다.


    # 초음파센서가 앞차량을 감지
    if 10 < ultrasonic < 40:
        # 앞차량을 감지했다고 최종 판단하면 속도 조절 시작
        if ultrasonic < target_distance:
            speed -= 5
        elif ultrasonic > target_distance:
            speed += 5
        elif ultrasonic < 20:
            self.car.accelerator.stop()
            while True:
                ultrasonic = self.car.distance_detector.get_distance()
                if ultrasonic > 30:
                    break
    
    # 거리가 35보다 멀어지면 정상속도로 가속
    if ultrasonic > 40:
        speed = 60

    # 속도가 30 미만으로 떨어지면 모터 작동에 문제가 생기므로 최소값 고정
    if speed < 30:
        speed = 30
    if speed > 60:
        speed = 60
    
    1) 앞차량을 감지하고 target_distance에 따라 감속/가속을 통해 거리를 유지합니다.
    2) 만약 그 거리가 20보다 가까우면 충돌할 가능성이 있으므로 일시 정차합니다.
    3) 단, 거리가 35보다 멀어지면 60으로 재가속합니다.
    4) 단, 차량의 최저/최고 속도는 30과 60으로 각각 제한합니다.


    # RGB Red감지시 3초 정지
    if rgb[0] > 250 and rgb[1] < 200 and rgb[2] < 200:
        self.car.accelerator.stop()
        self.car.steering.center_alignment()
        time.sleep(3)
        self.car.accelerator.go_forward(50)
        time.sleep(0.3)

    1)  RED값을 감지하면 차량을 3초간 정지시키는 미션을 수행합니다.


    # T자 후진주차 코드
    elif detector[0] == 0 and detector[2] == 1 and detector[4] == 1:
        while True:
            detector = self.car.line_detector.read_digital()
            if detector[2] == 1 and detector[4] == 1:
                continue
            elif detector[0] == 0 and detector[4] == 0 and detector[2] == 1:
                # 최적의 주차 속도/조향 산출
                self.car.accelerator.go_forward(40)
                time.sleep(0.3)
                self.car.steering.turn_left(60)
                time.sleep(0.6)
                self.car.accelerator.stop()
                self.car.steering.turn_right(120)
                self.car.accelerator.go_backward(40)
                time.sleep(1.8)
                self.car.steering.center_alignment()
                time.sleep(0.25)
                self.car.accelerator.stop()
                time.sleep(3)
                self.car.steering.turn_right(125)
                time.sleep(0.2)
                self.car.accelerator.go_forward(40)
                time.sleep(2.5)
                
            else: break
    
    1) T자 후진주차를 수행할 조건을 감지(0번에는 0, 2번/4번에 1이 감지)하면 최적의 조향각을 통해 정확히 주차합니다.


    # 추월구간시작(0번, 4번 센서에 라인이 동시감지)이 감지되었을 때 추월
    elif detector[0] == 1 and detector[3] == 1 and detector[4] == 1:
        if ultrasonic < 30:
            self.car.steering.turn_right(130)
            self.car.accelerator.go_forward(50)
            GPIO.output(31, True)
            self.car.steering.turn_right(130)
            time.sleep(0.9)
            self.car.steering.turn_left(50)
            while True:
                detector = self.car.line_detector.read_digital()
                if detector[3] == 1:
                    GPIO.output(31, False)
                    self.car.steering.turn_right(130)
                    time.sleep(0.4)
                    break
        else:
            continue
    
    1) 추월구간에 진입하고, 앞 차량과의 거리가 30미만일 경우 추월을 시도합니다.
    2) 우측으로 충분히 비켜서 정차해있는 앞차량을 넉넉히 피해 돌아갑니다.
    3) 추월과정에서 LED를 점등하여 추월사실을 알립니다.

## 5. 프로젝트 수행에서 어려웠던 점
    1) 기존 계획대로 제작이 힘들었기에 시험과정에서 트랙구조와 차량의 구조를 계속해서 변경해야했기에 시간이 오래 걸렸습니다.
        - 직진주로의 길이를 연장해야했고, 추월구간과 RGB구간의 크기와 길이도 수시로 변경해서 최종 트랙을 완성했습니다.
        
    2) 사용해야할 부품이 증가함에 따라 발생한 라즈베리파이 전류부족으로 연산이 제대로 진행되지 않는 경우가 많았고, 때문에 코드로직에 오류가 없음에도 예상과 다른 움직임을 보여주는 경우가 많았습니다.
        - 라즈베리파이에 원활한 전류를 공급하기 위하여 LED, 5방향추적센서, 초음파센서의 전원회로를 라즈베리파이에서 PWM보드의 남는 5+핀으로 변경하였습니다.
        
    3) RGB센서의 고정 방식과 위치가 애매하여 많은 고민이 있었습니다.
        - 차량키트의 미사용 플레이트와 케이블타이를 이용하여 5방향 추적센서 전면에 부착하였으며, 하단을 보도록 부착되어 RGB값이 크게 튀지않고 정확히 원하는 값을 계산하여 사용할 수 있었습니다.
        
    4) 추월구간에서 얇은 장애물이 아니라 실제 자동차를 회피하다보니 추월 동작 중 차량이 서로 충돌하는 일이 잦았습니다.
        - 추후 본선 진입에 다소 어려움이 있더라도 최대한 크게 회피하는 것을 선택했습니다.
        
    5) T자형 주차 상황에서 센서를 사용할 수 없이 감으로만 최적의 후면주차 조작을 찾아내는 과정이 힘들었습니다.
        - 실제 차량을 운전해온 경험을 바탕으로 실제 차량의 주차와 같은 방식으로 조작하였습니다.
