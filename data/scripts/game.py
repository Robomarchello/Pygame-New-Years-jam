import pygame
import random as rd
import time

from pygame.locals import *
from data.scripts.easings import *
from data.scripts.spriteSheet import *

class Combo():
    def __init__(self,pos):
        self.pos = pos
        
        self.combo = 1
        self.comb1 = 25
        self.comb2 = 50
        self.comb3 = 100

        self.startColor = pygame.Color(0,255,0)
        self.color1 = pygame.Color(255,0,255)
        self.color2 = pygame.Color(255,0,0)
        self.color3 = pygame.Color(238,130,238)
        
        self.multiplier = 1
        self.font = pygame.font.Font('data/assets/Roboto.ttf',40)

    def draw(self,screen):
        if self.combo < 0:
            self.combo = 0
        screen.blit(self.font.render(f'Combo:{self.combo*self.multiplier}',True,self.get_color()),self.pos)
    def get_color(self):
        if self.combo < self.comb1:
            percent = self.combo/self.comb1
            return self.startColor.lerp(self.color1,percent)
        elif self.combo < self.comb2:
            percent = self.combo/self.comb2
            return self.color1.lerp(self.color2,percent)
        elif self.combo < self.comb3:
            percent = self.combo/self.comb3
            return self.color2.lerp(self.color3,percent)
            if percent > 1:
                percent = 1
        else:
            percent = 0.99
            return self.color2.lerp(self.color3,percent)
        return self.startColor.lerp(self.color1,percent)

class HealthBar():
    def __init__(self,rect,color,hp):
        self.rect = rect
        self.color = color
        self.maxHp = hp
        self.hp = hp

        self.regen = False
        self.regenTime = 15
        self.regenStamp = time.time()+self.regenTime

        self.hpLen = self.rect.width//self.maxHp

    def draw(self,screen):
        hpRect = self.rect.copy()
        hpRect.width = self.hpLen*self.hp

        if self.regen == True:
            if self.regenStamp < time.time():
                if self.hp < self.maxHp:
                    self.hp += 1
                self.regenStamp = time.time()+self.regenTime

        self.rect.width = self.hpLen*self.maxHp
        pygame.draw.rect(screen,self.color,hpRect)
        pygame.draw.rect(screen,(0,0,0),self.rect,width=4)

class Wave_Timer():
    def __init__(self,mutation_menu): 
        self.wave = 1
        self.waveTime = 30
        self.timer = time.time()+self.waveTime

        self.timerStop = False
        self.update = False
        self.timeLeft = abs(self.timer-time.time())

        self.font = pygame.font.Font('data/assets/Roboto.ttf',50)

        self.mutation_menu = mutation_menu

    def draw(self,screen):
        if self.timerStop == True:
            self.timer = time.time()+self.waveTime
        self.timeLeft = self.timer-time.time()

        if self.timeLeft < 0:
            self.mutation_menu.upgrade_count += 1
            self.update = True
            self.timerStop = True

        if self.mutation_menu.upgrade_count < 1:
            self.timerStop = False

        text = self.font.render(str(round(self.timeLeft,1)),True,(255,255,255))
        rect = text.get_rect(center = [512,740])

        screen.blit(text,rect.topleft)
        
class Cursor():
    def __init__(self,radius):
        self.radius = radius
        self.rect = pygame.Rect(-radius,-radius,radius,radius)

        self.damage = 1

        self.maxRes = 8#px
        self.resEase = easeInOutQuart([self.maxRes,0],[0,0],0.0)
        
        self.pressAnim = False 
        self.pressed = False
        
    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.rect.center = event.pos

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 2:
                if self.pressAnim == False:
                    self.pressAnim = True
                    self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 or event.button == 2:
                self.pressed = False 
    def draw(self,screen):
        if self.pressAnim == True:
            if self.resEase.percent < 1:
                self.resEase.percent += 0.05
            else:
                self.pressAnim = False
        else:
            if self.resEase.percent > 0:
                self.resEase.percent -= 0.05
        if self.resEase.percent < 0:
            self.resEase.percent = 0

        resRadius = self.radius+self.resEase.get_pos()[0]
        pygame.draw.circle(screen,(0,0,0),self.rect.center,resRadius,width=2)
        pygame.draw.line(screen,(0,0,0),[self.rect.center[0],self.rect.center[1]-resRadius],[self.rect.center[0],self.rect.center[1]+resRadius-1],width=2)
        pygame.draw.line(screen,(0,0,0),[self.rect.center[0]-resRadius,self.rect.center[1]],[self.rect.center[0]+resRadius-1,self.rect.center[1]],width=2)


