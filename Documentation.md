# Vex V5 Interpreter

# Notes about the program
> This is not a python tutorial. You should understand how to program in Python before using this program. There will not be explanations of standard Python features. 

> This program does not do everything a Vex Robot will do. It allows for movements and printing. 

> Sensors are not yet supported, though differently colored tiles are supported, so personal implementations are possible. 

> This program will not be a 1:1 representation of the Vex Robots. You will need extra setup and some differences between code deployed to this program and code deployed to the Vex Robots. Many of these differences will be later described. 

> Seconds are the only supported unit of time for wait. Just divide Milliseconds / 1000 to get the number of seconds to use in this program. 

> In this documentation, examples will be shown as follows:

    Code goes here

> All examples should be considers sections of code and not entire files. If you use these examples, remember the setup code. 

> Any powershell commands will be shown like this:

    >Command goes here

>If you copy this, do not inclue the "$" symbol. These commands should be put into powershell on a windows machine. 

>The commands I used on Debian GNU/Linux 11 (bullseye) with Bash will be shown like this:
    
    $Command Goes Here

> Other shells may require different commands, which will not be included in this documentation. 

# Setup
> There are a few things you must do to prepare your program and system before using this software. 

>**You need to take the code from your file and copy it into another file. .v5python files include extra details that will cause many problems.**

>Install The Module 
    
    >pip install VexV5Interpreter

    $python3 -m pip install VexV5Interpreter

> At the top of your file, make sure ALL lines above "# Begin project code" (typically line 30) are commented out. If you want to run this again on a Vex Robot, you will need to uncomment these lines.

> You will now want to copy this to the top of your file:

    import VexV5Interpreter

    SECONDS = '\x53'
    FORWARD = '\x46'
    REVERSE = '\x42'
    MM = '\x4D\x4D'
    INCHES = '\x49\x4E'
    DEGREES = '\x44'
    RIGHT = '\x52'
    LEFT = '\x4C'
    GREEN = '\x67'
    RED = '\x72'
    YELLOW = '\x79'

    drivetrain = VexV5Interpreter.Drivetrain(4, 4, 1)
    brain = VexV5Interpreter.Brain()

> This will allow you to use functions like drivetrain.drive_for and brain.screen.print. 

> You will likely want something like this at the top of your file: 

    DRIVE_DISTANCE = 12.25  
    TURN_ANGLE = 71.5

> These constants can be used in your drive and turn functions. This program will require changes to these values, so having a constant at the top of your program is a best practice. 

# Tile
> This class represents the squares the robot drives on.

> If you wish to implement a color sensor, the color of a tile can be read as follows:
    
    tile.color

> The return value will be GREEN ('\x67'), RED ('\x72'), or YELLOW ('\x79)

> To access all tiles used by the program, access the following list: 

    VexV5Interpreter.tiles

> It will be a 2d list comprised of tiles, each with a default color of GREEN. 

> The top left tile can be indexed as follows:

    VexV5Interpreter.tiles[0][0]

> The bottom right will be selected through this operation:

    VexV5Interpreter.tiles[4][4]

> If required, each tile also has these values:

    self.x,
    self.y,
    self.image

# Screen
> This class is automatically created upon creation of a Brain class. 

> This class has 4 methods. print, next_row, clear_screen, and clear_row. 

> There is also a set_cursor method, however it has no function and only is present to prevent errors. 

> For all printing operations, it is best to use a fixed width font in your terminal. This will prevent unexpeted visuals caused by varying widths. 

## Method Descriptions

> Note that the screen should only be accessed through the brain instance made in the setup section. 

### print
> This method takes 1 paramter. It is the value that is printed. 

> This function prints a string to the standard output of the console invoking it. 

> This function does not print a new line.

    screen.print('Hello World!')

> Expected output:

    Hellow World!

### next_row
> This function takes no parameters. 

> This function prints a new line. 

    screen.next_row()

### clear_screen
> This function takes no parameters.

> The screen will not be cleared, however this is present to prevent errors in already written code. 

    screen.clear_screen()

> Expected output:

    PROGRAM MESSAGE: SCREEN CLEARED

### clear_row

> This function takes 1 parameter. 

>1. Row. This is the row to be cleared. 

> The supplied row will not be cleared, however this is to prevent errors in already written code. 

    screen.clear_row(1)

> Expected output:

    PROGRAM MESSAGE: ROW 1 CLEARED

## Example Code using methods in Context

> This is a simple program to print a smiley face pattern to the output. 

    pattern = [
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ]
    for row in pattern:
        for col in row:
            if col == 1:
                screen.print('*')
            else:
                screen.print(' ')
        screen.next_row()

> Expected output:

        * * 
        * *      

       *   *
        *** 

# Brain
> This is a very small class

> It has no methods

> It is only used to access the screen instance as follows:

    brain.screen

# Drivetrain
> This class has 6 methods, though you should only need 4. 

> These methods include in_valid_position, drive, drive_for, turn_for, turn, and draw.

> You should never need to use in_valid_position or draw. 

## Methods
### in_valid_position
> This method takes no parameters. 

> This method returns if the robot is within the constraints of the grid.


    if drivetrain.in_valid_position():
        # do something
    elif not drivetrain.in_valid_position:
        # do something else
### drive
> This method takes 1 parameter. 

1. Direction. This should be either FORWARD or REVERSE

> This method drives the robot forever. Between each spot it moves, the robot will wait the drivetrain.wait_duration, which defaults to 1.  

> It has very few applications within this simulator, as the robot will just drive off of the grid and have an error. 

    drivetrain.drive(FORWARD)

### drive_for
> This method takes 3 parameters. 
>1. Direction. This should be FORWARD or REVERSE. 
>2. Distance. This is the number of tiles the robot will drive in the given direction. 
>3. Unit. This is unused by the function, however is present to prevent errors. 

    drivetrain.drive_for(FORWARD, 1, INCHES)

### turn_for
> This method takes 3 parameters.
>1. Direction. This should be LEFT or RIGHT
>2. Angle. This is the angle that the robot will turn in the given direction. It should be divisible by 90, otherwise you may see unexpected behavior. 
>3. Degrees. This should be DEGREES. This is unused by the methor, however it must be used to prevent errors. 

    drivetrain.turn_for(RIGHT, 90, DEGREES)

### turn
> this method takes 1 parameter. 
>1. Direction. This should be LEFT or RIGHT.
, "pygame", "time"
> This function is not likely useful. The robot will simply turn in forever in the given direction. 

    drivetrain.turn(DIRECTION)

### draw
> This method takes one parameter. 
    
>1. win. This tells pygame, the module used for graphics, which surface to display to. This parameter has a default, so not argument must be provided by the user. 

> This function really shouldn't be used in your code. It is already called whenever the robot moves, and it will cause errors when downloaded to a Vex Robot. 

    drivetrain.draw()

## Example Code using methods in Context

    while True:
        drivetrain.drive_for(FORWARD, 4, INCHES)
        drivetrain.turn(LEFT, 90, DEGREES)
    
## Expected Output
> The robot will drive to each edge, then turn left. 

> This process will repeat forever. 


# Final Words
> Contributions to this module are welcome. The GitHub repository can be found [here](https://github.com/CrispierVase/Vex-V5-Python-Interpreter)