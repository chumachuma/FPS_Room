import pygame

class Game:
    def main (self, screen):
        clock = pygame.time.Clock() #for using less CPU, events are queued, may miss
        
        sprites = pygame.sprite.Group()
        self.player = Player(sprites)
        self.walls=pygame.sprite.Group()
        block = pygame.image.load("DBall.png")
        for x in range (0, 640, 54): #54 size of image
            for y in range (0, 480, 54):
                if x in (0, 640-54) or y in (0,480-54):
                    wall = pygame.sprite.Sprite(self.walls)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x,y), (54,32))
        sprites.add(self.walls)
        
        while 1:
            clock.tick(30) # microsleep, doesn't invoke more than 30 times/s
            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                
                sprites.update(dt/1000., self)#groups
                screen.fill((200, 200, 200)) #background color
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
        for cell in pygame.sprite.spritecollide(self, game.walls, False):
            self.rect = last
        

    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    G = Game()
    G.main(screen)
    pygame.quit()