class Target():
    def __init__(self,pos,image):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.speed = 2
        self.speedmult = 0.7

    def draw(self,screen):
        self.rect.y += self.speed*self.speedmult
        screen.blit(self.image,self.rect.topleft)
    
class Armored_Target():
    def __init__(self,pos,images):
        self.crntImg = 0
        self.images = images
        self.destroyed = False
        self.rect = self.images[0].get_rect(center=pos)

        self.speed = 2
        self.speedmult = 0.7

    def draw(self,screen):
        self.rect.y += self.speed*self.speedmult
        
        if self.crntImg == len(self.images)-1:
            self.destroyed = True
            
            
        screen.blit(self.images[self.crntImg],self.rect.topleft)



class Showing_Target():
    def __init__(self,pos1,pos2,image,destImg,brick,duration):
        self.pos1 = pos1
        self.pos2 = pos2
        self.ease = easeOutQuart(pos1,pos2,0.0)

        self.duration = time.time()+duration
        self.moveDir = True
        self.fromDir = {'left':False,'right':False}

        self.destroyed = False
        
        if pos1[0] < pos2[0]:
            self.fromDir['left'] = True
        elif pos1[0] > pos2[0]:
            self.fromDir['right'] = True
        #set_pos
        self.brick = brick
        self.brickRect = brick.get_rect()

        self.destImg = destImg
        self.image = image
        self.imgrect = image.get_rect()

        self.speed = 0.5

        self.update_pos()

    def draw(self,screen):
        screen.blit(self.brick,self.brickRect.topleft)
        if self.destroyed == False:
            screen.blit(self.image,self.imgrect.topleft)
        else:
            screen.blit(self.destImg,self.imgrect.topleft) 
        if self.moveDir == True:
            if self.ease.percent < 1:
                self.ease.percent += 0.01*self.speed

        else:
            if self.ease.percent > 0:
                self.ease.percent -= 0.01*self.speed

        if self.duration < time.time():
            self.moveDir = False

        #set_pos
        get_pos = self.ease.get_pos()
        self.brickRect.center = get_pos
        self.brickRect.right = get_pos[0]
        if self.fromDir['left'] == True:
            self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]
            self.imgrect.center = [self.brickRect.right,self.imgrect.center[1]]
        elif self.fromDir['right'] == True:
            self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]
            self.imgrect.center = [self.brickRect.left,self.imgrect.center[1]]
        

    def update_pos(self):
        self.brickRect.center = self.pos1
        self.brickRect.right = self.pos1[0]
        self.imgrect.center = [self.brickRect.right,self.imgrect.center[1]]
        self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]

class target_piece():
    def __init__(self,pos,image):
        self.pos = pos
        self.pieceImg = image
        self.pieceImg.set_colorkey((0,0,0))

        self.speed = rd.uniform(0.2,0.7)*rd.choice([-1,1]) 
        self.angle = 0

    def draw(self,screen):
        self.angle += self.speed

        self.pos[1] += 2
        rotImg = pygame.transform.rotate(self.pieceImg,self.angle)
        screen.blit(rotImg,self.pos)

