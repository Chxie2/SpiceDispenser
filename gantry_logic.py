import serial
import time
# cd: C:\Users\Abhik\Downloads\School\Senior\Sem 2\102B\GUI
from guiNew import run_gui
#from guiNew import measurementsNew
# we set up the connection to the usb we will be writing to (this will change based on laptop and which plug u use)
measurementsCopy = run_gui()

S = serial.Serial('COM5', 115200, timeout=0.050) # COM5 Transmits to bluetooth

# intiate
S.write(bytes("G91\n", 'UTF-8'))
# infinite loop to intake gcode from the terminal

''''  
def dispense(row, col):
    disps = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    disp_no = disps[row][col]
    rowpos = (row-1)*90/2 + offsety
    colpos = (col-1)*33/2 + offsetx
    up_disp = [1, 2, 4, 5, 7, 8]
    side_disp = [3, 6]
    # Upper Dispense: [1 2] [4 5] [7 8] 
    # Operation: Short Down(+Y), Long Right(+X), (Back to original pos) Short Up(-Y), Long Left(-X)
    # Side Dispense: [3; 6]
    # Operation: Long Down(+Y), Short Left(-X), (Back to original pos) Long Up(-Y), Short Right(+X)

    if disp_no in up_disp:
        movey = "Y" + str(rowpos + 5) + "\n"
        movex = "X" + str(colpos + 10) + "\n"
    elif disp_no in side_disp:
        movey = "Y" + str(rowpos + 20) + "\n"
        movex = "X" + str(colpos - 2) + "\n"
    S.write(bytes(movey, 'UTF-8'))
    S.write(bytes(movex, 'UTF-8'))
    nxt_row(row)
    nxt_col(col)'''

global offsetx, offsety, xlimit, ylimmit, measurements, isEmpty
# bring to where pole will not crash with any dispensers
offsetx = 4.5 
offsety = 7
# maximum movment in the gantry
xlimit = 30
ylimit = 80
# measurements = [0, 0, 0, 
#                 5, 0, 0, 
#                 0, 5, 0]
# measurements
isEmpty = False

def nxt_row(row): # Move to dispenser num
    if row == 1:
        movey = "Y" + str(-1*(ylimit)) + "\n" # upper bound
    elif row == 2:
        movey = "Y" + str(-1*((ylimit-offsety)/2 + offsety)) + "\n" # right in the middle of the 2 zones where they will not crash
    elif row == 3:
        movey = "Y" + str(-1*offsety) + "\n" # lower bound
    elif row == 0:
        movey = "Y" + str(0) + "\n"
    print(movey)
    S.write(bytes(movey, 'UTF-8'))

def nxt_col(col): # Move to col number
    if col == 3:
        movex = "X" + str(-1*offsetx)+"\n" # lower bound
    elif col == 2:
        movex = "X" + str(-1*((xlimit-offsetx)/2 + offsetx))+"\n" # right in the middle of the 2
    elif col == 1:
        movex = "X" + str(-1*(xlimit))+"\n" # upper bound 
    elif col == 0:
        movex = "X" + str(0) + "\n"
    print(movex)
    S.write(bytes(movex, 'UTF-8'))

# Region 1, 2, 3, 4
# Regions 2, 3, 4 have the same dispensing movements
def to_region(region_no):
    row = 3 # enter region between 1 and the others
    if region_no in [1, 4]:
        col = 3 # move up so moving up or sideways will result in no crashing
    elif region_no == 2:
        col = 1 # move left to region 2
    elif region_no == 3:
        col = 2 # In the middle of the limit and the x-offset
    elif region_no == 0:
        row = 0
        col = 0
    if region_no in [2, 3, 4]: # change which moves first depending on the region
        print("to region 234")
        nxt_col(col)
        nxt_row(row)
    else:
        print("to region 1")
        nxt_row(row)
        nxt_col(col)

def entr2disp(region_no, enter): # enter area to dispense
    starty = offsety # determine starting position of y based off the region (all regions start at the bottom of the grid)
    if region_no in [1, 4]:
        startx = offsetx # all the starting positions are based off the to_region method
    elif region_no == 2:
        startx = xlimit
    elif region_no == 3:
        startx = (xlimit-offsetx)/2 + offsetx
    # Entering Region
    if enter == True:
        if region_no in [2, 3, 4]:
            movex = "X" + str(-1*(startx - 2.75)) + "\n" # calculate where to move to enter the region and send g-code
            S.write(bytes(movex, 'UTF-8')) # move right to enter dispensing region
        elif region_no == 1:
            movey = "Y" + str(-1*(starty - 6)) + "\n" 
            S.write(bytes(movey, 'UTF-8')) # move down to enter dispensing region
    else:
        if region_no in [2, 3, 4]:
            movex = "X" + str(-1*(startx)) + "\n" 
            S.write(bytes(movex, 'UTF-8'))
        elif region_no == 1:
            movey = "Y" + str(-1*(starty)) + "\n" 
            S.write(bytes(movey, 'UTF-8')) 

def optimize_path(measurements):
    regions = [0, 0, 0, 0, 0, 0]

    return path

# Check Region 1
# Check Region 2 for dual, if not then check region 5, 6
# If dual dispensing Region 2, dispense then, check region 5, 6
# Check Region 3
# Check Region 4

def checkEmpty(arr):
    countEl = 0
    for el in arr:
        if el == 0:
            countEl = countEl + 1
    if countEl == len(arr):
        return False
    else:
        return True


