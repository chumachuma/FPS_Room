import pygame
from random import uniform as random

images = {}
sounds = {}

class Game:
    def __init__ (self, screen):
        self.isMouseCaptured = False
        self.screen = screen
        self.stats = Statistics()

        global images, sounds

        images["target"] = pygame.image.load("./img/target.png")
        images["crosshair"] = pygame.image.load("./img/crosshair.png")
        images["grid"] = pygame.image.load("./img/grid.png")

        sounds["shot"] = pygame.mixer.Sound("./sound/9mmGunshot.wav")
        sounds["shot"].set_volume(0.25)
        #sounds["hit"] = pygame.mixer.Sound("./sound/hit.wav")
        sounds["miss"] = pygame.mixer.Sound("./sound/miss.wav")
        sounds["miss"].set_volume(0.4)

    def __call__ (self):
        self.main()
        self.exit()

    def main (self):
        MAIN_LOOP = True
        FPS = 60
        BG_COLOR = (200, 200, 200)
        NUM_TARGETS = 2

        clock = pygame.time.Clock() #for using less CPU, events are queued, may miss
        
        sprites = pygame.sprite.OrderedUpdates()
        self.background = Background(self.screen)
        self.targets = []
        for i in range(NUM_TARGETS):
            self.targets.append(Target(sprites, self.screen))
        sprites.add(self.loadCrosshair())
        self.toggleCaptureMouse()

        while MAIN_LOOP:
            clock.tick(FPS)
            dt = clock.get_time()
            MAIN_LOOP = self.gameEvent()

            self.mouseIncrement = pygame.mouse.get_rel()
            #self.screen.fill(BG_COLOR) #background color
            self.background.update(dt, self)
            sprites.update(dt, self)#groups
            sprites.draw(self.screen)
            pygame.display.flip() #tearing, double buffering->display buffer/drawing bugffer

            print("\r FPS:%.2f  ACC:%.2f%%  SPD:%.2f HIT:%i  ESC:%i    " % 
                (clock.get_fps(), self.stats.get_accuracy(), self.stats.get_speed(), self.stats.hits, self.stats.escapes), 
                end='')

    def exit (self):
        print('')

    def gameEvent (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.toggleCaptureMouse()
        return True

    def loadCrosshair (self):
        crosshairSize = (32, 32)
        center = ((self.screen.get_width()-crosshairSize[0])/2, (self.screen.get_height()-crosshairSize[1])/2)
        crosshair = pygame.sprite.Group()
        crosshairImg = images["crosshair"] 
        crosshairImg = pygame.transform.scale(crosshairImg, crosshairSize)
        crosshairSprite = pygame.sprite.Sprite(crosshair)
        crosshairSprite.image = crosshairImg
        crosshairSprite.rect = pygame.rect.Rect(center, crosshairSize)
        return crosshair

    def toggleCaptureMouse (self):
        self.isMouseCaptured = not self.isMouseCaptured 
        pygame.mouse.set_visible(not self.isMouseCaptured) 
        pygame.event.set_grab(self.isMouseCaptured)


class Target (pygame.sprite.Sprite):
    def __init__ (self, *groups):
        super(Target, self).__init__(groups[0])
        self.screen = groups[1]
        self.image = images["target"]
        self.shootST = sounds["shot"]
        self.missST = sounds["miss"]
        self.radius = 16
        self.radius2 = self.radius**2 
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.rect = pygame.rect.Rect((-self.radius*2, -self.radius*2), (self.radius*2, self.radius*2))
        self.timeToLive = 2000
        self.timeLived = 0

        self.hGenRange = 0.1
        self.vGenRange = 0.25
        self.hGen = (self.screen.get_width()*self.hGenRange, self.screen.get_width()*(1-self.hGenRange))
        self.vGen = (self.screen.get_height()*self.vGenRange, self.screen.get_height()*(1-self.vGenRange))

    def update (self, dt, game):
        self.timeLived += dt
        if self.timeLived > self.timeToLive:
            self.miss()
        self.rect.x -= game.mouseIncrement[0]
        self.rect.y -= game.mouseIncrement[1]
        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot (self):
        game.stats.shoot()
        self.shootST.stop()
        self.shootST.play()
        center = (self.rect.x + self.radius - self.screen.get_width()/2, self.rect.y + self.radius - self.screen.get_height()/2)
        distance2 = center[0]**2 + center[1]**2
        if distance2 < self.radius2:
            self.hit()

    def respawn (self):
        self.timeLived = 0
        self.rect.x = random(*self.hGen)
        self.rect.y = random(*self.vGen)

    def miss (self):
        game.stats.escape()
        self.missST.stop()
        self.missST.play()
        self.respawn()

    def hit(self):
        #self.hitST.stop()
        #self.hitST.play()
        game.stats.hit(self.timeLived)
        self.respawn()


class Background:
    def __init__ (self, screen):
        self.image = images["grid"]
        self.size = self.image.get_width()
        self.columns = screen.get_width()//self.size + 3
        self.rows = screen.get_height()//self.size + 3
        self.xPos = 0
        self.yPos = 0

    def update (self, dt, game):
        self.xPos -= game.mouseIncrement[0]
        self.yPos -= game.mouseIncrement[1]
        self.xPos %= self.size
        self.yPos %= self.size

        for i in range(self.columns):
            for j in range(self.rows):
                game.screen.blit(self.image, ((i-1)*self.size+self.xPos, (j-1)*self.size+self.yPos))


class Statistics:
    def __init__ (self):
        self.shots = 0
        self.hits = 0
        self.escapes = 0
        self.speed = 0
        self.accuracy = []
        self.isStarted = False

    def shoot (self):
        self.shots += 1

    def escape (self):
        if self.isStarted:
            self.escapes += 1

    def hit (self, speed=0):
        if not self.isStarted:
            self.isStarted = True
        self.hits += 1
        self.speed += speed

    def get_accuracy (self):
        if self.shots:
            return (self.hits/self.shots)*100
        return 0

    def get_speed (self):
        if self.hits:
            return (self.speed / self.hits)/1000
        return 0


if __name__ == '__main__':
    pygame.init()
    print(pygame.display.Info())
    screen = pygame.display.set_mode((1280, 720))
    game = Game(screen)
    game()
    pygame.quit()
