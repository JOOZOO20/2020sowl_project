import pygame
import random
from time import sleep

main_screen_width=480
main_screen_height=800

black=(0,0,0)
white=(255,255,255)
gray=(150,150,150)
red=(255,0,0)

class Car:
    image_car=['RacingCar02.png','RacingCar03.png','RacingCar04.png',\
               'RacingCar05.png','RacingCar06.png','RacingCar07.png','RacingCar08.png',\
               'RacingCar09.png','RacingCar10.png','RacingCar11.png','RacingCar12.png',\
               'RacingCar13.png','RacingCar14.png','RacingCar15.png','RacingCar16.png',\
               'RacingCar17.png','RacingCar18.png','RacingCar26.png']

    
    def __init__(self,x=0,y=0,dx=0,dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx #direction x ==dx
        self.dy = dy #direction y == dy

    def load_image(self):#이미지로드
        self.image = pygame.image.load(random.choice(self.image_car))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]


    def draw_image(self): #이미지 진짜 그리기
        screen.blit(self.image, [self.x, self.y])

    def move_x(self): #x움직이기
        self.x += self.dx

    def move_y(self): #y움직이기
        self.y += self.dy

    def check_out_of_screen(self): #오류가난다면 if의 self.x+self.width
        if self.x + self.width > main_screen_width or self.x < 0:
            self.x -= self.dx

    def check_crash(self, car):
        if (self.x + self.width > car.x) and (self.x < car.x + car.width) and (self.y < car.y + car.height) and (self.y + self.height > car.width):
            return True
        else:
            return False

def draw_main_menu():
    draw_x = (main_screen_width / 2) - 200
    draw_y = main_screen_height / 2 
    image_intro = pygame.image.load('Pycar.png')
    screen.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("Pycar: Racing Car Game", True, black)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render("Score: " +str(score), True, white)
    screen.blit(text_score, [draw_x, draw_y + 70])
    text_start = font_30.render("Press space key and restart!", True, red)
    screen.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()


def draw_score():
    font_30 = pygame.font.SysFont("None", 30, True, False)
    text_score = font_30.render("Score: "+ str(score), True, black)
    screen.blit(text_score, [15,15])



if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((main_screen_width, main_screen_height))
    pygame.display.set_caption("Please, Don't Bump into Other Car")
    clock = pygame.time.Clock()

    pygame.mixer.music.load("race.wav")
    sound_crash = pygame.mixer.Sound('crash.wav')
    sound_engine = pygame.mixer.Sound('engine.wav')

    player = Car(main_screen_width, (main_screen_height - 150),0,0)
    player.load_image()

    cars = []
    car_count = 3 #방해자동차 갯수(==사용자와 함께 달리는 자동차 갯수)
    for i in range(car_count):
        x = random.randrange(0, main_screen_width-55)
        y = random.randrange(-150,-50)
        car = Car(x,y,0,random.randint(5,10)) #5<=direction<=10, 방해자동차의 속도 diffrent range
        car.load_image()
        cars.append(car)

    lanes = [] #차선
    lane_width=10
    lane_height = 80
    lane_margin = 20 #차선 간격
    lane_count = 20 #차선은 20개가 계속moving
    lane_x = (main_screen_width - lane_width) / 2
    lane_y = -10
    for i in range(lane_count): #lane_count갯수만큼 만들어쥼
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin


    #충돌 재기회 3times제공기능 추가하기
    score = 0
    crash = True
    game_on = True
    while game_on: #게임실행 기본이벤트루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #키가 눌렸는데 고것이 스페이스
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0, main_screen_width - cars[i].width)
                        cars[i].y = random.randrange(-150, -50) #장애물car 출몰위치조정
                        cars[i].load_image()

                    player.load_image() #change player car to random in next new game
                    player.x = main_screen_width / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False) #delete mouse in screen
                    sound_engine.play()
                    sleep(5) #만약에 죽으면 5초동안 bgm끌게여
                    pygame.mixer.music.play(-1) #racing bgm반복해서 재생(-1)

            if not crash:
                if event.type == pygame.KEYDOWN: #키 누를때
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4

                        
                if event.type == pygame.KEYUP: #키 안누를때
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0  #키 안누를땐 움직이면 안되니까 dx,dy모두 setting값 0

        screen.fill(gray)

        if not crash:
            for i in range(lane_count):
                pygame.draw.rect(screen, white, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10 #도로차선의 속도, 높을수록 fast
                if lanes[i][1] > main_screen_height:
                    lanes[i][1] = -40 -lane_height

            #사용자가 앞,뒤로도 움직일 수 있게끔 기능추가하
            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            for i in range(car_count):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > main_screen_height:
                    score += 10
                    cars[i].x = random.randrange(0, main_screen_width - cars[i].width)
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].load_image()

            for i in range(car_count):
                if player.check_crash(cars[i]):
                    crash = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break

            draw_score()
            pygame.display.flip()

        else:
            draw_main_menu()

        clock.tick(60)

    pygame.quit()
