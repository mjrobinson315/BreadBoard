from gpiozero import DigitalOutputDevice, Button, Buzzer, LED
from time import sleep
import os

# 0 - g mid
# 1 - f top l
# 2 - a top
# 3 - b top r
# 4 - dp
# 5 - c bot r
# 6 - d bot
# 7 - e bot l

led = LED(12)
button = Button(22)
buzzer = Buzzer(27)

def data_string(data):
    if data == 1:
        return "00111000" #56
    elif data == 2:
        return "11001101"
    elif data == 3:
        return "01101101"
    elif data == 4:
        return "00101011"
    elif data == 5:
        return "01100111"
    elif data == 6:
        return "11100111"
    elif data == 7:
        return "00101100"
    elif data == 8:
        return "11101111"
    elif data == 9:
        return "01111111"
    elif data == 0:
        return "11101110"
    elif data == 99:
        return "00000000"
    else:
        return "00000000"

data_pin = DigitalOutputDevice("GPIO19")
clock_pin = DigitalOutputDevice("GPIO21")
latch_pin = DigitalOutputDevice("GPIO20")

latch_pin.off()
    #read through variable
def shift_out(value):
    for x in value:
        if x == "1":
            data_pin.on()
        else:
            data_pin.off()
        clock_pin.on()
        clock_pin.off()
    latch_pin.on()
    latch_pin.off()

reset = 99
cnt = 0
spd = 0.4
rnd = 1
rnds = {
    "rnd1": False,
    "rnd2": False,
    "rnd3": False,
    "rnd4": False
}
rnd_pause = False 
bz_flag = False
attempts = 0
attempt_pause = False

def bz_func(bz_flag):
    if bz_flag == False:
        buzzer.off()
        led.off()
    else:
        buzzer.on()
        led.blink(0.2,0.2)
def get_highscore(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        return last_line
def set_highscore(filename, score):
    with open(filename, 'a') as file:
        file.write(score + '\n')
def game_reset(score):
    bz_func(False)
    shift_out(data_string(reset))
    spd = 0.4
    rnd = 1
    rnds["rnd1"] = False
    rnds["rnd2"] = False
    rnds["rnd3"] = False
    rnds["rnd4"] = False
    rnd_pause = False
    cnt = 0
    if score < int(hs):
        set_highscore("TimerHighScore.txt", str(attempts))
        print("Congrats on your highscore!")
    elif score > int(hs):
        print("Better luck next time.")

hs = get_highscore("TimerHighScore.txt")
shift_out(data_string(reset))
print("Try to stop the display on 0!")
print("There will be " + str(spd) + " seconds between numbers in Round 1.")
print("The current highscore is " + hs + ".")
print("Hold the button to begin, release the button to stop the display! Good luck!")
while True:
    if button.is_pressed:
        bz_flag = False
        bz_func(bz_flag)
        rnd_pause = False
        attempt_pause = False
        shift_out(data_string(cnt%10))
        sleep(spd)
        cnt += 1
    if cnt > 0 and cnt%10==1 and button.is_active==False and rnd_pause == False and rnds["rnd"+str(rnd)]==False:
        bz_flag = True
        bz_func(bz_flag)
        print(" ")
        print("You're the WINNER of round " + str(rnd) + "!!!")
        spd = spd/2
        print("The time between numbers has been set to " + str(spd) + " seconds!")
        rnds["rnd"+data_string(rnd)] = True
        rnd+=1
        if rnd < 5:
            print("Round " + str(rnd) + " is ready.")
        if rnd == 5:
            print(" ")
            print("Thanks for playing! It took " + str(attempts) + " in total to complete all 4 rounds")
            print("The game will reset. Please wait...")
            game_reset(attempts)
            attempts = 0
            sleep(2)
            print("The game has been reset!")
            hs = get_highscore("TimerHighScore.txt")
            print("The current highscore is " + hs + ".")
        rnd_pause = True
    elif button.is_active==False and attempt_pause == False:
        attempt_pause = True
        attempts += 1
        
