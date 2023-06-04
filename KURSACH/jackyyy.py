import sys
import pygame
import os
import random
import math

WIDTH = 623
HEIGHT = 150
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('let him cook')

class Background:

    def __init__(self, x):
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('content/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Game:

    def __init__(self, highestscore=0):
        self.bg = [Background(x=0),Background(x=WIDTH)]
        self.jackyyy = Jackyyy()
        self.obstacles = []
        self.collision = Collision()
        self.score = Score(highestscore)
        self.speed = 3
        self.playing = False
        self.set_sound()
        self.set_labels()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 22, bold = True)
        small_font = pygame.font.SysFont('monospace', 18, bold=False)
        self.big_lbl = big_font.render(f'J A C K Y Y Y  D E A D', 1, (0, 0, 0))
        self.small_lbl = small_font.render(f'*press esc to let him cook again*', 1, (0, 0, 0))

    def set_sound(self):
        path = os.path.join('content/sounds/die1.wav')
        self.sound = pygame.mixer.Sound(path)

    def start(self):
        self.playing = True

    def over(self):
        self.sound.play()
        screen.blit(self.big_lbl, (WIDTH // 2 - self.big_lbl.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_lbl, (WIDTH // 2 - self.small_lbl.get_width() // 2, HEIGHT // 2))
        self.playing = False

    def tospawn(self, loops):
        return loops % 100 == 0

    def spawn_moai(self):
        # list with moai
        if len(self.obstacles) > 0:
            prev_moai = self.obstacles[-1]
            x = random.randint(prev_moai.x + self.jackyyy.width + 100, WIDTH + prev_moai.x + self.jackyyy.width + 100)

        # empty list
        else:
            x = random.randint(WIDTH + 100, 1000)

        # create the new moai
        moai = Moai(x)
        self.obstacles.append(moai)

    def restart_game(self):
        self.__init__(highestscore=self.score.highestscore)

class Jackyyy:

    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_number = 0
        self.dy = 3
        self.gravity = 1.23
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.set_sound()
        self.show()

    def update(self, loops):
        #jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        #falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # walking
        elif self.onground and loops % 7 == 0:
           self.texture_number=(self.texture_number+1) % 11 #returns 0,1,2,...,9,10
           self.set_texture()


    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f'content/images/jack{self.texture_number}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_sound(self):
        path = os.path.join('content/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def jump(self):
        self.sound.play()
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True

class Moai:

    def __init__(self, x):
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('content/images/moai.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Collision:

        def between(self, obj1, obj2):
            distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)#формула дистанції d = sqrt((x2-x1)^2 + (y2-y1)^2)
            return distance < 35

class Score:
    def __init__(self, highestscore):
        self.highestscore = highestscore
        self.actualscore = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.show()

    def update(self, loops):
            self.actualscore = loops // 13 #за допомогою числа міняємо швидкість нарахування балів
            self.check_highestscore()

    def show(self):
       self.lbl = self.font.render(f'Score {self.highestscore} {self.actualscore}', 1, self.color)
       lbl_width = self.lbl.get_rect().width
       screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

    def check_highestscore(self):
        if self.actualscore >= self.highestscore:
            self.highestscore = self.actualscore

    def reset(self):
        self.actualscore = 0

def main():
    # objects
    game = Game()
    jackyyy = game.jackyyy

    # variables
    clock = pygame.time.Clock()
    loops = 0
    over = False

    # mainloop
    while True:
        if game.playing:

         loops += 1

         # Background
         for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

         # jackyyy
         jackyyy.update(loops)
         jackyyy.show()

         # moai
         if loops == 1:
             game.spawn_moai()

         if game.tospawn(loops):
            game.spawn_moai()

         for moai in game.obstacles:
          moai.update(-game.speed)
          moai.show()

          # collision
          if game.collision.between(jackyyy, moai):
                over = True

         if over:
             game.over()

         # score
         game.score.update(loops)
         game.score.show()

        # events
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              if not over:
               if jackyyy.onground:
                  jackyyy.jump()

               if not game.playing:
                  game.start()

            if event.key == pygame.K_ESCAPE:
                game.restart_game()
                jackyyy = game.jackyyy
                loops = 0
                over = False


        clock.tick(77)
        pygame.display.update()

main()
#if __name__ == "__main__":
    #pygame.init()
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #game = Game()
    #clock = pygame.time.Clock()
    #loops = 0
    #over = False
    #while True:
     #   # Your game logic here

      #  clock.tick(77)
       # pygame.display.update()
