# Chana Werblowsky
# COMP 1300 Semester Project

'''
I hereby certify that this program is solely the result of my own work 
[aside from the assistance and code provided for me by Professor Broder] 
and is in compliance with the Academic Integrity policy of the course syllabus 
and the academic integrity policy of the CS department.
'''
import Draw
import random
import Bounce
import math
import time

# Initialize constant values
CANVAS_SIZE = 700    
SOLVENT_DIAMETER = 15  
SOLUTE_DIAMETER =  10   
CELL_CENTER = 350

# Define a Particle class for all of the water and solute (sodium) particles.
class Particle(object):
    
    def __init__(self, x, y, dx, dy, diameter):
        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy
        self.__diameter = diameter
        self.__status = 'none'
    
    def getX(self):  # get the object's x position
        return self.__x
    
    def getY(self):  # get the object's y position
        return self.__y
    
    def getDX(self): # get the object's delta x
        return self.__dx
    
    def getDY(self): # get the object's delta y
        return self.__dy
    
    def getDiameter(self): # get the object's diameter
        return self.__diameter
    
    def getQuadrant(self):  # get the quadrant in which the particle is located relative to the center of the canvas
        # if the particle is at least halfway to the right of and halfway above the center of the canvas: 1st quadrant
        if (self.getX() + (self.getDiameter()/2) >= CELL_CENTER) and \
           (self.getY() + (self.getDiameter()/2) <= CELL_CENTER):       
            return 1
        
        # if the particle is at least halfway to the right of and halfway below the center: 2nd quadrant
        elif (self.getX() + (self.getDiameter()/2) >= CELL_CENTER) and \
           (self.getY() + (self.getDiameter()/2) >= CELL_CENTER):
            return 2
        
        # if the particle is at least halfway to the left of and halfway below the center: 3rd quadrant
        elif (self.getX() + (self.getDiameter()/2) <= CELL_CENTER) and \
           (self.getY() + (self.getDiameter()/2) >= CELL_CENTER):
            return 3
        
        # if the particle is at least halfway to the left of and halfway above the center: 4th quadrant
        elif (self.getX() + (self.getDiameter()/2) <= CELL_CENTER) and \
           (self.getY() + (self.getDiameter()/2) <= CELL_CENTER):
            return 4
    
    def getDistanceFromCenter(self, inside=True):
        
        # If particle is in first quadrant:
        if self.getQuadrant() == 1:
            
            if inside:      # compute distance from upper right corner of particle to center
                return (((self.__x + self.__diameter) - CELL_CENTER)**2 + (self.__y - CELL_CENTER)**2)**(1/2)
            
            else:           # compute distance from lower left corner of particle to center 
                return ((self.__x - CELL_CENTER)**2 + ((self.__y + self.__diameter) - CELL_CENTER)**2)**(1/2)
            
        # If particle is in second quadrant:       
        elif self.getQuadrant() == 2:
            
            if inside:      # compute distance from lower right corner of particle
                return (((self.__x + self.__diameter) - CELL_CENTER)**2 + ((self.__y + self.__diameter) - CELL_CENTER)**2)**(1/2)
            
            else:           # compute distance from upper left corner of particle
                return ((self.__x - CELL_CENTER)**2 + (self.__y - CELL_CENTER)**2)**(1/2)
        
        # If particle is in third quadrant:
        elif self.getQuadrant() == 3:
            if inside:      # compute distance from lower left corner of particle
                return ((self.__x - CELL_CENTER)**2 + ((self.__y + self.__diameter) - CELL_CENTER)**2)**(1/2)
            
            else:           # compute distance from upper right corner of particle
                return (((self.__x + self.__diameter) - CELL_CENTER)**2 + (self.__y - CELL_CENTER)**2)**(1/2)
        
        # If particle is in fourth quadrant:
        elif self.getQuadrant() == 4:
            
            if inside:      # compute distance from upper left corner of particle
                return ((self.__x - CELL_CENTER)**2 + (self.__y - CELL_CENTER)**2)**(1/2)
            
            else:           # compute distance from lower right corner of particle
                return (((self.__x + self.__diameter) - CELL_CENTER)**2 + ((self.__y + self.__diameter) - CELL_CENTER)**2)**(1/2)
            
        
    def getStatus(self):   # get the object's status - either 'none' or 'just exited'
        return self.__status
            
    def setX(self, newX):  # set the object's x position
        self.__x = newX
    
    def setY(self, newY):  # set the object's y position
        self.__y = newY 
    
    def setDX(self, newDX): # set the object's delta x
        self.__dx = newDX
    
    def setDY(self, newDY): # set the object's delta y
        self.__dy = newDY
        
    def setStatus(self, newStatus): # set the object's status
        self.__status = newStatus
    
    def resetStatus(self):          # revert the object's status back to 'none'
        self.__status = 'none'
    
    
