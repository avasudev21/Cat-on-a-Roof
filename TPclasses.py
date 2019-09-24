##Contains all the classes that are used in the project
from tkinter import*
class Cat(object):#used to create game's character
    def __init__(self,x,y):
        self.cat = PhotoImage(file = "cat.png")
        self.width = self.cat.width()
        self.height = self.cat.height()
        self.x = x
        self.y = y
        
    def draw(self,canvas):#draws cat
        canvas.create_image(self.x,self.y,image = self.cat)
        
    def jump(self, jumpHeight):#used to facilitate "jump" of cat
        self.y-=jumpHeight
    
    def landsOnBuilding(self,other):#checks if cat lands on building
        if not isinstance(other, Building):
            return False
        else:
            return ((other.x-other.width/2) <= (self.x) <= \
            (other.x+other.width/2)) and (-20 <= \
            (other.y - self.y) - (other.height/2 + self.height/2) <= 20)
    
    def clashesWithBuilding(self,other):#checks if cat collides with building 
    #but does not land on it
        if not isinstance(other, Building):
            return False
        else:
            if self.y>=other.y-other.height/2 and \
            (other.x-other.width/2<=self.x+self.width/2<=other.x+other.width/2):
                return True
    
    def collidesWithFish(self,other):#checks if cat collides with a fish
        if not isinstance(other,Fish):
            return False
        else:
            return (abs(other.x - self.x)<= (other.width/2 + self.width/2)) \
            and (abs(other.y - self.y)<= (other.height/2 + self.height/2))
    
    def collidesWithEnemy(self,other):#check if cat collides with enemy
        if not isinstance(other,Enemy) and not isinstance(other,movingEnemy) \
        and not isinstance(other,flyingEnemy):
            return False
        else:
            return abs(other.x - self.x)<= (other.width/2 + self.width/2) and \
            (abs(other.y - self.y)<= (other.height/2 + self.height/2))
    
    def collidesWithPower(self,other):#checks if cat collides with power icon
        if not isinstance(other,Power):
            return False
        else:
            return abs(other.x - self.x)<= (other.width/2 + self.width/2) and \
            (abs(other.y - self.y)<= (other.height/2 + self.height/2))
            
        
    

class Building(object):#used to create buildings
    def __init__(self,width, height, x, y, color):
        self.width= width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    
    def draw(self,canvas):#draws building
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,\
        self.x+self.width/2,self.y+self.height/2,fill=self.color)
       

class Power(object):#used to create power icons
    def __init__(self,x,y):
        self.x = x
        self.y = y
         
class Speed(Power):#creates speed icon object
    def __init__(self,x,y):
        super().__init__(x,y)
        self.power = PhotoImage(file="speed.png")
        self.width = self.power.width()
        self.height = self.power.height()
    def draw(self,canvas):
          canvas.create_image(self.x,self.y,image = self.power)

class Magnet(Power):#creates magnet icon object
    def __init__(self,x,y):
        super().__init__(x,y)
        self.power = PhotoImage(file="magnet.png")
        self.width = self.power.width()
        self.height = self.power.height()
    def draw(self,canvas):
          canvas.create_image(self.x,self.y,image = self.power)

class Shield(Power):#creates shield icon object
    def __init__(self,x,y):
        super().__init__(x,y)
        self.power = PhotoImage(file="shield.png")
        self.width = self.power.width()
        self.height = self.power.height()
    def draw(self,canvas):
          canvas.create_image(self.x,self.y,image = self.power)
    
    
class Fish(object):#used to create fish object
    def __init__(self,x,y):
        self.fish = PhotoImage(file = "coin.png")
        self.x = x
        self.y = y
        self.width = self.fish.width()
        self.height = self.fish.height()
    
    def draw(self,canvas):
          canvas.create_image(self.x,self.y,image = self.fish)

class Enemy(object):#used to create stationary enemy object
    def __init__(self,x,y):
        self.enemy = PhotoImage(file = "enemy.png")
        self.width = self.enemy.width()
        self.height = self.enemy.height()
        self.x = x
        self.y = y
        
    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image = self.enemy)

class flyingEnemy(object):#used to create flying enemy object
    def __init__(self,x,y):
        self.enemy = PhotoImage(file = "crow.png")
        self.width = self.enemy.width()
        self.height = self.enemy.height()
        self.x = x
        self.y = y
    
    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image = self.enemy)
        
class movingEnemy(object):#used to create moving enemy object
    def __init__(self,x,y):
        self.enemy = PhotoImage(file = "movingEnm.png")
        self.width = self.enemy.width()
        self.height = self.enemy.height()
        self.x = x
        self.y = y
    
    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image = self.enemy)
        
    def landsOnBuilding(self,other):#checks if enemy lands on building
        if not isinstance(other, Building):
            return False
        else:
            return ((other.x-other.width/2)-70<= (self.x) <= \
            (other.x+other.width/2)) and (-70 <= \
            (other.y - self.y) - (other.height/2 + self.height/2) <= 70)
    
    def jump(self, jumpHeight):#used to facilitate "jump" of enemy
        self.y-=jumpHeight
    

class Bone(object):#creates bone object
    def __init__(self,x,y):
        self.bone = PhotoImage(file = "fish.png")
        self.width = self.bone.width()
        self.height = self.bone.height()
        self.x = x
        self.y = y
    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image = self.bone)
    def collidesWithEnemy(self,other):
        if not isinstance(other,Enemy) and not isinstance(other,movingEnemy)\
         and not isinstance(other,flyingEnemy):
            return False
        else:
            return abs(other.x - self.x)<= (other.width/2 + self.width/2) and \
            (abs(other.y - self.y)<= (other.height/2 + self.height/2))
        
       