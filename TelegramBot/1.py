import keyboard, pyperclip
from time import sleep
from win32gui import GetWindowText, GetForegroundWindow

BUFFER = ""

def active_window() -> str:
    print("Paste: ",end="")
    return GetWindowText(GetForegroundWindow())

def paste():
    if active_window().endswith("Avrora") or True:
        BUFFER = pyperclip.paste()
        print(BUFFER)
        BUFFER.replace("    ","")
        for ch in BUFFER:
            keyboard.write(ch)
            sleep(0.2)

keyboard.add_hotkey("ctrl+b",paste)

while True:
    sleep(0.5)