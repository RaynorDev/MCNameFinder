import tkinter as tk
from tkinter import ttk
import requests
import string
import random
import datetime
import threading

usernames = []

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

# Generates the username
def generate_random_username(length):
    usernames.clear()
    num_usernames = random.randint(25, 30)
    # Generates 25 - 30 usernames
    for _ in range(num_usernames):
        result = []
        # Using this method to generate clean usernames
        for i in range(length):
            if i % 2 == 0:
                result.append(random.choice(consonants))
            else:
                result.append(random.choice(vowels))
        usernames.append(''.join(result))


# Modifying the username to your liking
def modify_username(username, start_letter, end_letter):
    # Set first letter
    if start_letter and username:
        username = start_letter + username[1:]
    # Set last letter
    if end_letter and len(username) > 1:
        username = username[:-1] + end_letter
    return username

def check_username():
    result_label.config(text=f"Generating txt please wait...")
    length = int(option_var.get())
    generate_random_username(length)

    start_letter = start_entry.get().strip().lower()
    end_letter = end_entry.get().strip().lower()

    # Use threading to run API checks in the background, Decreases lag
    thread = threading.Thread(target=check_usernames_background, args=(usernames, start_letter, end_letter))
    thread.start()

def check_usernames_background(usernames, start_letter, end_letter):
    modified_usernames = [modify_username(username, start_letter, end_letter) for username in usernames]

    results = []

    # Appending usernames with their status to results array
    for username in modified_usernames:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            results.append(f"{username}: is not available")
        elif response.status_code == 404:
            results.append(f"{username}: is available")
        else:
            results.append(f"{username}: Error checking status")

    generatetxt(results)

# Generating the txt with the usernames
def generatetxt(results):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"MCNameFinder_{timestamp}.txt"

    with open(filename, "w") as txt:
        for result in results:
            txt.write(result + "\n")

    result_label.config(text=f"Txt generated at MCNameFinder Folder at time:\n {datetime.datetime.now()}")

# GUI SETUP
root = tk.Tk()
root.title("MCNameFinder")
root.geometry("400x400")

frame_options = tk.Frame(root)
frame_options.pack(pady=20)

option_var = tk.StringVar(value="8")
option_box = ttk.OptionMenu(frame_options, option_var, "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15")
option_box.pack()

label_length = tk.Label(frame_options, text="Username Length")
label_length.pack()

frame_modify = tk.Frame(root)
frame_modify.pack(pady=10)

start_label = tk.Label(frame_modify, text="Start with:")
start_label.grid(row=0, column=0)

start_entry = tk.Entry(frame_modify, width=5)
start_entry.grid(row=0, column=1)

end_label = tk.Label(frame_modify, text="End with:")
end_label.grid(row=0, column=2)

end_entry = tk.Entry(frame_modify, width=5)
end_entry.grid(row=0, column=3)

check_button = tk.Button(root, text="Generate and Check Usernames", command=check_username)
check_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()