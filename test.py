import turtle as t
import random

# 게임상태변수
playing = False
score = 0

def start():
    global playing
    playing = True
    print('게임상태 변경 ', playing)

    # 게임 시작
    play()

def turn_up():
    t.setheading(90)

def turn_down():
    t.setheading(270)

def turn_left():
    t.setheading(180)

def turn_right():
    t.setheading(0)    

def play():

    global playing
    global score

    t.forward(10)
    
    # 악당 거북이의 움직임
    t_te_angle = te.towards(t.position())
    te.setheading(t_te_angle)
    te.forward(2+score)

    # 먹이 먹은거 처리
    if t.distance(ts) < 30:        
        # 점수 증가
        score = score + 1
        print('먹이를 먹었음!! score:', score)
        # 먹이 이동
        ts.goto(random.randint(-250, 250), random.randint(-250, 250))

    # 잡힌거 처리
    if t.distance(te) < 30:
        print('악당에게 잡혔음!!')
        # 게임 종료
        playing = False
        print('게임상태 변경 ', playing)

    if playing == True:
        t.ontimer(play, 200)

# 배경 설정
t.bgcolor('orange')

# 플레이어 거북이 설정
t.shape('turtle')
t.up()
t.speed(0)
t.color('white')

# 악당 거북이 설정
te = t.Turtle()
te.shape('turtle')
te.up()
te.speed(0)
te.color('red')
te.goto(0, 200)

# 먹이 설정
ts = t.Turtle()
ts.shape('circle')
ts.up()
ts.speed(0)
ts.color('green')
ts.goto(0, -200)

# 플레이어 거북이 키 바인딩
t.onkeypress(turn_up, 'Up')
t.onkeypress(turn_down, 'Down')
t.onkeypress(turn_left, 'Left')
t.onkeypress(turn_right, 'Right')
t.onkeypress(start, "space")



t.listen()
t.mainloop()