import tkinter as tk
from tkinter import messagebox
from functools import partial

def init_instruction_screen():
    window = tk.Tk()
    window.geometry("400x600")
    window.title("Wordle Solver")
    window.resizable(False, False)
    window["bg"] = "#424242"

    title = tk.Label
        window,
        text="Wordle Solver", bg="#424242", fg="#d9d9d9", font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    frame = tk.Frame(
        window,w
        bg="#2b2b2b",
        relief="solid"
    )
    frame.place(x=30, y=80, width=340, height=400)

    title = tk.Label(
        frame,
        text="Instructions:",
        font=("Arial", 14, "bold"),
        fg="#d9d9d9",
        bg="#2b2b2b",
        anchor="center"
    )
    title.pack(pady=(20, 5))

    body = tk.Label(
        frame,
        pady=5,
        text=(
            "1. Make a guess on your Wordle.\n"
            "2. Enter that guess where prompted.\n"
            "3. Select the colors that match\n"
            "   the feedback from Wordle.\n"
            "4. Enter the next word.\n" 
            "5. Repeat the process!"
        ),
        justify="left",
        bg="#2b2b2b",
        fg="#d9d9d9",
        font=("Arial", 12),
        wraplength=320,  # Ensures text wraps within the frame width
        anchor="nw"  # Aligns text to the top-left corner
    )
    body.pack(padx=10, pady=10)

    frame_buttons = tk.Frame(window, bg="#424242")
    frame_buttons.place(x=60, y=500, width=340, height=80)

    play_button = tk.Button(
        frame_buttons,
        text="PLAY",
        fg="black",
        bg="#86E44C",
        font=("Arial", 15),
        command=lambda: wordle_solver_gui(window))

    play_button.grid(row=0, column=0, padx=10)

    stats_button = tk.Button(
        frame_buttons,
        text="STATS",
        fg="black",
        bg="#86E44C",
        font=("Arial", 15),
        command=partial(stats_screen_gui, window))
    
    stats_button.grid(row=0, column=1, padx=10)

    quit_button = tk.Button(
        frame_buttons,
        text="QUIT",
        fg="black",
        bg="#E6494B",
        font=("Arial", 15),
        command=lambda: window.quit() if messagebox.askokcancel("Quit", "Do you really want to quit?") else None)
    
    quit_button.grid(row=0, column=2, padx=10)

    # Adding hover effects for buttons
    play_button.bind("<Enter>", lambda e: e.widget.config(bg="#4CAF50"))
    play_button.bind("<Leave>", lambda e: e.widget.config(bg="#86E44C"))

    stats_button.bind("<Enter>", lambda e: e.widget.config(bg="#4CAF50"))
    stats_button.bind("<Leave>", lambda e: e.widget.config(bg="#86E44C"))

    quit_button.bind("<Enter>", lambda e: e.widget.config(bg="#FF6347"))  # Tomato color for better visual indication
    quit_button.bind("<Leave>", lambda e: e.widget.config(bg="#E6494B"))

    window.mainloop()  


