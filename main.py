import tkinter as tk
from tkinter import ttk
import aiohttp
import asyncio
import random
import datetime
import threading
import os
from concurrent.futures import ThreadPoolExecutor

usernames = []

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

# Generates the username
def generate_random_username(length, num_usernames):
    usernames.clear()
    for _ in range(num_usernames):
        result = []
        for i in range(length):
            if i % 2 == 0:
                result.append(random.choice(consonants))
            else:
                result.append(random.choice(vowels))
        usernames.append(''.join(result))

# Modifying the username to your liking
def modify_username(username, start_letter, end_letter):
    if start_letter:
        username = start_letter + username[1:]
    if end_letter and len(username) > 1:
        username = username[:-1] + end_letter
    return username

def check_username():
    result_label.config(text=f"Generating txt, please wait...")
    length = int(user_var.get())
    num_usernames = int(amount_var.get())
    generate_random_username(length, num_usernames)

    start_letter = start_entry.get().strip().lower()
    end_letter = end_entry.get().strip().lower()

    # Use threading to run API checks in the background
    thread = threading.Thread(target=check_usernames_background, args=(usernames, start_letter, end_letter))
    thread.start()

async def fetch_username_status(session, username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with session.get(url) as response:
        if response.status == 404:
            return f"{username}: is available"
        elif response.status == 200:
             return f"{username}: is not available"
        return None

async def check_usernames_async(modified_usernames):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_username_status(session, username) for username in modified_usernames]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result]

def check_usernames_background(usernames, start_letter, end_letter):
    modified_usernames = [modify_username(username, start_letter, end_letter) for username in usernames]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(check_usernames_async(modified_usernames))

    generatetxt(results)

def generatetxt(results):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"MCNameFinder_{timestamp}.txt"

    with open(filename, "w") as txt:
        txt.write("DELETED ALL THE ERRORED NAMES \n")
        for result in results:
            txt.write(result + "\n")
    path = os.getcwd()
    result_label.config(text=f"Txt generated at {os.path.abspath(os.path.join(path, os.pardir))} Folder at time:\n {datetime.datetime.now()}")

# GUI SETUP
root = tk.Tk()
root.title("MCNameFinder")
root.geometry("400x400")

frame_options = tk.Frame(root)
frame_options.pack(pady=20)

user_var = tk.StringVar(value="8")
user_box = ttk.OptionMenu(frame_options, user_var, "4", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15")
user_box.pack()

label_length = tk.Label(frame_options, text="Username Length")
label_length.pack()

amount_var = tk.StringVar(value="8")
amount_box = ttk.OptionMenu(frame_options, amount_var, "10", "10", "20", "30", "40", "60", "80", "100")
amount_box.pack(pady=5)

label_amount = tk.Label(frame_options, text="Amount Of Names")
label_amount.pack()

check_button = tk.Button(root, text="Generate and Check Usernames", command=check_username)
check_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Optional features frame
frame_optional = tk.Frame(root)
frame_optional.pack(pady=20)

optional_label = tk.Label(frame_optional, text="Optional Features")
optional_label.grid(row=0, columnspan=4, pady=(0, 10))

start_label = tk.Label(frame_optional, text="Start with:")
start_label.grid(row=1, column=0, padx=(0, 10))

start_entry = tk.Entry(frame_optional, width=5)
start_entry.grid(row=1, column=1)

end_label = tk.Label(frame_optional, text="End with:")
end_label.grid(row=1, column=2, padx=(10, 10))

end_entry = tk.Entry(frame_optional, width=5)
end_entry.grid(row=1, column=3)

root.mainloop()