def dispenseRegion(region_no):
    start = True
    while (checkEmpty(measurementsCopy)):
        print("we have 5mL somewhere")

        # getting from region to the 'measurements' array indices of the 2 dispensers in each region
        top234 = region_no - 2 # will be 0 1 2
        bot234 = region_no + 1 # will be 3 4 5
        left1 = region_no + 5 # will be 6
        right1 = region_no + 6 # will be 7
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # this is the 2D matrix such that R2 = 0/3, R3 = 1/4, R4 = 2/5, R1 = 6/7

        # Region 2,3,4
        if region_no in [2, 3, 4]:
            print("R"+str(region_no))

            if start == True:
                to_region(region_no)
                start = False

            # gives mL at locations
            top_mL = measurementsCopy[top234]
            bot_mL = measurementsCopy[bot234]

            # gives row wanted to move to
            top = 1 # will hit both dispensers
            bot = 2 # will just hit bottom dispenser

            # NEITHER DISPENSE
            if top_mL == 0 and bot_mL == 0:
                print("Done with R"+str(region_no))
                break

            # BOTH DISPENSE
            elif top_mL != 0 and bot_mL != 0:
                print("both needed dispense")
                
                # offset to dispense, dispense both rows, exit dispense region
                entr2disp(region_no, True)
                nxt_row(top)
                measurementsCopy[top234] -= 5
                measurementsCopy[bot234] -= 5
                
                if measurementsCopy[top234] != 0 and measurementsCopy[bot234] == 0:
                    entr2disp(region_no, False)
                else:
                    to_region(region_no)
                    

            # TOP DISPENSE
            elif top_mL != 0 and bot_mL == 0:
                print("top needed dispense")
                entr2disp(region_no, False)
                # move to top row location, offset to dispense, dispense, back to home
                nxt_row(bot)
                entr2disp(region_no, True)
                nxt_row(top)
                entr2disp(region_no, False)

                measurementsCopy[top234] -= 5

                if measurementsCopy[top234] == 0:
                    to_region(region_no)

            # BOTTOM DISPENSE
            elif top_mL == 0 and bot_mL != 0:
                print("bottom needed dispense")
                # offset to dispense, dispense through one row up, back to home
                entr2disp(region_no, True)
                nxt_row(bot)
                to_region(region_no)
            
                measurementsCopy[bot234] -= 5
                
        # Region 1
        # Create Regions 5 & 6
        else:
            print("R1")
            if start == True:
                to_region(region_no)
                start = False
            
            # gives mL at locations
            top_mL = measurementsCopy[left1]
            bot_mL = measurementsCopy[right1]
            
            # gives col wanted to move to
            top = 1 # will hit both dispensers
            bot = 2 # will just hit right dispenser

            # NEITHER DISPENSE
            if top_mL == 0 and bot_mL == 0:
                print("Done with R"+str(region_no))
                break

            # BOTH DISPENSE
            elif top_mL != 0 and bot_mL != 0:
                print("both needed dispense")

                # offset to dispense, dispense both rows, exit dispense region
                entr2disp(region_no, True)
                nxt_col(top)
                measurementsCopy[left1] -= 5
                measurementsCopy[right1] -= 5
                
                if measurementsCopy[left1] != 0 and measurementsCopy[right1] == 0:
                    entr2disp(region_no, False)
                else:
                    to_region(region_no)

            # LEFT DISPENSE
            elif top_mL != 0 and bot_mL == 0:
                print("left needed dispense")
                entr2disp(region_no, False)
                # move to top row location, offset to dispense, dispense, back to home
                nxt_col(bot)
                entr2disp(region_no, True)
                nxt_col(top)
                entr2disp(region_no, False)

                measurementsCopy[left1] -= 5
                
                if measurementsCopy[left1] == 0:
                    to_region(region_no+1)

            # RIGHT DISPENSE
            elif top_mL == 0 and bot_mL != 0:
                print("right needed dispense")
                # offset to dispense, dispense through one row up, back to home
                entr2disp(region_no, True)
                nxt_col(bot)
                to_region(region_no)
            
                measurementsCopy[right1] -= 5


while True:
    time.sleep(2) 
    if measurementsCopy[6] != 0 or measurementsCopy[7] != 0:
        dispenseRegion(1)
        print("end of 1")

    time.sleep(2)
    if measurementsCopy[0] != 0 or measurementsCopy[3] != 0:
        dispenseRegion(2)
        print("end of 2")

    time.sleep(2)
    if measurementsCopy[1] != 0 or measurementsCopy[4] != 0:
        dispenseRegion(3)
        print("end of 3")

    time.sleep(2)
    if measurementsCopy[2] != 0 or measurementsCopy[5] != 0:
        dispenseRegion(4)
        print("end of 4")
        
    time.sleep(2)
    print("going home")
    to_region(0)
    break
    
    '''
    dispenseRegion(1)
    dispenseRegion(2)
    dispenseRegion(3)
    dispenseRegion(4)
    print("DONE DISPENSE")

    row = int(input("Row: "))
    col = int(input("Col: "))
    nxt_row(row)
    nxt_col(col)
    reg = int(input("Region No: "))
    to_region(reg)
    ynd = int(input("Enter Dispense (1/0): "))
    if ynd == 1:
        entr2disp(reg)
        yne = int(input("Go Back (1/0): "))
        if yne == 1:
            to_region(reg)
'''
# assume pole is on top left 

# Check if region needs to be dispensed
# Check both dispensers
# if both need, enter -> then dispense both
# if bottom, enter -> dispense
# if top, move to top, enter -> dispense