def wordle_solver_gui(window):
    window = tk.Tk()
    window.geometry("520x800")
    window.title("Solver Interface")
    window.resizable(False, False)
    window["bg"] = "#031f28"

    title = tk.Label(
            window,
            fg="#d9d9d9",
            bg="#424242",
            text="Guess!",
            font=("Arial", 16, "bold"),
            anchor="center"
        )
    title.pack(pady=(10, 5))  

    canvas = tk.Canvas(
        window, 
        bd=0,
        highlightthickness=0,
        width=465,
        height=710,
        bg="#2b2b2b"
    )
    canvas.pack(pady=20)
    
    # Draw circles and add text
    circle_diameter = 60
    spacing_x = 90  
    spacing_y = 115
    start_x = 20  
    y = 30

    # Store all circle and text IDs
    all_circles = []
    all_texts = []
    current_focus = 0  # Keep track of which circle we're on

    def key_press(event):
        nonlocal current_focus
        
        # Only process if we have circles to work with
        if not all_texts:
            return
            
        # Handle backspace
        if event.keysym == 'BackSpace':
            if current_focus > 0:
                current_focus -= 1
                canvas.itemconfig(all_texts[current_focus], text="")
            return

        # Handle letter keys
        if event.char.isalpha():
            # Update current circle's text
            canvas.itemconfig(all_texts[current_focus], text=event.char.upper())
            if current_focus < len(all_texts) - 1:
                current_focus += 1

    def circle_click(event):
        # Find which circle or text was clicked
        clicked_id = canvas.find_closest(event.x, event.y)[0]
        
        # If we clicked text, get its index and use the corresponding circle
        if clicked_id in all_texts:
            text_index = all_texts.index(clicked_id)
            circle_id = all_circles[text_index]
        # If we clicked circle, use it directly
        elif clicked_id in all_circles:
            circle_id = clicked_id
        else:
            return  # clicked something else
            
        # Change the circle's colorm     
        current_color = canvas.itemcget(circle_id, "fill")
        if current_color == "#d3d3d3":    # grey
            canvas.itemconfig(circle_id, fill="#86E44C")  # green
        elif current_color == "#86E44C":   # green
            canvas.itemconfig(circle_id, fill="#ffde5a")  # yellow
        elif current_color == "#ffde5a":
            canvas.itemconfig(circle_id, fill="#d3d3d3")
        else: 
            return

    # Create 6 rows of 5 circles with text
    for row in range(6):
        for col in range(5):
            x = start_x + (col * spacing_x)
            current_y = y + (row * spacing_y)
            
            # Create circle
            circle = canvas.create_oval(
                x, current_y, 
                x + circle_diameter, 
                current_y + circle_diameter, 
                fill="#d3d3d3", 
                outline="gray"
            )
            all_circles.append(circle)
            
            # Create text in circle center
            text = canvas.create_text(
                x + circle_diameter/2,
                current_y + circle_diameter/2,
                text="",
                font=("Arial", 24, "bold")
            )
            all_texts.append(text)

    # Bind events
    window.bind('<Key>', key_press)
    canvas.bind('<Button-1>', circle_click)
    canvas.focus_set()

    window.mainloop()

def stats_screen_gui(window):
    # Create new window for stats
    stats_window = tk.Toplevel(window)
    stats_window.geometry("400x500")
    stats_window.title("Wordle Solver Stats")
    stats_window.resizable(False, False)
    stats_window["bg"] = "#424242"

    # Title
    title = tk.Label(
        stats_window,
        text="Statistics",
        bg="#424242",
        fg="#d9d9d9",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    # Frame for stats content
    stats_frame = tk.Frame(
        stats_window,
        bg="#2b2b2b",
        relief="solid"
    )
    stats_frame.place(x=30, y=80, width=340, height=300)

    # Text widget for displaying stats
    text_display = tk.Text(
        stats_frame,
        width=35,
        height=15,
        bg="#2b2b2b",
        fg="#d9d9d9",
        font=("Arial", 12),
        wrap=tk.WORD,
        padx=10,
        pady=10
    )
    text_display.pack(padx=10, pady=10)

    try:
        with open("performance_data.txt", "r") as file:
            content = file.read()
            if content.strip() == "":
                content = "No games played yet!"
            text_display.insert("1.0", content)
    except FileNotFoundError:
        text_display.insert("1.0", "No statistics available yet!")
    
    # Make text widget read-only
    text_display.config(state="disabled")

    # Back button
    back_button = tk.Button(
        stats_window,
        text="BACK",
        fg="black",
        bg="#86E44C",
        font=("Arial", 15),
        command=stats_window.destroy
    )
    back_button.pack(pady=20)

    # Add hover effect for back button
    back_button.bind("<Enter>", lambda e: e.widget.config(bg="#4CAF50"))
    back_button.bind("<Leave>", lambda e: e.widget.config(bg="#86E44C"))

init_instruction_screen()