class Bullet():
    def __init__(self,pos,radius,angle):
        self.pos = pos
        self.radius = radius
        self.angle = angle

        self.radiusAnim = 5
        self.radiusEase = Linear([self.radiusAnim,0],[0,0],0.0)
        self.dir = True

        self.speed = 1

    def draw(self,screen):
        getRad = self.radiusEase.get_pos()[0]
        if self.radiusEase.percent < 1:
            if self.dir == True:
                self.radiusEase.percent += 0.03
        else:
            self.dir = False

        if self.radiusEase.percent > 0:
            if self.dir == False:
                self.radiusEase.percent -= 0.03
        else:
            self.dir = True
        
        self.pos[0] -= math.cos(self.angle)*self.speed
        self.pos[1] += math.sin(self.angle)*self.speed
        pygame.draw.circle(screen,(150,150,150),self.pos,self.radius+getRad)
        pygame.draw.circle(screen,(25,25,25),self.pos,self.radius+getRad,width=3)

    def ifCollide(self,cursor):
        dist = math.sqrt((cursor.rect.center[0]-self.pos[0])**2+(cursor.rect.center[1]-self.pos[1])**2)

        if dist-self.radius-cursor.radius < 0:
            return True
        else:
            return False
class Cannon():
    def __init__(self,pos,gun,stand,hpBar,combo):
        self.pos = pos

        self.combo = combo
        self.hpBar = hpBar

        self.gun = gun
        self.stand = stand
        
        self.rect = self.stand.get_rect(bottomleft=self.pos)
        self.angle = 0

        self.bulletDelay = 1
        self.bulletTimer = time.time()+self.bulletDelay
        self.bullets = []

        self.mp = [0,0]

        self.hitSound = pygame.mixer.Sound('data/assets/hitHurt.ogg')
        
    def get_angle(self):
        self.dist = [self.rect.center[0]-self.mp[0],self.rect.top-self.mp[1]]
        self.angle = math.degrees(math.atan2(self.dist[0],self.dist[1]))

    def update(self):
        if self.bulletTimer <= time.time():
            self.bulletTimer = time.time()+self.bulletDelay#30,55

            #get bullet pos
            radAng = math.radians(self.angle-90)
            pos = [self.rect.center[0],self.rect.top]
            pos[0] -= math.cos(radAng)*30
            pos[1] += math.sin(radAng)*55
            
            self.bullets.append(Bullet(pos,20,radAng))

    def popBullet(self):
        try:
            self.bullets.pop(self.bullets.index(bullet))
        except:
            pass
    def draw(self,screen,cursor):
        self.update()
        #rotate gun
        #draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
            
            if bullet.pos[0] > 1024 or bullet.pos[0]+bullet.radius < 0 or bullet.pos[1] > 768 or bullet.pos[1]+bullet.radius < 0:
                self.popBullet()


            if bullet.ifCollide(cursor):
                try:
                    self.bullets.pop(self.bullets.index(bullet))
                    self.hpBar.hp -= 1
                    self.combo.combo = 1
                    self.hitSound.play()
                    
                except:
                    pass
                
                
        self.get_angle()
        rotatedGun = pygame.transform.rotate(self.gun,self.angle)
        rotGunRect = rotatedGun.get_rect(center=(self.rect.center[0],self.rect.top))

        screen.blit(rotatedGun,rotGunRect.topleft)

        #blit stand
        screen.blit(self.stand,self.rect.topleft)
    
