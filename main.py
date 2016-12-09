import pygame

class Game:
    def __init__ (self):
        self.isMouseCaptured = False

    def __call__ (self, screen):
        self.main(screen)

    def main (self, screen):
        MAIN_LOOP = True
        FPS = 60
        BG_COLOR = (200, 200, 200)

        clock = pygame.time.Clock() #for using less CPU, events are queued, may miss
        
        sprites = pygame.sprite.Group()
        self.target = Target(sprites)
        
        self.toggleCaptureMouse()

        while MAIN_LOOP:
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.toggleCaptureMouse()

                ######print(pygame.mouse.get_pressed())
                
                screen.fill(BG_COLOR) #background color

                sprites.update(dt/1000., self)#groups
                sprites.draw(screen)
                pygame.display.flip() #tearing, double buffering->display buffer/drawing bugffer
            print("\r %i     "%int(clock.get_fps()), end='')

    def toggleCaptureMouse (self):
        self.isMouseCaptured = not self.isMouseCaptured 
        pygame.mouse.set_visible(not self.isMouseCaptured) 
        pygame.event.set_grab(self.isMouseCaptured)

class Target (pygame.sprite.Sprite):
    def __init__ (self, *groups):
        super(Target, self).__init__(*groups)
        self.image = pygame.image.load('DBall.png')
        self.radius = self.image.get_size()[0]
        self.radius2 = self.radius**2 
        self.rect = pygame.rect.Rect((320, 240), (self.radius*2, self.radius*2))

    def update (self, dt, game):
        last = self.rect.copy()
        movement_increment = pygame.mouse.get_rel()
        self.rect.x -= movement_increment[0]
        self.rect.y -= movement_increment[1]
        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot (self):
       center =  (self.rect.x + self.radius, self.rect.y + self.radius)
       print(center)
       

    
if __name__ == '__main__':
    pygame.init()
    print(pygame.display.Info())
    screen = pygame.display.set_mode((640, 480))
    game = Game()
    game(screen)
    pygame.quit()
