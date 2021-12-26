import pygame,math
#My easing engine, formulas borrowed from easings.net :)

class Easing():
    def __init__(self,pos1,pos2,percent):
        self.pos1 = pos1
        self.pos2 = pos2
        self.percent = percent

        self.dist = [self.pos2[0]-self.pos1[0],self.pos2[1]-self.pos1[1]]
        
    def get_pos(self):
        raise NotImplementedError
    
class Linear(Easing):
    def __init__(self,pos1,pos2,percent):
        super().__init__(pos1,pos2,percent)
    
    def get_pos(self):
        return [self.pos1[0]+self.dist[0]*self.percent,self.pos1[1]+self.dist[1]*self.percent]
    
class easeOutQuart(Easing):
    def __init__(self,pos1,pos2,percent):
        super().__init__(pos1,pos2,percent)
    
    def get_pos(self):
        prcnt = 1 - pow(1 - self.percent, 4)

        return [self.pos1[0]+self.dist[0]*prcnt,self.pos1[1]+self.dist[1]*prcnt]

class easeInOutQuart(Easing):
    def __init__(self,pos1,pos2,percent):
        super().__init__(pos1,pos2,percent)

    def get_pos(self):
        x = self.percent
        prcnt = 1 - pow(-2 * x + 2, 4) / 2
        
        if x < 0.5:
            prcnt = 8 * x * x * x * x

        return [self.pos1[0]+self.dist[0]*prcnt,self.pos1[1]+self.dist[1]*prcnt]

class easeInBounce(Easing):
    def __init__(self,pos1,pos2,percent):
        super().__init__(pos1,pos2,percent)

    def get_pos(self):
        x = self.percent
        t = self.percent
        prcnt = 0
        
        if t < 4 / 11:
            prcnt = 121 * t * t / 16
        elif t < 8 / 11:
            prcnt = (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            prcnt = (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        else:
            prcnt = (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0

        return [self.pos1[0]+self.dist[0]*prcnt,self.pos1[1]+self.dist[1]*prcnt]

class easeOutBounce(Easing):
    def __init__(self,pos1,pos2,percent):
        super().__init__(pos1,pos2,percent)

    def get_pos(self):
        x = self.percent
        t = self.percent
        prcnt = 0
        
        if t < 4 / 11:
            prcnt = 121 * t * t / 16
        elif t < 8 / 11:
            prcnt = (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            prcnt = (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        else:
            prcnt = (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0

        prcnt = 1-prcnt
        return [self.pos1[0]+self.dist[0]*prcnt,self.pos1[1]+self.dist[1]*prcnt]