class Target_System():
    def __init__(self,cursor,wave_timer,hpBar,combo,updateParallax):
        self.combo = combo
        self.score = 0
        self.wave = wave_timer.wave
        self.Wave_Timer = wave_timer

        self.updateParallax = updateParallax

        self.hpBar = hpBar

        self.pieces = []

        self.destroySnd = [
            pygame.mixer.Sound('data/assets/Hitsound.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound1.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound2.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound3.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound4.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound5.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound6.ogg'),
            pygame.mixer.Sound('data/assets/Hitsound7.ogg')]
        
        self.cursor = cursor

        self.targSpeed = 0.5
        
        self.target_1 = pygame.image.load('data/assets/target_1.png').convert()
        self.target_1.set_colorkey((0,0,0))
        self.targets = []
        self.targets.append(Target([rd.randint(0,1024),-128],self.target_1))

        self.brick = pygame.image.load('data/assets/wood_horizontal.png').convert_alpha()
        
        self.showTarget = pygame.image.load('data/assets/target_1_big.png').convert()
        self.showTarget.set_colorkey((0,0,0))
        self.showTargetDestroyed = pygame.image.load('data/assets/target_1_big_destroyed.png').convert()
        self.showTargetDestroyed.set_colorkey((0,0,0))
        
        self.show_targets = []
        self.show_targets_poses = [([-64,250],[275,250]),([1088+self.brick.get_width(),250],[1088,250])]

        self.images = spriteSheet(pygame.image.load('data/assets/armored_target_imgs.png').convert(),(96,96))

        self.pieceImgs = [
            pygame.image.load('data/assets/targetPiece1.png').convert(),
            pygame.image.load('data/assets/targetPiece2.png').convert(),
            pygame.image.load('data/assets/targetPiece3.png').convert(),
        ]
            
        for img in self.images:
            img.set_colorkey((0,0,0))

        for img in self.pieceImgs:
            img.set_colorkey((0,0,0))
            
        self.armored_targets = []

        self.appendUpdt = time.time()+1

        self.mp = [0,0]

        self.cannon_gun = pygame.image.load('data/assets/cannon_gun.png').convert()
        self.cannon_gun.set_colorkey((255,255,255))
        self.cannon_stand = pygame.image.load('data/assets/cannon_stand.png').convert()
        self.cannon_stand.set_colorkey((255,255,255))
        self.cannons = [
            ]

    def update_speed(self):
        if self.targSpeed < 1.2:
            self.targSpeed += 0.1

        self.updateParallax()

    def clean(self):
        self.targets = []
        self.show_targets = [] 
        self.armored_targets = []
        for cannon in self.cannons:
            cannon.bullets = []
        
    def draw(self,screen):
        if self.Wave_Timer.timerStop == True:
            self.update_speed()
            
            if self.Wave_Timer.wave == 1:
                self.cannons.append(Cannon([200,768],self.cannon_gun,self.cannon_stand,self.hpBar,self.combo))

            if self.Wave_Timer.wave == 4:
                self.cannons.append(Cannon([800,768],self.cannon_gun,self.cannon_stand,self.hpBar,self.combo))

            self.Wave_Timer.wave += 1

        #Append targets
        if self.appendUpdt < time.time():
            if rd.randint(0,10) == 10:
                self.armored_targets.append(Armored_Target([rd.randint(0,1024),-64],self.images))
            elif rd.randint(0,5) == 5:
                pos = rd.choice([([-64,250],[275,250]),([1088+self.brick.get_width(),250],[1088,250])])
                ps = rd.randint(100,600)
                pos[0][1] = ps
                pos[1][1] = ps
                self.show_targets.append(Showing_Target(pos[0],pos[1],self.showTarget,self.showTargetDestroyed,self.brick,1))
            else:
                self.targets.append(Target([rd.randint(0,1024),-64],self.target_1))
                self.appendUpdt = time.time()+1

            
        #loop targets
        for target in self.targets:
            target.speedmult = self.targSpeed
            target.draw(screen)
            
            if target.rect.top > 768:
                try:
                    self.targets.pop(self.targets.index(target))
                    self.combo.combo -= 3
                except:
                    pass

        for target in self.show_targets:
            target.draw(screen)

            if target.ease.percent <= 0.0:
                try:
                    self.show_targets.pop(self.show_targets.index(target))
                    if target.destroyed == False:
                        self.combo.combo -= 2
                except:
                    pass
                
        for target in self.armored_targets:
            target.speedmult = self.targSpeed
            target.draw(screen)
            if target.rect.top > 768:
                try:
                    self.armored_targets.pop(self.targets.index(target))
                    self.combo.combo -= 5
                except:
                    pass
                
        for cannon in self.cannons:
            cannon.draw(screen,self.cursor)
            
        for piece in self.pieces:
            piece.draw(screen)
            


    def playSnd(self):
        if self.combo.combo < 5:
            self.destroySnd[0].play()
        elif self.combo.combo < 10:
            self.destroySnd[1].play()
        elif self.combo.combo < 15:
            self.destroySnd[2].play()
        elif self.combo.combo < 20:
            self.destroySnd[3].play()
        elif self.combo.combo < 30:
            self.destroySnd[4].play()
        elif self.combo.combo < 40:
            self.destroySnd[5].play()
        elif self.combo.combo < 50:
            self.destroySnd[6].play()
        elif self.combo.combo < 60:
            self.destroySnd[7].play()
        else:
            self.destroySnd[7].play()

    def addPieces(self,target):
        self.combo.combo += 1
        for x in range(3):
            self.pieces.append(target_piece([target.rect.center[0]+rd.randint(-30,30),target.rect.center[1]+rd.randint(-30,30)],self.pieceImgs[x]))

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.mp = event.pos

            for cannon in self.cannons:
                cannon.mp = event.pos

        if event.type == MOUSEBUTTONDOWN:
            getCollide = False
            if event.button == 1 or event.button == 2:
                
                for target in self.targets:
                    if target.rect.colliderect(self.cursor):
                        self.targets.pop(self.targets.index(target))
                        self.playSnd()
                        self.addPieces(target)
                        getCollide = True
                        
                for target in self.show_targets:
                    if target.destroyed == False:
                        self.combo.combo += 1
                    if target.imgrect.colliderect(self.cursor):
                        target.destroyed = True
                        self.playSnd()
                        getCollide = True

                for target in self.armored_targets:
                    if target.rect.colliderect(self.cursor):
                        if self.cursor.damage >= 3:
                            target.destroyed = True
                            getCollide = True
                        else:
                            target.crntImg += self.cursor.damage
                            if target.crntImg >= len(self.images):
                                getCollide = True
                                target.crntImg = 0
                                target.destroyed = True

                    if target.destroyed == True:
                        getCollide = True
                        self.playSnd()
                        self.armored_targets.pop(self.armored_targets.index(target))
                        self.addPieces(target)
                if getCollide == False:
                    self.combo.combo -= 1
