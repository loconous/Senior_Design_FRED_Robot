from  pycreate2 import Create2
from pycreate2.OI import OPCODES
from time import sleep
import serial

# Create a Create2.
#port = "/dev/ttyUSB0"  # for the raspi
port = "COM9"   # for my laptop
bot = Create2(port)

# # define a movement path
# path = [
#     [-200,-200, 3, 'for'],
#     [-100, 100, 1.6, 'turn'],
#     [   0,   0, 1, 'stop']
# ]

bot.start()
# bot.SCI.write(128)
print("START Mode: Sucessful")
bot.safe()
print("SAFE Mode: Sucessful")

# # path to move
# for lft, rht, dt, s in path:
#     print(s)
#     bot.drive_direct(lft, rht)
#     sleep(dt)

sensor = bot.get_sensors()
levelCharge = sensor.battery_charge
chargestate = sensor.charger_state
print(levelCharge)
print(chargestate)

# bot.full()

# # random MIDI songs I found on the internet
# # they cannot be more than 16 midi notes or really 32 bytes arranged
# # as [(note, duration), ...]
# song = [59, 64, 62, 32, 69, 96, 67, 64, 62, 32, 60, 96, 59, 64, 59, 32, 59, 32, 60, 32, 62, 32, 64, 96, 62, 96]
# song = [76, 16, 76, 16, 76, 32, 76, 16, 76, 16, 76, 32, 76, 16, 79, 16, 72, 16, 74, 16, 76, 32, 77, 16, 77, 16, 77, 16, 77, 32, 77, 16]
# song = [76, 12, 76, 12, 20, 12, 76, 12, 20, 12, 72, 12, 76, 12, 20, 12, 79, 12, 20, 36, 67, 12, 20, 36]
# song = [72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71, 16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]

# print(">> song len: ", len(song)//2)

# # song number can be 0-3
# song_num = 0
# bot.createSong(song_num, song)
# sleep(0.1)
# how_long = bot.playSong(song_num)

# bot.SCI.write(143)
# print("DOCK Mode: Docking")
# #sleep(18)

# chargeFlag = True

# while (chargeFlag):
#     sensor = bot.get_sensors()
#     chargestate = sensor.charger_state
# #    print(chargestate)
#     if(chargeFlag >=0 and chargeFlag <=6):
#         if (chargestate == 2):
#             chargeFlag = False
#             #print(chargestate)
#         else:
#             #print(chargestate)
#             sleep(1)
#     else:
#         #print(chargestate)
#         sleep(1)        
#         pass

# while (chargeFlag):
#     sensor = bot.get_sensors()
#     chargestate = sensor.charger_state
#     print(chargestate)
#     if (chargestate != 0 and chargestate != 99):
#         chargeFlag = False
#     elif (chargestate == 99):
#         bot.SCI.write(143)
#     else:
#         sleep(1)


#count = 0
    # else:
    #     if (count == 45):
    #         bot.SCI.write(143)
    #         count = 0
    #     else:
    #         count += 1
    #         sleep(1)

print('shutting down ... bye')
bot.SCI.write(173)
#bot.drive_stop()
sleep(0.1)

# Close the connection
bot.power()