# Initialize the amounts of each type of particle depending on tonicity.
def setNumOutsideParticles(tonicity):
    if tonicity == 'HYPERTONIC':    # These numbers don't have any special significance, they just worked out.
        numInsideSolutes = 2
        numInsideWaters = 70
        numOutsideSolutes = 100
        numOutsideWaters = 2            
                                        
    elif tonicity == 'HYPOTONIC':
        numInsideSolutes = 50
        numInsideWaters = 6     
        numOutsideSolutes = 3
        numOutsideWaters = 100
        
    elif tonicity == 'ISOTONIC':
        numInsideSolutes = 15
        numInsideWaters = 35       
        numOutsideSolutes = 30
        numOutsideWaters = 70
    
    return numInsideSolutes, numInsideWaters, numOutsideSolutes, numOutsideWaters

# Create four lists of Particle objects: inside water, outside water, inside solute, and outside solute
def initializeParticleLists(numInsideWaters, numOutsideWaters, numInsideSolutes, numOutsideSolutes, cellRadius):
    insideWaterList = []
    outsideWaterList = []
    insideSoluteList = []
    outsideSoluteList = []
    
    # Create list of insideWater Particle objects
    for i in range(numInsideWaters):
        randomAngle = random.uniform(0, 2 * math.pi)  # with random x and y values within the cell
        x = math.cos(randomAngle)*(random.random()*0.9*cellRadius) + CELL_CENTER 
        y = math.sin(randomAngle)*(random.random()*0.9*cellRadius) + CELL_CENTER
        
        randomAngle = random.uniform(0, 2 * math.pi)  # and a random direction.
        dx = math.cos(randomAngle)                   
        dy = math.sin(randomAngle)
        
        insideWaterList.append(Particle(x, y, dx, dy, SOLVENT_DIAMETER)) # append the new Particle to the insideWaterList
        
    # Create list of outsideWater Particle objects
    for i in range(numOutsideWaters): 
        randomAngle = random.uniform(0, 2 * math.pi)  # with random x and y values outside the cell
        x = math.cos(randomAngle)*(random.uniform(1.1, 1.6)*cellRadius) + CELL_CENTER  
        y = math.sin(randomAngle)*(random.uniform(1.1, 1.6)*cellRadius) + CELL_CENTER
        
        randomAngle = random.uniform(0, 2 * math.pi)  # and a random direction.
        dx = math.cos(randomAngle)
        dy = math.sin(randomAngle)
        
        outsideWaterList.append(Particle(x, y, dx, dy, SOLVENT_DIAMETER)) # append the new Particle to the outsideWaterList
    
    # Create list of insideSolute Particle objects
    for i in range(numInsideSolutes):  
        randomAngle = random.uniform(0, 2 * math.pi)  # with random x and y values within the cell
        x = math.cos(randomAngle)*(random.random()*0.9*cellRadius) + CELL_CENTER
        y = math.sin(randomAngle)*(random.random()*0.9*cellRadius) + CELL_CENTER
        
        randomAngle = random.uniform(0, 2 * math.pi)  # and a random direction.
        dx = math.cos(randomAngle)
        dy = math.sin(randomAngle)
        
        insideSoluteList.append(Particle(x, y, dx, dy, SOLUTE_DIAMETER)) # append the new Particle to the insideSoluteList
    
    # Create list of outsideSolute Particle objects.
    for i in range(numOutsideSolutes):   
        # each near a corner of the canvas 
        x = random.choice([10, 20, 30, CANVAS_SIZE-10, CANVAS_SIZE-20, CANVAS_SIZE-30]) 
        y = random.choice([10, 20, 30, CANVAS_SIZE-10, CANVAS_SIZE-20, CANVAS_SIZE-30])
        
        randomAngle = random.uniform(0, 2 * math.pi)  # with a random direction.
        dx = math.cos(randomAngle)
        dy = math.sin(randomAngle)
        
        outsideSoluteList.append(Particle(x, y, dx, dy, SOLUTE_DIAMETER)) # append the new Particle to the outsideSoluteList
      
    return insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList


