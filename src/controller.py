import pygame
from helpers import *

class Controller:
    def __init__(self, model):
        self.model = model
    
    def control(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.onMouseMove(mouseX,mouseY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.appOn = False
            if event.type == pygame.KEYDOWN:
                if self.onKeyPress(event.key):
                    self.model.initialiseHomeScreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.onMousePress(mouseX,mouseY)
            if self.model.isCustomLevel:
                self.checkSlidersControl()
    
    #GITHUB REPO: all sliders code has been directly adapted from a github repo
    # details in citation
    def checkSlidersControl(self):
        if self.model.isCustomLevel:
            mousePos=pygame.mouse.get_pos()
            mousePressed=pygame.mouse.get_pressed()[0]
            configurationSliders=self.model.configurationSliders
            if not mousePressed:
                for config in configurationSliders:
                    configurationSliders[config].grabbed=False
            for config in configurationSliders:
                slider=configurationSliders[config]
                if slider.buttonRect.collidepoint(mousePos):
                    if mousePressed:
                        slider.grabbed=True
                    else:
                        slider.grabbed=False
                if slider.buttonRect.collidepoint(mousePos):
                    slider.hover()
                if slider.grabbed:
                    slider.moveSlider(mousePos)
                    slider.hover()
                else:
                    slider.hovered = False
            self.model.lives = configurationSliders['lives'].getValue()
            self.model.numOfShapes = (
                configurationSliders['numOfShapes'].getValue())
            self.model.charSize = configurationSliders['charSize'].getValue()
            self.model.gravity = configurationSliders['gravity'].getValue()
            oldSize = self.model.averageShapeSize
            newSize = configurationSliders['averageShapeSize'].getValue()
            if abs(oldSize-newSize)>=1:
                self.model.averageShapeSize = newSize
                self.model.gameElement = self.model.createDemoShape()
    
    def onMouseMove(self, mouseX, mouseY):
        self.model.crosshairX, self.model.crosshairY = mouseX, mouseY
            
    def onMousePress(self,mouseX,mouseY):
        if self.model.activeScreen=='GameScreen':
            if (not self.model.gameOver and not self.model.gamePaused):
                self.model.keypresses +=1
                self.checkForShapeClicks(mouseX,mouseY)
        if self.model.activeScreen=='ConfigureScreen':
            self.checkForButtonClicks(mouseX,mouseY)
    
    def onKeyPress(self,key):
        # print(self.model.activeScreen)
        if  self.model.activeScreen == 'HomeScreen': #self.model.homeScreenOn:
            if key == pygame.K_RETURN:
                self.model.activeScreen = 'GameScreen'
            elif key == pygame.K_RSHIFT or key==pygame.K_LSHIFT:
                self.model.activeScreen = 'ConfigureScreen'
            # self.model.gameScreenOn = True
        
        elif self.model.activeScreen == 'ConfigureScreen':
            if key == pygame.K_RETURN:
                self.model.initialiseHomeScreen()
            
        elif self.model.activeScreen == 'GameScreen':
            keyBoxes = self.model.keyBoxes
            if key == pygame.K_RSHIFT or key==pygame.K_LSHIFT:
                self.model.togglePause()
            if key == pygame.K_RETURN and self.model.gameOver:
                #self.model.gameOver = False TODO: work on this logic
                return True
            elif (key in keyBoxes) and not (self.model.gamePaused):
                self.model.keypresses +=1
                # self.model.hitSound.play()
                self.checkForShapeClicksKeys(key,keyBoxes[key])
    
    def checkForButtonClicks(self,mouseX,mouseY):
        buttons = self.model.levelButtons
        for button in buttons:
            buttonInfo = buttons[button]
            centerX,centerY = buttonInfo[2],buttonInfo[1]
            buttonWidth, buttonHeight = 150, 30
            if (centerX-buttonWidth/2<=mouseX<=centerX+buttonWidth/2 and
                centerY-buttonHeight/2<=mouseY<=centerY+buttonWidth/2):
                self.model.setLevel(button)

    def checkForShapeClicks(self,mouseX,mouseY):
        for shape in self.model.shapes:
            if shape['alive']:
                # Get the shape's screen position
                rotated = [rotatePoint(v, shape['angleX'], 
                                        shape['angleY'], 
                                        shape['angleZ']) 
                                        for v in shape['vertices']]
                projected = [project3dTo2d(v[0], 
                                            v[1], v[2] + shape['z'], 
                                            shape['distance']) 
                                            for v in rotated]
                projected = [(shape['x'] + px, shape['y'] + py) 
                                for px, py in projected]
                
                # Create a bounding box for the shape
                minX = min(p[0] for p in projected)
                maxX = max(p[0] for p in projected)
                minY = min(p[1] for p in projected)
                maxY = max(p[1] for p in projected)
                
                # Check if click is within bounding box
                if (minX <= mouseX <= maxX and minY <= mouseY <= maxY):
                    # More precise check - see if click is inside any face
                    for face in shape['faces']:
                        facePoints = [projected[i] for i in face]
                        if pointInPolygon(mouseX, mouseY, facePoints):
                            self.model.hitSound.play()
                            self.model.explodeShape(shape)
                            break
    
    def checkForShapeClicksKeys(self,key,keyBox):
        for shape in self.model.shapes:
            if shape['alive']:
                # Get the shape's screen position
                rotated = [rotatePoint(v, shape['angleX'], 
                                        shape['angleY'], 
                                        shape['angleZ']) 
                                        for v in shape['vertices']]
                projected = [project3dTo2d(v[0], 
                                            v[1], v[2] + shape['z'], 
                                            shape['distance']) 
                                            for v in rotated]
                projected = [(shape['x'] + px, shape['y'] + py) 
                                for px, py in projected]
                
                # Create a bounding box for the shape
                minX = min(p[0] for p in projected)
                maxX = max(p[0] for p in projected)
                minY = min(p[1] for p in projected)
                maxY = max(p[1] for p in projected)

                boundingBox = (minX,minY,maxX-minX,maxY-minY)
                
                rect1 = pygame.Rect(*keyBox)
                rect2 = pygame.Rect(*boundingBox)
                if rect1.colliderect(rect2):
                    self.model.hitSound.play()
                    self.model.explodeShape(shape)
                    break