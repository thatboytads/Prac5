
import math
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import time
import RPi.GPIO as GPIO
wait=10
GPIO.setmode(GPIO.BCM)
sampRate =26
def setup():
    GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(15,GPIO.FALLING, callback=change, bouncetime=200)
def change(channel):
    dict ={10: 5,5: 1,1: 10}
    global wait
    if GPIO.event_detected(channel):
       print("button pressed")
       wait=dict[wait]
def print_time_thread():
    """
    This function prints the time to the screen every five seconds
    """
    start_time = time.process_time()
    thread = threading.Timer(wait, print_time_thread)
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()
    output_string= str(math.trunc(start_time))+"s"
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    chan = AnalogIn(mcp, MCP.P1)
    temp= round(((1000*chan.voltage)-500)/10)
    print('{:10}'.format(output_string),'{:10}'.format(str(chan.value)),'{:10}'.format(temp),"C")
    #print(datetime.datetime.now())
    #spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    #cs = digitalio.DigitalInOut(board.D5)
    #mcp = MCP.MCP3008(spi, cs)
    #chan = AnalogIn(mcp, MCP.P1)
    #print("Raw ADC Value: ", chan.value)
    #print("ADC Voltage: " + str(chan.voltage) + "V")


if __name__ == "__main__":
    print("Runtime    Temp Reading      Temp")
    setup()
    print_time_thread() # call it once to start the thread
    # Tell our program to run indefinitely
    while True:
        pass