# Draw water molecule - 3 circles in an upside-down 'v' shape, in a square frame   
def drawWaterMolecule(p): 
    # Larger cirle (oxygen atom)         
    Draw.filledOval(p.getX() + (SOLVENT_DIAMETER/6), p.getY(), (3/4)*SOLVENT_DIAMETER, (3/4)*SOLVENT_DIAMETER)   
    # smaller circle to the left and below (hydrogen atom)
    Draw.filledOval(p.getX(), p.getY() + (3/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER)  
    # smaller circle to the right and below (hydrogen atom)
    Draw.filledOval(p.getX() + ((3/5)*SOLVENT_DIAMETER), p.getY() + (3/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER)  
    
# Draw the canvas
def drawBoard(insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList, innerConcentration, outerConcentration, cellRadius, tonicity):
    Draw.clear()
    
    Draw.setBackground(Draw.RED)  
    
    # Draw red blood cell
    Draw.setColor(Draw.color(170, 5, 50))
    Draw.filledOval(CELL_CENTER-cellRadius, CELL_CENTER-cellRadius, cellRadius*2, cellRadius*2)
    Draw.setColor(Draw.BLACK)
    Draw.oval(CELL_CENTER-cellRadius, CELL_CENTER-cellRadius, cellRadius*2, cellRadius*2)
    
    # Label cell and blood vessel
    Draw.setFontBold(0)     
    Draw.setColor(Draw.PINK)
    Draw.setFontSize(20)
    Draw.string("RED BLOOD VESSEL", 10, 10)
    Draw.string("RED BLOOD CELL", 240, 320)    
    
    # Display tonicity
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(30)
    Draw.setFontFamily('Century Gothic')
    Draw.string(tonicity, 240, 45)      

    # Display inner and outer solute concentrations
    Draw.setFontSize(14)
    Draw.string('Inner Solute Concentration: ' + str((innerConcentration*10000//1)/100) + ' %', 10, CANVAS_SIZE-150)
    Draw.string('Outer Solute Concentration: ' + str((outerConcentration*10000//1)/100) + ' %', 10, CANVAS_SIZE-125)
    
    # Draw a key to identify water and sodium particles
    Draw.setFontSize(8)
    Draw.string(' = water molecule', CANVAS_SIZE-135, CANVAS_SIZE-149)
    Draw.string(' = sodium ion', CANVAS_SIZE-135, CANVAS_SIZE-129)
    
    Draw.setColor(Draw.BLUE) # draw water molecule
    Draw.filledOval(CANVAS_SIZE-150 + (SOLVENT_DIAMETER/6), CANVAS_SIZE-150, (3/4)*SOLVENT_DIAMETER, (3/4)*SOLVENT_DIAMETER)  
    Draw.filledOval(CANVAS_SIZE-150, CANVAS_SIZE-150 + (3/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER)  
    Draw.filledOval(CANVAS_SIZE-150 + ((3/5)*SOLVENT_DIAMETER), CANVAS_SIZE-150 + (3/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER, (2/5)*SOLVENT_DIAMETER)    
    
    Draw.setColor(Draw.YELLOW) # draw sodium ion
    Draw.filledRect(CANVAS_SIZE-148, CANVAS_SIZE-125, SOLUTE_DIAMETER, SOLUTE_DIAMETER)
    
    # Draw each water molecule
    Draw.setColor(Draw.BLUE)       
    for p in insideWaterList:
        drawWaterMolecule(p)
        
    for p in outsideWaterList:
        drawWaterMolecule(p)
    
    # Draw each solute particle (sodium ion)  
    Draw.setColor(Draw.YELLOW)
      
    for p in insideSoluteList:
        Draw.filledRect(p.getX(), p.getY(), SOLUTE_DIAMETER, SOLUTE_DIAMETER)
        
    for p in outsideSoluteList:
        Draw.filledRect(p.getX(), p.getY(), SOLUTE_DIAMETER, SOLUTE_DIAMETER)
      
    Draw.show()
    
 
# Move particle by adding its dx to its x and its dy to its y 
def moveParticle(p, x, y, dx, dy): 
    p.setX(x + dx)
    p.setY(y + dy)
    
    
# Check if particle hit canvas edge, and if so, bounce it off.
def bounceOffCanvasEdgeIfHit(p, x, y, particleDiameter):
    xHit = True
    yHit = True
    
    if x <= 0:             # First, move particle inward slightly if it went off the right edge 
        p.setX(0)
    
    elif x + particleDiameter >= CANVAS_SIZE: # or left edge of the canvas.
        p.setX(CANVAS_SIZE - particleDiameter)
        
    else: xHit = False     # if it hit neither the right nor the left edge, its x hasn't hit the canvas's x border.
    
    if y <= 0:             # Move the particle inward slightly if it went off the top edge 
        p.setY(0)
        
    elif y + particleDiameter >= CANVAS_SIZE:  # or bottom edge of the canvas.
        p.setY(CANVAS_SIZE - particleDiameter)
        
    else: yHit = False      # if it hit neither the top nor the bottom, its y hasn't hit the canvas's y border.
    
    if xHit:               # If the particle hit the right or left edge of the canvas, negate its dx.
        p.setDX(-p.getDX())
    if yHit:               # If it hit the top or bottom edge, negate its dy.
        p.setDY(-p.getDY())  

# Check if inner particle has hit the membrane (using the Particle method to get its distance from the center).
def hitMembraneFromInside(particle, cellRadius):
    return particle.getDistanceFromCenter() >= cellRadius          

# Check if outer particle has hit the membrane (using the Particle method to get its distance from the center).
def hitMembraneFromOutside(particle, cellRadius):       
    return particle.getDistanceFromCenter(False) <= cellRadius

# Determine whether the given outer particle should enter the cell
def shouldEnter(tonicity, concentrationSoluteInside, concentrationSoluteOutside):
# (the higher the bounceFactor, the less likely the particle is to enter)
    
    if tonicity == 'HYPOTONIC': # and there should be a net movement of water into the cell:
        # if for some reason there's a higher solute concentration outside than inside, raise the bounceFactor a little
        if concentrationSoluteInside < concentrationSoluteOutside:  
            bounceFactor = 0.3  
        # otherwise, make the particle very likely to enter
        else:
            bounceFactor = 0.1 
            
    elif tonicity == 'HYPERTONIC': # and there should be a net movement of water out of the cell:
        # if for some reason there's a higher solute concentration inside than outside, lower the bounceFactor a little
        if concentrationSoluteInside > concentrationSoluteOutside:
            bounceFactor = 0.7  
        # otherwise, make it very unlikely that the particle will enter
        else:
            bounceFactor = 0.9 
            
    elif tonicity == 'ISOTONIC':
        bounceFactor = 0.5
    
    return random.random() > bounceFactor  # only return True if the random float is higher than the particle's bounceFactor
 
# Determine whether the given inner particle should enter the cell   
def shouldExit(tonicity, concentrationSoluteInside, concentrationSoluteOutside):

    if tonicity == 'HYPOTONIC':    # and there should be a net movement of water into the cell:
        # in the unlikely case of higher solute concentration outside, make the particle a little more likely to exit
        if concentrationSoluteInside < concentrationSoluteOutside:           
            bounceFactor = 0.7
        # otherwise, make it very unlikely that the particle will leave the cell   
        else: 
            bounceFactor = 0.9
           
    # Since the ratio of particles per pixel area is greater inside the cell than out,
    # each INNER particle is more likely to hit the membrane than each OUTER particle,
    # (especially as the cell decreases).
    # Therefore, in order to achieve a speed of cell-shrinking in hypertonic solution 
    # apporoximately equal to that of the cell growing in hypotonic solution, 
    # the bounceFactors are adjusted to make it less likely for an inner particle
    # to exit in hypertonic solution than an outer particle to enter in a hypotonic solution.
                     
    elif tonicity == 'HYPERTONIC': # and there should be a net movement of water out of the cell:
        # in the unlikely case of higher solute concentration inside, make it more unlikely that particle will leave cell
        if concentrationSoluteInside > concentrationSoluteOutside:
            bounceFactor = 0.9
        # otherwise, make it somewhat unlikely that particle will leave cell
        else:   
            bounceFactor = 0.5  
            
    elif tonicity == 'ISOTONIC':
        # bounceFactor higher than isotonic bounceFactor in the shouldEnter() function because water molecules hit more often from inside
        bounceFactor = 0.7  
        
    return random.random() > bounceFactor # only return True (that should leave) if random float is higher than bounceFactor
           

# Bounce inner particle off membrane using Bounce module.
def bounceOffInsideOfMembrane(p, cellRadius):          
    Bounce.bounce(CELL_CENTER, CELL_CENTER, cellRadius, p, True)

# Bounce outer particle off membrane using Bounce module.
def bounceOffOutsideOfMembrane(p, cellRadius):
    Bounce.bounce(CELL_CENTER, CELL_CENTER, cellRadius, p)

# Check if particle hit cell membrane, and if so, determine whether it should pass through or bounce off
def determineActivityAtMembrane(p, cellRadius, tonicity, concentrationSoluteInside, concentrationSoluteOutside, insideWaterList, outsideWaterList, numWatersExited, numWatersEntered, solute, inside, hitMembraneFromInside, hitMembraneFromOutside=False):
    
    # if particle is a solute particle, just bounce off if hit    
    if solute and hitMembraneFromInside:    
        bounceOffInsideOfMembrane(p, cellRadius)      
        
    elif solute and hitMembraneFromOutside:  
        bounceOffOutsideOfMembrane(p, cellRadius)   
  
    # If particle is water, invoke the shouldExit() or shouldEnter() function 
    # to determine whether, if hit, it should bounce off or pass through
    
    elif not solute and hitMembraneFromInside: # if hit from inside:
        
        if shouldExit(tonicity, concentrationSoluteInside, concentrationSoluteOutside): 
            
            insideWaterList.remove(p)  # remove Particle from insideWaterList
            outsideWaterList.append(p) # and append it to outsideWaterList
            
            # invoke transition() function from Bounce module to bring particle out
            Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2)
            
            numWatersExited += 1    # increase count of number of waters exited
            p.setStatus('just exited')   # set Particle attribute 'status' to 'just exited'     
        
        else: # otherwise, bounce
            bounceOffInsideOfMembrane(p, cellRadius)
    
    elif not solute and hitMembraneFromOutside: # if hit from outside:

        if shouldEnter(tonicity, concentrationSoluteInside, concentrationSoluteOutside):
            
            outsideWaterList.remove(p)  # remove Particle from outsideWaterList
            insideWaterList.append(p)   # and append it to insideWaterList
            
            # invoke transition() function from Bounce module to bring particle in
            Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2, False)

            numWatersEntered += 1 # increase count of number of waters exited
            
        else: # otherwise, bounce
            bounceOffOutsideOfMembrane(p, cellRadius)
            
    return numWatersExited, numWatersEntered


# Increase or decrease the cell radius according to the amount of water molecules that have entered or left the cell since the last iteration.
def adjustCellRadius(tonicity, cellRadius, insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList, numWatersExited, numWatersEntered):
    
    if tonicity == 'HYPERTONIC': # and cell should be shrinking:
        
        # Decrease the previous radius such that each outgoing particle causes an 8 square pixel decrease in cell area
        newCellRadius = cellRadius - ((numWatersExited * 8/ math.pi) ** (0.5))  

        newToOldRadiusRatio = newCellRadius / cellRadius # compute ratio of new to old radius
        
        cellRadius = newCellRadius                       # update cellRadius
        
        # Move the inner particles slightly inward if they fall between the old and new circumference of the cell    
        for p in insideWaterList:           
                
            if p.getDistanceFromCenter() >= cellRadius:  # if outside of or touching new radius:
                Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2, False)

        for p in insideSoluteList:
            
            if p.getDistanceFromCenter() >= cellRadius:  # if outside of or touching new radius:
                Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2, False)
          
        
    
    elif tonicity == 'HYPOTONIC':
     
        # Increase the previous radius such that each incoming particle causes an 8 square pixel increase in cell area
        newCellRadius = cellRadius + ((numWatersEntered * 8 / math.pi) ** (0.5)) 
        
        newToOldRadiusRatio = newCellRadius / cellRadius # compute the ratio of new to old cell radius
        
        # Move the outer particles slightly outward if they fall between the old and new circumference of the cell
        for p in outsideWaterList:      
            
            if p.getDistanceFromCenter() <= newCellRadius: # if within or touching radius:
                Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2)
   
        for p in outsideSoluteList:
            
            if p.getDistanceFromCenter() <= newCellRadius: # if within or touching radius:
                Bounce.transition(CELL_CENTER, CELL_CENTER, cellRadius, p, p.getDiameter()/2)
                
        cellRadius = newCellRadius     # update cellRadius
        
    return cellRadius  # return updated cellRadius


# Run the simulation, depending on the tonicity given.    
def runExperiment(tonicity):

    cellRadius = CANVAS_SIZE / 4  # initialize cellRadius to be a quarter of the canvas
    
    # Initialize the number particles of each type by invoking setNumOutsideParticles() 
    numInsideSolutes, numInsideWaters, numOutsideSolutes, numOutsideWaters = setNumOutsideParticles(tonicity) 
       
    # Create and store particle lists by invoking initializeParticleLists()
    insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList = \
        initializeParticleLists(numInsideWaters, numOutsideWaters, numInsideSolutes, numOutsideSolutes, cellRadius)
    
    # Initialize solute concentration inside and outside cell (solute per water) based on newly created particle lists
    concentrationSoluteInside = len(insideSoluteList) / len(insideWaterList)                   
    concentrationSoluteOutside = len(outsideSoluteList) / len(outsideWaterList)  
    
    # Draw the canvas once to reflect initial conditions
    drawBoard(insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList, concentrationSoluteInside, concentrationSoluteOutside, cellRadius, tonicity)
    
    numTimesLooped = 0
        
    while True: 
        
        numTimesLooped += 1
        
        # each time through the loop, reset amount of waters entered and exited to 0 
        numWatersExited = 0   
        numWatersEntered = 0      
            
        for p in insideWaterList:  # for each inner water Particle:
            
            moveParticle(p, p.getX(), p.getY(), p.getDX(), p.getDY())  # move it
            
            # if hit canvas edge, bounce
            bounceOffCanvasEdgeIfHit(p, p.getX(), p.getY(), p.getDiameter()) 
            
            # if hit membrane, bounce or pass through (according to determineActivityAtMembrane())
            numWatersExited, numWatersEntered = determineActivityAtMembrane(p, cellRadius, tonicity, concentrationSoluteInside, concentrationSoluteOutside, insideWaterList, outsideWaterList, numWatersExited, numWatersEntered, False, True, hitMembraneFromInside(p, cellRadius))

        
        for p in outsideWaterList: # for each outer water Particle:
            moveParticle(p, p.getX(), p.getY(), p.getDX(), p.getDY()) # move it
            
            # if hit canvas edge, bounce
            bounceOffCanvasEdgeIfHit(p, p.getX(), p.getY(), p.getDiameter()) 
            
            if p.getStatus() != 'just exited': # if particle has not just left the cell during this iteration:
                
                # if hit membrane, bounce or pass through (according to determineActivityAtMembrane())              
                numWatersExited, numWatersEntered = determineActivityAtMembrane(p, cellRadius, tonicity, concentrationSoluteInside, concentrationSoluteOutside, insideWaterList, outsideWaterList, numWatersExited, numWatersEntered, False, False, False, hitMembraneFromOutside(p, cellRadius))
        
            else: p.resetStatus() # if particle has just left cell, do nothing, but reset its status to none
            
        for p in insideSoluteList:  # for each inner solue Particle:
            moveParticle(p, p.getX(), p.getY(), p.getDX(), p.getDY()) # move it
            
            # if hit canvas edge, bounce
            bounceOffCanvasEdgeIfHit(p, p.getX(), p.getY(), p.getDiameter()) 

            # if hit membrane, bounce
            determineActivityAtMembrane(p, cellRadius, tonicity, concentrationSoluteInside, concentrationSoluteOutside, insideWaterList, outsideWaterList, numWatersExited, numWatersEntered, True, True, hitMembraneFromInside(p, cellRadius))
            
            
        for p in outsideSoluteList: # for each outer solute Particle
            moveParticle(p, p.getX(), p.getY(), p.getDX(), p.getDY()) # move it
            
            # if hit canvas edge, bounce
            bounceOffCanvasEdgeIfHit(p, p.getX(), p.getY(), p.getDiameter()) 
            
            # if hit membrane, bounce
            determineActivityAtMembrane(p, cellRadius, tonicity, concentrationSoluteInside, concentrationSoluteOutside, insideWaterList, outsideWaterList, numWatersExited, numWatersEntered, True, False, False, hitMembraneFromOutside(p, cellRadius))
            
        
        
        # Update solute concentration inside and outside cell (solute per water)
        concentrationSoluteInside = len(insideSoluteList) / len(insideWaterList)                 
        concentrationSoluteOutside = len(outsideSoluteList) / len(outsideWaterList)           
    
        
        # Update the cell radius by invoking adjustCellRadius()
        cellRadius = adjustCellRadius(tonicity, cellRadius, insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList, numWatersExited, numWatersEntered)
            
    
        # Draw the canvas   
        drawBoard(insideWaterList, outsideWaterList, insideSoluteList, outsideSoluteList, concentrationSoluteInside, concentrationSoluteOutside, cellRadius, tonicity)        
            
        # Break out of loop if there is virtually no water left in/out, if cell has exceeded its max/min size, or if it has reached equilibrium:
        
        # if most of the water has left the cell or the radius has shrunken sufficiently...
        if len(insideWaterList) < 3 or cellRadius < (CANVAS_SIZE / 14):     
            Draw.setColor(Draw.BLACK)
            Draw.setFontBold(2)      # display a message that the cell has shriveled, wait 5 seconds, and then return 
            Draw.setFontSize(40)                                
            Draw.string('CELL SHRIVELED!', 145, 260)
            Draw.show()
            time.sleep(5)
            return        
        
        # if most of the water has entered the cell or the cell radius has expanded sufficiently...
        elif len(outsideWaterList) < 2 or cellRadius > (CANVAS_SIZE * 0.38):
            Draw.setColor(Draw.BLACK)
            Draw.setFontBold(2)      # display a message that the cell has ruptured and then return (no need to wait because end of simulation)
            Draw.setFontSize(40)
            Draw.string('CELL RUPTURED!', 145, 260)
            Draw.show()
            return    
        
        # if the intercellular and extracellular fluid are equally concentrated and a few seconds have elapsed...   
        elif (concentrationSoluteInside * 100 // 1) == (concentrationSoluteOutside * 100 // 1) and numTimesLooped > 250: 
                Draw.setColor(Draw.BLACK)
                Draw.setFontSize(40)
                Draw.setFontBold(2)   # display a message that the cell and surroundings have reached equilibrium, wait 5 seconds, and then return
                Draw.string('EQUILIBRIUM', 190, 260)  
                Draw.show()
                time.sleep(5)
                return        
                
    return    # if returned from while loop, return from runExperiment()

# Run the simulation with hypertonic solution, isotonic solution, and then hypotonic solution.       
def main(): 
    
    Draw.setCanvasSize(CANVAS_SIZE, CANVAS_SIZE)
    
    runExperiment('HYPERTONIC')
    
    runExperiment('ISOTONIC')
    
    runExperiment('HYPOTONIC')
    
    
main()