import random
import time
import os
import ctypes
import msvcrt
import playsound
import threading

os.system("title Slot Machine")
os.system(f"mode con: cols=41 lines=11")

def header():
    print("\033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[40m \033[105m \033[40m \033[43m \033[40m \033[46m \033[0m")

# --- WINDOW HANDLING ---
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
GWL_STYLE = -16
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
WS_MAXIMIZEBOX = 0x00010000 
ctypes.windll.user32.SetWindowLongW(
    hwnd, 
    GWL_STYLE, 
    WS_VISIBLE | (WS_OVERLAPPEDWINDOW & ~0x00040000 & ~WS_MAXIMIZEBOX)
)
ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0020)
# -----------------------

#starter tickets
tickets = 100
#autospin off by default
auto_spin_active = False
#special combinations and their rewards
two_of_a_kind_reward = 20
three_of_a_kind_reward = 70
special_combinations = {
    (7, 7, 7): 150, #Jackpot 
    (1, 2, 3): 50,  #Sequence
    (3, 2, 1): 55,  #Countdown
    (1, 1, 1): 100, #All ONEs
    (3, 6, 5): 45,  #Year
    (1, 0, 1): 60,  #Binary
}

#sounds
current_dir = os.path.dirname(os.path.abspath(__file__))
jackpot_sound_path = os.path.join(current_dir, 'jackpot.wav')
lost_sound_path = os.path.join(current_dir, 'lost.wav')
win_sound_path = os.path.join(current_dir, 'won.wav')

def play_sound(sound_file):
    threading.Thread(target=playsound.playsound, args=(sound_file,), daemon=True).start()

def jackpot_sound():
    play_sound(jackpot_sound_path)

def lost_sound():
    play_sound(lost_sound_path)

def win_sound():
    play_sound(win_sound_path)
#-----

def spin():
    return (random.randint(1, 7), random.randint(1, 7), random.randint(1, 7))

def check_combination(result):
    return special_combinations.get(result, 0)

def check_for_two_of_a_kind(result):
    return len(set(result)) == 2 #just 2 types of numbers

def check_for_three_of_a_kind(result):
    return len(set(result)) == 1 #just 1 type of number

def display_animation():
    for _ in range(25):
        spinning_result = [random.randint(1, 7), random.randint(1, 7), random.randint(1, 7)]
        print(f"\rSpinning... \033[47m\033[30m{spinning_result}\033[0m", end="", flush=True)
        print()
        print("\n\033[90mGood Luck :)\033[0m", end=" ", flush=True)
        print()
        print("\nYour Tickets:\033[33m", tickets, "\033[0m", end=" ", flush=True)
        time.sleep(0.1)
        clear_terminal()
    clear_terminal()

