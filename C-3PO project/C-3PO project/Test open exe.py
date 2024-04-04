import psutil
import subprocess

def call_app(app = str):
    found = False
    name = {'steam': ['steam.exe', r'C:\Program Files (x86)\Steam\steam.exe'],
            'iracing': ['iRacingUI.exe', r'C:\Program Files (x86)\iRacing\ui\iRacingUI.exe'],
            'simracing studio': ['simracingstudio.exe', r'C:\Program Files\SimRacingStudio 2.0\simracingstudio.exe'],
            'crew chief': ['CrewChiefV4.exe',r'C:\Program Files (x86)\Britton IT Ltd\CrewChiefV4\CrewChiefV4.exe']
            }
    while True:
        for proc in psutil.process_iter():
            if proc.name() == name[app][0]:
                print("app is already running")
                found = True
                break
        break
    if found == False:
        subprocess.Popen([name[app][1]])
        print("Started app")
    print("code finished correctly")
    return 'succes'

call_app('iracing')