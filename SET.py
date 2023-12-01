import tkinter as tk
import random
import os,sys
from PIL import Image, ImageTk
import time
import pygame #only for the sound when the game finishes

root = tk.Tk()
root.title("Set")

# Set the background color
root.configure(bg="thistle")

# Initialize the mixer
pygame.mixer.init()

def resource_path(relative_path):
        """"Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys. MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

# Specify the directory containing the images
image_dir = resource_path("cards")


# Get a list of all image files in the directory
image_files = [f for f in os.listdir(resource_path("cards")) if f.endswith('.png')]

# Create a 3x4 grid of buttons with gaps and borders
buttons = []
for row in range(3):
    for col in range(4):
        # Choose a random image file
        image_file = random.choice(image_files)
        # Load the image
        image = Image.open(os.path.join(image_dir, image_file))
        # Resize the image
        image = image.resize((200, 150), Image.LANCZOS)
        # Convert it to a format Tkinter can use
        img = ImageTk.PhotoImage(image)
        button = tk.Button(root, image=img, width=200, height=150, bd=4, relief="groove", highlightbackground="white")
        # Keep a reference of the image and its filename
        button.image = img
        button.image_name = image_file
        button.grid(row=row, column=col, padx=5, pady=5)
        buttons.append(button)

# Define a function to handle button clicks
def button_click(button):
    if button["relief"] == "sunken":
        button.config(relief="groove", bd=4, highlightbackground="white")
    else:
        button.config(relief="sunken", bd=4, highlightbackground="black")
    if sum(button["relief"] == "sunken" for button in buttons) == 3:
        image_names = [os.path.splitext(button.image_name)[0] for button in buttons if button["relief"] == "sunken"]
        print(f"Image names: {image_names}")
        
        # Initialize a flag to indicate whether a set was found
        is_set = True

        # Check each position in the strings
        for i in range(4):
            # Get the i-th character of each string
            elements = [name[i] for name in image_names]
            # Count how many times each element appears
            counts = [elements.count(e) for e in elements]
            # If two elements are the same and one is different, print a message and set the flag to False
            if counts.count(2) > 0:
                is_set = False
                if i == 0:
                    print_to_console("Not a set, \nTwo cards have the same number")
                elif i == 1:
                    print_to_console("Not a set, \nTwo cards have the same color")
                elif i == 2:
                    print_to_console("Not a set, \nTwo cards have the same shape")
                elif i == 3:
                    print_to_console("Not a set, \nTwo cards have the same shading")
                
                    

        # If all checks passed (the flag is still True)
        if is_set:
            print_to_console("You found a set!")
            update_sets_found()
            #found a set sound
            pygame.mixer.music.load(resource_path("other/correct.mp3"))
            pygame.mixer.music.play()
            for button in buttons:
                if button["relief"] == "sunken":
                    # Choose a random image file
                    image_file = random.choice(image_files)
                    # Load the image
                    image = Image.open(os.path.join(image_dir, image_file))
                    # Resize the image
                    image = image.resize((200, 150), Image.LANCZOS)
                    # Convert it to a format Tkinter can use
                    img = ImageTk.PhotoImage(image)
                    
                    button.config(image=img, relief="groove", bd=4, highlightbackground="white")
                    button.image = img
                    # Update the button's grid placement using its stored row and column
                    #button.grid(row=button.grid_row, column=button.grid_col, padx=5, pady=5)
                    button.image_name = image_file
        else:  # If not a set
            for button in buttons:
                if button["relief"] == "sunken":
                    button.config(relief="groove", bd=4, highlightbackground="white")

    
# Bind the button click function to each button
for button in buttons:
    button.config(command=lambda b=button: button_click(b))

# Define a function to refresh all images on buttons and start the timer.
def play():
    refresh_images()
    start_timer()
    reset_set_counter()

def refresh_images():
    remove_message()
    for button in buttons:
        if button["relief"] == "sunken":
            button.config(relief="groove", bd=4, highlightbackground="white")
        # Choose a random image file
        image_file = random.choice(image_files)
        # Load the image
        image = Image.open(os.path.join(image_dir, image_file))
        # Resize the image
        image = image.resize((200, 150), Image.LANCZOS)
        # Convert it to a format Tkinter can use
        img = ImageTk.PhotoImage(image)
        
        button.config(image=img)
        button.image = img
        button.image_name = image_file
        
# Load an icon for the refresh button from a specific file location.
refresh_icon_image_path = resource_path("other/refresh.png")
refresh_icon_image = Image.open(refresh_icon_image_path)
refresh_icon_image_resized = refresh_icon_image.resize((200, 150), Image.LANCZOS)
refresh_icon_img = ImageTk.PhotoImage(refresh_icon_image_resized)

# Add a refresh button to the right of your grid of buttons.
refresh_button = tk.Button(root, command=refresh_images,
                           height=150, width=200,
                           compound=tk.TOP,
                           relief="groove",
                           image=refresh_icon_img,
                           bd=4, highlightbackground="black")
refresh_button.image = refresh_icon_img
refresh_button.grid(row=2, column=5)

# Load an icon for the play button from a specific file location.
play_icon_image_path = resource_path("other/play.png")
play_icon_image = Image.open(play_icon_image_path)
play_icon_image_resized = play_icon_image.resize((200, 150), Image.LANCZOS)
play_icon_img = ImageTk.PhotoImage(play_icon_image_resized)

# Add a play button to the right of your grid of buttons.
play_button = tk.Button(root, command=play,
                        height=150, width=200,
                        compound=tk.TOP,
                        relief="groove",
                        bd=4, highlightbackground="black",
                        image=play_icon_img)
play_button.image = play_icon_img
play_button.grid(row=1, column=5)

# Create a label for the timer.
timer_label = tk.Label(root, text="5:00",relief="solid",borderwidth = 5, font=("Ubuntu Light", 40))
timer_label.grid(row=0, column=5)

timer_running = False

# Initialize the timer_running variable and timer_id
timer_running = False
timer_id = None

# Define a function to start the timer.
def start_timer():
    global timer_running, timer_id
    if timer_running:
        reset_timer()
    countdown(300)

def countdown(time_left):
    global timer_running, timer_id
    if time_left > 0:
        timer_running = True
        mins, secs = divmod(time_left, 60)
        timer = '{:2d}:{:02d}'.format(mins, secs) #{:02d} for a timer greater than single digit minutes
        timer_label.config(text=timer)
        # Store the id of the scheduled event
        timer_id = root.after(1000, countdown, time_left - 1)
    else:
        end_timer()

def end_timer():
    global timer_running, timer_id
    # Cancel the scheduled event
    root.after_cancel(timer_id)
    timer_label.config(text="Time's up!")
    #end of game sound
    pygame.mixer.music.load(resource_path("other/end.mp3"))
    pygame.mixer.music.play()
    timer_running = False

def reset_timer():
    global timer_running, timer_id
     # Cancel the current timer if it's running
    if timer_running:
        root.after_cancel(timer_id)
    timer_running = False
    start_timer()
        
# Create a text box
golden_rule = tk.Label(root, text="GOLDEN RULE:\nIf two are, and one is not, then it is not a set",
                       relief="solid",borderwidth = 5, font=("Ubuntu Light", 20), bg="white")
golden_rule.grid(row = 3, column = 3, columnspan = 3)

# Create a variable to keep track of the number of sets found
sets_found = 0

# Create a box with a border
box = tk.Label(root, relief="solid", borderwidth = 5, bg="white", width=200, height=150)
box.grid(row=3, column=0)

# Add text inside the box
text = tk.Label(box, text="Sets Found",font=("Ubuntu Light", 22), bg="white")
text.pack()

# Add the variable inside the box
variable = tk.Label(box, text=str(sets_found),font=("Ubuntu Light", 24), bg="white")
variable.pack()

# Define a function to update the number of sets found
def update_sets_found():
    global sets_found
    sets_found += 1
    variable.config(text=str(sets_found))
    
def reset_set_counter():
    global sets_found
    sets_found = 0
    variable.config(text=str(sets_found))
    
# Create a console box
console_box = tk.Text(root,relief="solid",borderwidth = 5, font=("Ubuntu Light", 20), height = 10, width = 28)
console_box.grid(row = 3, column = 1, columnspan = 2)

# Store the current time whenever a message is printed
message_time = time.time()

def print_to_console(message):
    global message_time
    console_box.insert(tk.END, message + "\n")
    message_time = time.time()

def remove_message():
    if time.time() - message_time >= 7:
        console_box.delete("1.0", tk.END)
    root.after(1000, remove_message)


# Start the timer to remove messages
remove_message()
    
root.mainloop()