def display_prizes():
    clear_terminal()
    header()
    print("\033[4mCombinations / Prizes\033[0m")
    print()
    print(" \033[34m[7, 7, 7]\033[0m -> \033[33m150\033[0m \033[33m\033[4mJACKPOT\033[0m")  
    print(" \033[34m[1, 2, 3]\033[0m -> \033[33m50 \033[0m \033[33mSequence\033[0m")                
    print(" \033[34m[3, 2, 1]\033[0m -> \033[33m55 \033[0m \033[33mCountdown\033[0m")                
    print(" \033[34m[1, 1, 1]\033[0m -> \033[33m100\033[0m \033[33mAll ONEs\033[0m")
    print(" \033[34m[3, 6, 5]\033[0m -> \033[33m45 \033[0m \033[33mA Year\033[0m")
    print(" \033[34m[1, 0, 1]\033[0m -> \033[33m60 \033[0m \033[33mOnly Binary\033[0m")
    print()

    while True:
        user_input = input("\033[31mQ\033[0m to return:").strip().upper()
        if user_input == 'Q':
            clear_terminal()
            return
        else:
            print("Invalid input. \033[31mQ\033[0m to return:")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_spin_result(result):
    global tickets
    reward = check_combination(result)
    
    if reward == 150:
        print(f"JACKPOT! You won {reward}\033[0m TICKETS! \033[32m+150\033[0m")
        tickets += reward
        jackpot_sound()
    elif reward == 50:
        print(f"123 Sequence! You won {reward}\033[0m Tickets! \033[32m+50\033[0m")
        tickets += reward
        win_sound()
    elif reward == 55:
        print(f"321 Countdown! You won {reward}\033[0m Tickets! \033[32m+55\033[0m")
        tickets += reward
        win_sound()
    elif reward == 100:
        print(f"All ONEs! You won {reward}\033[0m Tickets! \033[32m+100\033[0m")
        tickets += reward
        win_sound()
    elif reward == 45:
        print(f"That's a Year! You won {reward}\033[0m Tickets! \033[32m+45\033[0m")
        tickets += reward
        win_sound()
    elif reward == 60:
        print(f"Binary Digits! You won {reward}\033[0m Tickets! \033[32m+60\033[0m")
        tickets += reward
        win_sound()
    elif check_for_three_of_a_kind(result):
        print(f"Three of a kind! You won {three_of_a_kind_reward} Tickets! \033[32m+70\033[0m")
        tickets += three_of_a_kind_reward
        win_sound()
    elif check_for_two_of_a_kind(result):
        print(f"Two of a kind! You won {two_of_a_kind_reward} Tickets! \033[32m+20\033[0m")
        tickets += two_of_a_kind_reward
        win_sound()
    else:
        print("\033[31mAw dang it!\033[0m Better luck next time! \033[31m-10\033[0m")
        lost_sound()

def auto_spin():
    global auto_spin_active, tickets
    while auto_spin_active:
        if tickets < 10:
            print("Not enough Tickets! Auto-spin \033[91mOFF\033[0m")
            auto_spin_active = False
            break

        print("Spinning in 3...")
        time.sleep(1)
        if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').upper() == 'A':
            auto_spin_active = False
            clear_terminal()
            print("\nAuto-spin \033[91mOFF\033[0m")
            return
        
        print("Spinning in 2...")
        time.sleep(1)
        if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').upper() == 'A':
            auto_spin_active = False
            clear_terminal()
            print("\nAuto-spin \033[91mOFF\033[0m")
            return

        print("Spinning in 1...")
        time.sleep(1)
        if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').upper() == 'A':
            auto_spin_active = False
            clear_terminal()
            print("\nAuto-spin \033[91mOFF\033[0m")
            return
        
        clear_terminal()
        print("Spinning...")
        time.sleep(0.1)
        tickets -= 10
        display_animation()
        result = spin()
        print("Result:", result)
        handle_spin_result(result)
        time.sleep(1)
        print("Your Tickets:\033[33m", tickets, "\033[0m")


def play_slot_machine():
    clear_terminal()
    header()
    global tickets
    global auto_spin_active
    
    print()
    print("LET'S GO GAMBLING!")
    
    while True:
        if tickets < 10:
            print("Not enough Tickets! You're poor now lol")
            time.sleep(5)
            break
        
        print("\nYou have\033[33m", tickets, "\033[0mTickets.")
        print("\033[36mA\033[0m to Auto-spin")
        user_input = input("\033[32mT\033[0m to Spin, \033[35mY\033[0m to see Prizes, \033[31mQ\033[0m to Quit:").strip().upper()
        
        if user_input == 'Q':
            print("Quitting...")
            break
        elif user_input == 'T':
            header()
            clear_terminal()
            tickets -= 10
            display_animation()
            result = spin()
            print("Result:", result)
            handle_spin_result(result)
            print("Your Tickets:\033[33m", tickets, "\033[0m")
        elif user_input == 'Y':
            display_prizes()
        elif user_input == 'A':
            auto_spin_active = not auto_spin_active
            if auto_spin_active:
                print("Auto-spin \033[92mON\033[0m. A to Stop.")
                auto_spin()
        else:
            print("Invalid input.")

if __name__ == "__main__":
    play_slot_machine()
