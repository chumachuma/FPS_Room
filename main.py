import pygame
from random import uniform as random

class Game:
    def __init__ (self):
        self.isMouseCaptured = False

    def __call__ (self, screen):
        self.main(screen)

    def main (self, screen):
        self.screen = screen

        MAIN_LOOP = True
        FPS = 60
        BG_COLOR = (200, 200, 200)

        clock = pygame.time.Clock() #for using less CPU, events are queued, may miss
        
        sprites = pygame.sprite.OrderedUpdates()
        self.target = Target(sprites, self.screen)
        sprites.add(self.loadCrosshair())
        self.toggleCaptureMouse()

        while MAIN_LOOP:
            clock.tick(FPS)
            dt = clock.get_time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.toggleCaptureMouse()

            self.screen.fill(BG_COLOR) #background color
            sprites.update(dt, self)#groups
            sprites.draw(self.screen)
            pygame.display.flip() #tearing, double buffering->display buffer/drawing bugffer
            #print("\r %i     "%int(clock.get_fps()), end='')

    def loadCrosshair (self):
        crosshairSize = (32, 32)
        center = ((self.screen.get_width()-crosshairSize[0])/2, (self.screen.get_height()-crosshairSize[1])/2)
        print(center)
        crosshair = pygame.sprite.Group()
        crosshairImg = pygame.image.load("./img/crosshair.png")
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
        self.radius = 16
        self.radius2 = self.radius**2 
        self.image = pygame.image.load('DBall.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.rect = pygame.rect.Rect((-self.radius*2, -self.radius*2), (self.radius*2, self.radius*2))
        self.timeToLive = 1500
        self.timeLived = 0

    def update (self, dt, game):
        self.timeLived += dt
        if self.timeLived > self.timeToLive:
            self.respawn()
        movement_increment = pygame.mouse.get_rel()
        self.rect.x -= movement_increment[0]
        self.rect.y -= movement_increment[1]
        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot (self):
       center =  (self.rect.x + self.radius - self.screen.get_width()/2, self.rect.y + self.radius - self.screen.get_height()/2)
       distance2 = center[0]**2 + center[1]**2
       if distance2 < self.radius2:
           self.respawn()

    def respawn (self):
        self.timeLived = 0
        self.rect.x = random(0, self.screen.get_width())
        self.rect.y = random(0, self.screen.get_height())


if __name__ == '__main__':
    pygame.init()
    print(pygame.display.Info())
    screen = pygame.display.set_mode((1280, 720))
    game = Game()
    game(screen)
    pygame.quit()
