import pygame, math, random

class Model:
    def __init__(self): 
        self.isCustomLevel=False
        self.appOn = True
        self.activeScreen = 'HomeScreen'
        self.screenWidth = 1400; self.screenHeight = 700
        self.selectedLevel = '3' #1 to 5 + custom
        self.lives = 5 #3 to 8
        self.numOfShapes = 5 #3 to 7
        self.charSize = 20 #10 to 30
        self.averageShapeSize = 4 #2 to 7
        self.gravity = 1
        self.colors = [ (0, 0, 0),        
                        (255, 255, 255),  
                        (255, 50, 50),    
                        (50, 255, 50),    
                        (50, 50, 255),    
                        (255, 255, 50),   
                        (50, 255, 255),   
                        (255, 50, 255),   
                        (255, 150, 50),   
                        (150, 50, 255) ]
        self.shapeSizeDistributions = {2: [1,1,1,1,2,2,3,3,4], 
                                       3: [2,2,2,2,3,3,4,4,5],
                                       4: [3,3,3,3,4,4,5,5,6], 
                                       5: [4,4,4,4,5,5,6,6,7], 
                                       6: [5,5,5,5,6,6,7,7,8], 
                                       7: [6,6,6,6,7,7,8,8,9],
                                       8: [7,7,7,7,8,8,9,9,9]}
        self.initialiseGameScreen()
        self.initialiseConfigureScreen()
    
    def initialiseHomeScreen(self):
        self.activeScreen = 'HomeScreen'
        self.initialiseGameScreen()

    def initialiseGameScreen(self):
        self.gameOver = False; self.gamePaused = False
        self.hits = 0; self.particles = []
        self.crosshairX = self.screenWidth//2
        self.crosshairY = self.screenHeight//2
        self.hitSound = pygame.mixer.Sound('pluh.mp3')
        self.hitSound.set_volume(0.5)
        self.keypresses = 0; self.accuracy = 1
        self.score = 0
        self.currentLives=self.lives
        self.shapeSizeDistribution=(
            self.shapeSizeDistributions[self.averageShapeSize])
        self.asciiChars = ['@', '#', '8', '&', 'o', ':', '*', '.', ' ']
        self.charFont = pygame.font.SysFont('Courier', self.charSize, 
                                            bold=True)
        #CHATGPT: List of keys obtained by chatgpt
        self.controlKeys = [
                [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, 
                 pygame.K_MINUS],
                [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, 
                 pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p],
                [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, 
                 pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l],
                [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, 
                 pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD],]
        self.keyBoxes = self.getKeyBoxes(self.controlKeys)
        self.shapes = [self.createShape() for i in range(self.numOfShapes)] 
    
    def initialiseConfigureScreen(self):
        #initialise title - maybe
        #initialise level buttons 
        # (level: button centerX, button centerY, selected=False)
        self.levelButtons = {'1': ['Level 1', 
                                   3*self.screenHeight//10,self.screenWidth/6, 
                                   False],
                             '2': ['Level 2', 
                                   4*self.screenHeight//10,self.screenWidth/6, 
                                   False],
                             '3': ['Level 3', 
                                   5*self.screenHeight//10,self.screenWidth/6, 
                                   False],
                             '4': ['Level 4', 
                                   6*self.screenHeight//10,self.screenWidth/6, 
                                   False],
                             '5': ['Level 5', 
                                   7*self.screenHeight//10,self.screenWidth/6, 
                                   False],
                             'Custom': ['Custom',
                                    8*self.screenHeight//10,self.screenWidth/6, 
                                        False]}
        # self.selectedLevel = '3'
        #initialise game element
        #customised this function from createShape
        self.gameElement = self.createDemoShape() 
        self.configurationSliders = self.createConfigurationSliders()
    
    #GITHUB REPO: all sliders code directly adapted from repo
    #details in citation
    def createConfigurationSliders(self):
        configurations = {'lives':
                Slider((self.screenWidth/2,2.5*self.screenHeight/8), 
                       (300,10), 5, 1, 10, 'Lives'),
            'numOfShapes':
            Slider((self.screenWidth/2,3.25*self.screenHeight/8), 
                   (300,10), 5, 3, 10, 'Number of Shapes'),
            'averageShapeSize':
            Slider((self.screenWidth/2,4.25*self.screenHeight/8), 
                   (300,10), 5, 3, 8, 'Average Shape Size'),
            'charSize':
            Slider((self.screenWidth/2,5.5*self.screenHeight/8), 
                   (300,10), 20, 10, 50, 'Ascii Symbol Size'),
            'gravity':
            Slider((self.screenWidth/2,6.5*self.screenHeight/8), 
                   (300,10), 5, 1, 10, 'Gravity'), 
            }
        return configurations

    def createDemoShape(self):
        shapeType = random.choice(['cube', 'pyramid'])
        size = max(self.shapeSizeDistribution)
        return {
            'x': 4*self.screenWidth//5,
            'y': self.screenHeight//2,
            'z': 0,
            'size': 0,
            'angleX': random.random() * 2 * math.pi,
            'angleY': random.random() * 2 * math.pi,
            'angleZ': random.random() * 2 * math.pi,
            'speed': 3,
            'alive': True,
            'type': shapeType,
            'vertices': self.createVertices(shapeType, size),
            'faces': self.createFaces(shapeType),
            'faceColors': ([random.choice(self.colors[2:]) 
                            for i in self.createFaces(shapeType)]),
            'distance': 250
        }
    
    def update(self):
        if self.activeScreen=='GameScreen':
            if self.keypresses!=0:
                self.accuracy = int(100*math.floor(
                                (self.hits)/self.keypresses)) 
            else:
                 self.accuracy = 100
            self.score = int(self.hits*10*self.accuracy)//100
            self.updateShapes()
            self.updateParticles()
        if self.activeScreen=='ConfigureScreen':
            self.updateGameElement()
    
    def updateGameElement(self):
        shape = self.gameElement
        # shape['y'] += shape['speed']
        shape['angleX'] += 0.02
        shape['angleY'] += 0.03
        shape['angleZ'] += 0.01

    def updateShapes(self):
        if not self.gameOver:
            for shape in self.shapes:
                shape['y'] += shape['speed'] + self.gravity
                shape['angleX'] += 0.02
                shape['angleY'] += 0.03
                shape['angleZ'] += 0.01
                
                if shape['y'] > self.screenHeight + 100:
                    #TODO: change this logic to remove shape from screen 
                    # and new shape
                    self.resetShape(shape) 
                    self.currentLives-=1
                    if self.currentLives==0:
                        self.gameOver=True

    def updateParticles(self):
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def createShape(self):
        shapeType = random.choice(['cube', 'pyramid'])
        # print(self.shapeSizeDistribution)
        size = random.choice(self.shapeSizeDistribution)
        speed = random.randint(1, 5)
        x = random.randint(100, self.screenWidth - 100)
        return {
            'x': x,
            'y': -100,
            'z': 0,
            'size': size,
            'angleX': random.random() * 2 * math.pi,
            'angleY': random.random() * 2 * math.pi,
            'angleZ': random.random() * 2 * math.pi,
            'speed': speed,
            'alive': True,
            'type': shapeType,
            'vertices': self.createVertices(shapeType, size),
            'faces': self.createFaces(shapeType),
            'faceColors': ([random.choice(self.colors[2:]) 
                            for i in self.createFaces(shapeType)]),
            'distance': 250
        }

    def createVertices(self,shapeType, size):
        s = size * (self.averageShapeSize/6)
        if shapeType == 'cube':
            return ([ [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s], 
                    [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]])
        elif shapeType == 'pyramid':
            return ([ [-s, s, -s], [s, s, -s], [s, s, s], 
                     [-s, s, s], [0, -s, 0] ])

    def createFaces(self,shapeType):
        if shapeType == 'cube':
            return [
                [0, 1, 2, 3],  # front
                [4, 5, 6, 7],  # back
                [0, 1, 5, 4],  # bottom
                [2, 3, 7, 6],  # top
                [0, 3, 7, 4],  # left
                [1, 2, 6, 5]   # right
            ]
        else:  # pyramid
            return [
                [0, 1, 2, 3],  # base
                [0, 1, 4],     # front
                [1, 2, 4],     # right
                [2, 3, 4],     # back
                [3, 0, 4]      # left
            ]

    def resetShape(self,shape):
        shape['y'] = -150
        shape['x'] = random.randint(100, self.screenWidth - 100)
        shape['z'] = 0
        shape['distance'] = 250
        shape['alive'] = True
        shape['angleX'] = random.random() * 2 * math.pi
        shape['angleY'] = random.random() * 2 * math.pi
        shape['angleZ'] = random.random() * 2 * math.pi
        shape['faceColors'] = ([random.choice(self.colors[2:]) 
                                for i in shape['faces']])

    def explodeShape(self,shape):
        particles = self.particles
        shape['alive'] = False
        for i in range(25):
            angle = random.random() * 2 * math.pi
            speed = random.randint(2, 8)
            color = random.choice(self.colors[2:])
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            particles.append({
                'x': shape['x'],
                'y': shape['y'],
                'dx': dx,
                'dy': dy,
                'size': random.randint(3, 6),
                'color': color,
                'life': 30
            })
        self.hits += 1
        self.resetShape(shape)

    def getKeyBoxes(self,keys):
        keyBoxes = dict()
        keyRows = len(keys)
        boxHeight = self.screenHeight/keyRows
        for rowIndex in range(keyRows):
            keysInRow = len(keys[rowIndex])
            boxWidth = self.screenWidth/keysInRow
            for colIndex in range(keysInRow):
                keyBoxes[keys[rowIndex][colIndex]]=(colIndex*boxWidth,
                                                    rowIndex*boxHeight,
                                                    boxWidth,boxHeight)
        return keyBoxes
    
    def togglePause(self):
        self.gamePaused = not self.gamePaused

    def setLevel(self,level):
        if self.activeScreen!='ConfigureScreen':
            return
        self.selectedLevel = level #1 to 5 + custom
        if level=='Custom':
            self.isCustomLevel=True
        else:
            self.isCustomLevel=False
            self.applyLevelSettings(level)

    def applyLevelSettings(self, level):
        if level=='1': #easiest
            self.lives = 10; self.currentLives=self.lives
            self.numOfShapes = 3; self.charSize = 15 #10 to 50
            self.averageShapeSize = 8; self.gravity = 1 #1 to 10
        elif level=='2':
            self.lives = 7; self.currentLives=self.lives
            self.numOfShapes = 5; self.charSize = 25
            self.averageShapeSize = 6; self.gravity = 2
        elif level=='3': 
            self.lives = 5; self.currentLives=self.lives
            self.numOfShapes = 6; self.charSize = 20 
            self.averageShapeSize = 5; self.gravity = 3
        elif level=='4':
            self.lives = 3; self.currentLives=self.lives
            self.numOfShapes = 6; self.charSize = 25 
            self.averageShapeSize = 4; self.gravity = 7
        elif level=='5': 
            self.lives = 1; self.currentLives=self.lives
            self.numOfShapes = 6; self.charSize = 30 
            self.averageShapeSize = 4; self.gravity = 10
        self.charFont=pygame.font.SysFont('Courier', self.charSize, bold=True)
        self.shapeSizeDistribution=(
            self.shapeSizeDistributions[self.averageShapeSize])
        if level!='Custom':
            self.gameElement = self.createDemoShape()
        self.updateSliders()
    
    def updateSliders(self):
        sliders=self.configurationSliders
        sliders['lives'].setValue(self.lives)
        sliders['numOfShapes'].setValue(self.numOfShapes)
        sliders['averageShapeSize'].setValue(self.averageShapeSize)
        sliders['charSize'].setValue(self.charSize)
        sliders['gravity'].setValue(self.gravity)

    def calculateAsciiSpacing(self):
        baseSpacing=self.charSize*0.6
        return baseSpacing+(self.averageShapeSize/6)


