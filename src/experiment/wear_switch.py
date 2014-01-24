from device import knownDevices
import time

if __name__ == '__main__':
    switch = knownDevices['switchPlatform'] 
    while True:
    #        switch.setPreset('86205A')
        switch['DUT'].setPosition('86205A')
        time.sleep(5)
    #        switch.setPreset('773D')
        switch['DUT'].setPosition('open')
        time.sleep(5)
    
      
        