class GameOver():
    def __init__(self,hp):
        self.hp = hp
        self.surf = pygame.Surface((1024,768))
        self.gameover = False

        self.font = pygame.font.Font('data/assets/Roboto.ttf',80)

        self.rdText = [
            'You can do better:)',
            'Hhhoow?',
            'Take another try',
            'This all you got?',
            'I thought you are better',
            'How did you die?!?']

        self.text = rd.choice(self.rdText)

        self.appearEff = easeInBounce([0,-self.surf.get_width()],[0,0],0.0)


    def draw(self,screen):
        self.surf.fill((105,105,105))

        render = self.font.render(self.text,True,(170,170,170))
        rectrend = render.get_rect(center = [512,100])
        self.surf.blit(render,rectrend.topleft)

        self.surf.blit(self.font.render('Press R to restart',True,(170,170,170)),(0,670))
        if self.gameover == True:
            if self.appearEff.percent < 1:
                self.appearEff.percent += 0.0025
        else:
            if self.appearEff.percent > 1:
                self.appearEff.percent -= 0.0025
        if self.appearEff.percent > 0.0:
            screen.blit(self.surf,self.appearEff.get_pos())

    def handle_event(self,event):
        if self.gameover == True:
            if event.type == KEYDOWN:
                if event.key == K_r:
                    self.gameover = False
                    self.hp.hp = 3
                    self.hp.maxHp = 3
                    self.appearEff = easeInBounce([0,-self.surf.get_width()],[0,0],0.0)
