import pygame
from helpers import *

class View:
    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((self.model.screenWidth,
                                               self.model.screenHeight))
    
    def draw(self):
        #TODO: add logic draw screen based on app screen
        if self.model.activeScreen=='HomeScreen': #self.model.homeScreenOn:
            self.drawHomeScreen()
        elif self.model.activeScreen == 'GameScreen':
            self.drawGameScreen()
        elif self.model.activeScreen == 'ConfigureScreen':
            self.drawConfigureScreen()
    
    def drawHomeScreen(self):
        self.screen.fill(self.model.colors[0])
        titleFont = pygame.font.SysFont('Courier', 50, bold=True)
        title = titleFont.render('Welcome to Epic ASCII Blaster!',
                                 True,self.model.colors[1])
        self.screen.blit(title,
                         (self.model.screenWidth//2-title.get_width()//2,
                          self.model.screenHeight//2-title.get_height()//2))
        instructionFont = pygame.font.SysFont('Courier', 30, bold=False)
        instruction2 = instructionFont.render(
                    'Press enter to start or shift to configure',True,
                    self.model.colors[1])
        self.screen.blit(instruction2,
                    (self.model.screenWidth//2-instruction2.get_width()//2,
                    (self.model.screenHeight//2+
                    5*instruction2.get_height()//2)+30))
        instruction = instructionFont.render('Use mouse or keyboard',True,
                                             self.model.colors[1])
        self.screen.blit(instruction,
                    (self.model.screenWidth//2-instruction.get_width()//2,
                    (self.model.screenHeight//2+
                    3.5*instruction.get_height()//2)))
        
    #CONFIGURE SCREEN

    def drawConfigureScreen(self):
        self.screen.fill(self.model.colors[0])
        self.drawConfigureScreenTitle()
        self.drawConfigureScreenButtons()
        self.drawConfigureScreenElement()
        self.drawConfigureScreenSliders()
    
    #GITHUB REPO: all sliders code has been adapted from a github repo
    # details in citations
    def drawConfigureScreenSliders(self):
        for slider in self.model.configurationSliders:
            sliderObj=self.model.configurationSliders[slider]
            if self.model.isCustomLevel:
                pygame.draw.rect(self.screen, 
                                 'gray', sliderObj.containerRect, 12)
                pygame.draw.circle(self.screen, 
                                   'blue', sliderObj.buttonRect.center, 12)
                # sliderObj.render(self.screen)
                # sliderObj.displayValue(self.screen)
            else:
                pygame.draw.rect(self.screen, 
                                 'lightgray', sliderObj.containerRect, 12)
                pygame.draw.circle(self.screen, 
                                   'lightblue', 
                                   sliderObj.buttonRect.center, 12)
            sliderObj.displayValue(self.screen)

    
    def drawConfigureScreenTitle(self):
        titleFont = pygame.font.SysFont('Courier',50,bold=True)
        title = titleFont.render("Configure your game",
                                 True,self.model.colors[1])
        moreTextFont=pygame.font.SysFont('Courier',30,bold=False)
        moreText = moreTextFont.render("Press enter to play!",
                                 True,self.model.colors[1])
        self.screen.blit(title,
                         (self.model.screenWidth//2-title.get_width()//2,
                          self.model.screenHeight//8-title.get_height()//2))
        self.screen.blit(moreText,
                         (self.model.screenWidth-400,
                          self.model.screenHeight-50))
    
    def drawConfigureScreenButtons(self):
        buttons = self.model.levelButtons
        for button in buttons:
            buttonInfo = buttons[button]
            centerX,centerY = buttonInfo[2],buttonInfo[1]
            buttonWidth, buttonHeight = 150, 30
            font = pygame.font.SysFont('Courier',20,bold=False)
            text = font.render(buttonInfo[0], True,self.model.colors[1])
            if button==self.model.selectedLevel:
                font = pygame.font.SysFont('Courier',30,bold=True)
                text = font.render(buttonInfo[0], True,self.model.colors[2])
            
            #CHATGPT: drawing a rectangle given centerx, centerY, width, 
            # height & drawing text on it
            textRect =  text.get_rect(
                center=(buttonWidth // 2, buttonHeight // 2))
            rectSurf = pygame.Surface(
                (buttonWidth, buttonHeight), pygame.SRCALPHA)  
            rectSurf.fill((255,255,255,128))    
            # pygame.draw.rect(rectSurf, (255,255,255), rectSurf.get_rect())
            rectSurfRect = rectSurf.get_rect(center=(centerX, centerY))
            rectSurf.blit(text,textRect)
            self.screen.blit(rectSurf, rectSurfRect)

    def drawConfigureScreenElement(self):
        shape = self.model.gameElement
        #adapted from drawShape
        rotated = [rotatePoint(v, shape['angleX'], shape['angleY'], 
                                shape['angleZ']) 
                                for v in shape['vertices']]
        projected = [project3dTo2d(v[0], v[1], v[2] + shape['z'], 
                                    shape['distance']) 
                                    for v in rotated]
        projected = [(shape['x'] + px, shape['y'] + py) 
                        for px, py in projected]
        
        # Sort faces by Z-depth
        faceDepths = [(i, sum(rotated[v][2] for v in face)/len(face)) 
                        for i, face in enumerate(shape['faces'])]
        sortedFaces = sorted(faceDepths, key=lambda x: -x[1])
        
        for faceIdx, _ in sortedFaces:
            face = shape['faces'][faceIdx]
            normal = getNormalVector(face, rotated)
            brightness = (normal[2] + 1) / 2
            
            charIndex = min(len(self.model.asciiChars)-1, 
                            max(0, int(brightness * 
                            (len(self.model.asciiChars)-1))))
            asciiChar = self.model.asciiChars[charIndex]
            points = [projected[i] for i in face]
            self.drawAsciiPolygon(points, asciiChar, 
                                    shape['faceColors'][faceIdx])
        
    #GAME SCREEN

    def drawGameScreen(self):
        if not self.model.gameOver:
            self.screen.fill(self.model.colors[0])
            self.drawShapes()
            self.drawParticles()
            self.drawCrosshair()
            self.drawKeyBoxes()
        self.drawGameText()
        
    def drawAsciiPolygon(self,points,char,color):
        asciiSpacing=self.model.calculateAsciiSpacing()

        minX = min(p[0] for p in points)
        maxX = max(p[0] for p in points)
        minY = min(p[1] for p in points)
        maxY = max(p[1] for p in points)

        charFont = self.model.charFont
        for x in range(int(minX), int(maxX), int(asciiSpacing)):
            for y in range(int(minY), int(maxY), int(asciiSpacing)):
                if pointInPolygon(x, y, points):
                    text = charFont.render(char, True, color)
                    self.screen.blit(text, (x - text.get_width()//2, 
                                            y - text.get_height()//2))

    def drawShapes(self):
        for shape in self.model.shapes:
            if shape['alive']:
                rotated = [rotatePoint(v, shape['angleX'], shape['angleY'], 
                                       shape['angleZ']) 
                                       for v in shape['vertices']]
                projected = [project3dTo2d(v[0], v[1], v[2] + shape['z'], 
                                           shape['distance']) 
                                           for v in rotated]
                projected = [(shape['x'] + px, shape['y'] + py) 
                             for px, py in projected]
                
                # Sort faces by Z-depth
                faceDepths = [(i, sum(rotated[v][2] for v in face)/len(face)) 
                              for i, face in enumerate(shape['faces'])]
                sortedFaces = sorted(faceDepths, key=lambda x: -x[1])
                
                for faceIdx, _ in sortedFaces:
                    face = shape['faces'][faceIdx]
                    normal = getNormalVector(face, rotated)
                    brightness = (normal[2] + 1) / 2
                    
                    charIndex = min(len(self.model.asciiChars)-1, 
                                    max(0, int(brightness * 
                                    (len(self.model.asciiChars)-1))))
                    asciiChar = self.model.asciiChars[charIndex]
                    points = [projected[i] for i in face]
                    self.drawAsciiPolygon(points, asciiChar, 
                                          shape['faceColors'][faceIdx])

    def drawParticles(self):
        for particle in self.model.particles:
            pygame.draw.circle(self.screen, particle['color'],
                               (int(particle['x']), int(particle['y'])), 
                                particle['size'])

    def drawCrosshair(self):
        crosshairX, crosshairY = self.model.crosshairX, self.model.crosshairY 
        pygame.draw.circle(self.screen, self.model.colors[1], 
                           (crosshairX, crosshairY), 8, 2)
        pygame.draw.line(self.screen, self.model.colors[1], 
                         (crosshairX - 15, crosshairY), 
                         (crosshairX + 15, crosshairY), 2)
        pygame.draw.line(self.screen, self.model.colors[1], 
                         (crosshairX, crosshairY - 15), 
                         (crosshairX, crosshairY + 15), 2)
    
    def drawGameText(self):
        width,height = self.model.screenWidth, self.model.screenHeight
        white,red = self.model.colors[1],self.model.colors[2]
        scoreTextFont=pygame.font.SysFont('Courier', 30, bold=False)
        hitsText = scoreTextFont.render(f"Hits: {self.model.hits}", 
                                        True, white)
        accuracyText = scoreTextFont.render(
                        f"Accuracy: {self.model.accuracy}%", 
                                            True, white)
        scoreText = scoreTextFont.render(f"Score: {self.model.score}", 
                                         True, white)
        self.screen.blit(hitsText, (10, 10))
        self.screen.blit(accuracyText, (10, 50))
        self.screen.blit(scoreText, (10, 90))
        helpText = scoreTextFont.render("Click shapes to destroy", True, 
                                              white)
        self.screen.blit(helpText, (width//2 - helpText.get_width()//2, 10))
        livesTextFont=pygame.font.SysFont('Courier', 35, bold=False)
        livesText = livesTextFont.render(f"Lives: {self.model.currentLives}", 
                                         True, red)
        self.screen.blit(livesText, (width - (helpText.get_width()//2+10), 10))
        if self.model.gameOver:
            gameOverFont = pygame.font.SysFont('Courier', 50, bold=False)
            gameOverText = gameOverFont.render("Game Over :(", True, red)
            self.screen.blit(gameOverText, 
                             (width//2 - gameOverText.get_width()//2, 
                              height//2 - gameOverText.get_height()//2))
            restartTextFont = pygame.font.SysFont('Courier', 30, bold=False)
            restartText = restartTextFont.render("Press enter to go home", 
                                                 True, red)
            self.screen.blit(restartText, 
                             (width//2 - restartText.get_width()//2, 
                              height//2 +3* gameOverText.get_height()//2))

#CHATGPT: Used help to change text opacity
    def drawKeyBoxes(self):
        keyBoxes = self.model.keyBoxes
        for key in keyBoxes:
            rect = pygame.Rect(*keyBoxes[key])
            textSurface = self.model.charFont.render(pygame.key.name(key), 
                                                     True, (255, 255, 255))
            textSurface.set_alpha(50)
            self.screen.blit(textSurface, (
                (rect.x + rect.width // 2 - textSurface.get_width() // 2),
                (rect.y + rect.height // 2 - textSurface.get_height() // 2)))
    