#GITHUB REPO: all sliders code has been directly adapted from a github repo
# i.e. the entire sliders class below and sliders functions 
# have been picked up from the repo
# repo: https://github.com/vimichael/Pygame-Tutorials 

class Slider:
    def __init__(self, pos: tuple, size: tuple, initialVal: float, min: int, 
                 max: int, gameParameter):
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False
        self.sliderLeftPos = self.pos[0] - (size[0]//2)
        self.sliderRightPos = self.pos[0] + (size[0]//2)
        self.sliderTopPos = self.pos[1] - (size[1]//2)
        self.min = min
        self.max = max
        #(self.sliderRightPos-self.sliderLeftPos)*initialVal#<-percentage
        self.initialVal = initialVal 
        self.containerRect = pygame.Rect(self.sliderLeftPos, 
                                          self.sliderTopPos, self.size[0], 
                                          self.size[1])
        self.buttonRect = pygame.Rect((self.sliderLeftPos + 
                                        self.initialVal - 5),
                                          self.sliderTopPos, 10, 
                                          self.size[1])
        # label
        self.gameParameter = gameParameter
        self.font = pygame.font.SysFont('Courier',25,bold='True')
        self.text = self.font.render(str(int(self.getValue())), True, 
                                     "white", None)
        self.text=self.font.render(
                            f'{self.gameParameter}: {int(self.getValue())}', 
                                    True, "white", None)
        self.labelRect = self.text.get_rect(center = (self.pos[0], 
                                                       self.sliderTopPos-15))
        
    def setValue(self, value):
        value=max(self.min, min(self.max, value))
        valRange=self.sliderRightPos-self.sliderLeftPos-1
        buttonPos=(int(((value-self.min)/(self.max-self.min))*valRange)+
                   self.sliderLeftPos)
        self.buttonRect.centerx=buttonPos
        self.text=self.font.render(f'{self.gameParameter}: {int(value)}', 
                                   True, 'white', None)

    def moveSlider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.sliderLeftPos:
            pos = self.sliderLeftPos
        if pos > self.sliderRightPos:
            pos = self.sliderRightPos
        self.buttonRect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self, screen):
        pygame.draw.rect(screen, "gray", self.containerRect)
        pygame.draw.circle(screen, 'blue', self.buttonRect.center, 12)
        # pygame.draw.rect(app.screen, BUTTONSTATES[self.hovered], 
        # self.buttonRect)

    def getValue(self):
        valRange = self.sliderRightPos - self.sliderLeftPos - 1
        buttonVal = self.buttonRect.centerx - self.sliderLeftPos
        return int((buttonVal/valRange)*(self.max-self.min)+self.min)
    
    def displayValue(self, screen):
        self.text=self.font.render(
                    f'{self.gameParameter}: {int(self.getValue())}', 
                                    True, "white", None)
        x,y = self.pos
        screen.blit(self.text, (x - self.text.get_width()//2, 
                                y - self.text.get_height()//2-20))