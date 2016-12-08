import pygame

class Game:
    def main (self, screen):
        MAIN_LOOP = True
        FPS = 30
        BG_COLOR = (200, 200, 200)
        CAPTURE_MOUSE = False

        clock = pygame.time.Clock() #for using less CPU, events are queued, may miss
        
        sprites = pygame.sprite.Group()
        self.player = Player(sprites)
        
        while MAIN_LOOP:
            clock.tick(FPS) #microsleep, doesn't invoke more than 30 times/s
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        CAPTURE_MOUSE = not CAPTURE_MOUSE
                        pygame.mouse.set_visible(not CAPTURE_MOUSE) 
                        pygame.event.set_grab(CAPTURE_MOUSE)
                print(pygame.mouse.get_pressed())
                print(pygame.mouse.get_rel())
                
                screen.fill(BG_COLOR) #background color

                sprites.update(dt/1000., self)#groups
                sprites.draw(screen)
                pygame.display.flip() #tearing, double buffering->display buffer/drawing bugffer


class Player (pygame.sprite.Sprite):
    def __init__ (self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('DBall.png')
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

    def update (self, dt, game):
        last = self.rect.copy()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
             self.rect.x -= 300*dt
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.rect.x += 300*dt
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.rect.y -= 300*dt
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.rect.y += 300*dt
        

    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    G = Game()
    G.main(screen)
    pygame.quit()
