import random
import turtle, time
import math


class PongZone:
    def __init__(self):
        self.ball_speed = 5
        self.bullet_speed = 5
        self.paddle_speed = 30
        self.reward = 0

        self.wn = turtle.Screen()
        self.wn.title('Pong AI')
        self.wn.bgcolor("black")
        self.wn.setup(width=800, height=600)

        self.wn.tracer(0)

        self.score_a = 0
        self.score_b = 0

        self.flag_a_shoot = 0
        self.flag_b_shoot = 0


        self.paddle_a = turtle.Turtle()
        self.paddle_a.speed(0)
        self.paddle_a.shape("square")
        self.paddle_a.color("blue")
        self.paddle_a.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle_a.penup()

        self.paddle_b = turtle.Turtle()
        self.paddle_b.speed(0)
        self.paddle_b.shape("square")
        self.paddle_b.color("red")
        self.paddle_b.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle_b.penup()

        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("square")
        self.ball.color("white")
        self.ball.shapesize(stretch_wid=1, stretch_len=1)
        self.ball.penup()
        self.ball.dx = self.ball_speed
        self.ball.dy = self.ball_speed

        self.bullet_a = turtle.Turtle()
        self.bullet_a.speed(0)
        self.bullet_a.shape("square")
        self.bullet_a.color("blue")
        self.bullet_a.shapesize(stretch_wid=1, stretch_len=2)
        self.bullet_a.penup()
        self.bullet_a.dx = 0
        self.bullet_a.goto(0, 320)

        self.bullet_b = turtle.Turtle()
        self.bullet_b.speed(0)
        self.bullet_b.shape("square")
        self.bullet_b.color("red")
        self.bullet_b.shapesize(stretch_wid=1, stretch_len=2)
        self.bullet_b.penup()
        self.bullet_b.dx = 0
        self.bullet_b.goto(0, 320)

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Player A,Player B", align="center")

        self.wn.listen()
        self.wn.onkeypress(self.paddle_a_up, "w")
        self.wn.onkeypress(self.paddle_a_down, "s")
        self.wn.onkeypress(self.paddle_b_up, "Up")
        self.wn.onkeypress(self.paddle_b_down, "Down")
        self.reset()

    def reset(self):

        self.ball_speed = 1
        self.paddle_speed = 30
        self.reward = 0
        self.ball.goto(0, 0)
        self.paddle_b.goto(350, 0)
        self.paddle_a.goto(-350, 0)

        angle_degree = int(random.uniform(-45, 45)) % 360
        cont = 3
        self.ball.dx = random.choice([-1, 1]) * (cont * math.cos(angle_degree * math.pi / 180)).__round__(2)
        self.ball.dy = (cont * math.sin(angle_degree * math.pi / 180)).__round__(2)

        return self.get_state()

    def paddle_a_up(self):
        ay = self.paddle_a.ycor()
        if ay < 270:
            ay = ay + self.paddle_speed
            self.paddle_a.sety(ay)

    def paddle_a_down(self):
        ay = self.paddle_a.ycor()
        if ay > -270:
            ay = ay - self.paddle_speed
            self.paddle_a.sety(ay)

    def paddle_b_up(self):
        by = self.paddle_b.ycor()
        if by < 270:
            by = by + self.paddle_speed
            self.paddle_b.sety(by)

    def paddle_b_down(self):
        by = self.paddle_b.ycor()
        if by > -270:
            by = by - self.paddle_speed
            self.paddle_b.sety(by)


    def paddle_a_shoot(self):
        if self.flag_a_shoot == 0:
            self.bullet_a.goto(-320, self.paddle_a.ycor())
            self.flag_a_shoot = 1
    def move_bullet_a(self):
        #self.bullet_a.xcor() #+= self.bullet_speed
        self.bullet_a.setx(self.bullet_a.xcor() + self.bullet_speed)


    def paddle_b_shoot(self):
        if self.flag_b_shoot == 0:
            self.bullet_b.goto(320, self.paddle_b.ycor())
            self.flag_b_shoot = 1

    def move_bullet_b(self):
        #self.bullet_b.dx -= self.bullet_speed
        self.bullet_b.setx(self.bullet_b.xcor() - self.bullet_speed)

    def newpan(self):
        self.pen.write(str(self.score_a) + " : " + str(self.score_b), font=("Arial", 30, "normal"), align="center")

    def render(self, action_a=None, action_b=None):

        # For Player A
        if action_a == 0:
            self.paddle_a_up()
        if action_a == 1:
            self.paddle_a_down()
        if action_a == 2:
            self.paddle_a_shoot()

        # For Player B
        if action_b == 0:
            self.paddle_b_up()
        if action_b == 1:
            self.paddle_b_down()
        if action_a == 2:
            self.paddle_b_shoot()

        if self.flag_a_shoot == 1:
            self.move_bullet_a()
        if self.flag_b_shoot == 1:
            self.move_bullet_b()

        done = False
        reward_a = 0
        reward_b = 0

        self.wn.update()
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        if self.ball.ycor() > 290 or self.ball.ycor() < -290:
            self.ball.dy = self.ball.dy * -1


        # If Player B misses the ball
        if self.ball.xcor() > 390:
            done = True
            reward_a = 100
            reward_b = -100
            self.ball.goto(0, 0)
            self.score_a += 1
            self.pen.clear()

        # If Player A misses the ball
        if self.ball.xcor() < -390:
            done = True
            reward_a = -100
            reward_b = 100
            self.ball.goto(0, 0)
            self.score_b += 1
            self.pen.clear()

        if (self.ball.xcor() > 340 and self.ball.xcor() < 350
             and (self.ball.ycor() < self.paddle_b.ycor() + 40)
             and (self.ball.ycor() > self.paddle_b.ycor() - 40)):
            self.ball.dx = self.ball.dx * -1
            self.ball_speed = self.ball_speed + 0.05
            reward_b = 1000

        if (self.ball.xcor() < -340 and self.ball.xcor() > -350
             and (self.ball.ycor() < self.paddle_a.ycor() + 40)
             and (self.ball.ycor() > self.paddle_a.ycor() - 40)):
            self.ball.dx = self.ball.dx * -1
            self.ball_speed = self.ball_speed + 0.05
            reward_a = 1000


        if (self.bullet_a.xcor() > 340 and self.bullet_a.xcor() < 350
                and self.bullet_a.ycor() < self.paddle_b.ycor() + 40
                and self.bullet_a.ycor() > self.paddle_b.ycor() - 40):
            self.score_a += 1
            self.bullet_a.goto(0, 320)
            self.flag_a_shoot = 0
            reward_a = 100
            reward_b = -100
            self.pen.clear()


        if (self.bullet_b.xcor() < -340 and self.bullet_b.xcor() > -350
                and self.bullet_b.ycor() < self.paddle_a.ycor() + 40
                and self.bullet_b.ycor() > self.paddle_a.ycor() - 40):
            self.score_b += 1
            self.bullet_b.goto(0, 320)
            self.flag_b_shoot = 0
            reward_b = 100
            reward_a = -100
            self.pen.clear()

        if (self.bullet_a.xcor() > 390):# or self.bullet_a.xcor() > 390):
            self.bullet_a.goto(0, 320)
            self.flag_a_shoot = 0
            self.pen.clear()

        if (self.bullet_b.xcor() < -390):# or self.bullet_b.xcor() > 390):
            self.bullet_b.goto(0, 320)
            self.flag_b_shoot = 0
            self.pen.clear()

        self.newpan()
        return self.get_state(), reward_a, reward_b, done

    def get_state(self):
        tile = 100
        ax, ay = self.paddle_a.xcor() // tile, self.paddle_a.ycor() // tile
        bx, by = self.paddle_b.xcor() // tile, self.paddle_b.ycor() // tile
        ball_x, ball_y = self.ball.xcor() // tile, self.ball.ycor() // tile
        bullet_a_x, bullet_a_y = self.bullet_a.xcor() // tile, self.bullet_a.ycor() // tile
        bullet_b_x, bullet_b_y = self.bullet_b.xcor() // tile, self.bullet_b.ycor() // tile
        return (ax, ay, bx, by, int(ball_x), int(ball_y), bullet_a_x, bullet_a_y, bullet_b_x, bullet_b_y)
