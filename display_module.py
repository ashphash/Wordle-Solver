import tkinter as tk
from tkinter import messagebox
from functools import partial
import engine_module

def init_instruction_screen():
    window = tk.Tk()
    window.geometry("400x600")
    window.title("Wordle Solver")
    window.resizable(False, False)

    title = tk.Label(
        text="Wordle Solver", fg="black", font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    frame = tk.Frame(
        window,
        bg="#ffde5a",
        relief="solid",
        bd=2,
    )
    frame.place(x=30, y=80, width=340, height=400)

    title = tk.Label(
        frame,
        text="Instructions:",
        font=("Arial", 13, "bold"),
        bg="#ffde5a",
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
        bg="#ffde5a",
        font=("Arial", 12),
        wraplength=320,  # Ensures text wraps within the frame width
        anchor="nw"  # Aligns text to the top-left corner
    )
    body.pack(padx=10, pady=10)

    frame_buttons = tk.Frame(window)
    frame_buttons.place(x=30, y=500, width=340, height=80)

    play_button = tk.Button(
        frame_buttons,
        text="PLAY",
        fg="black",
        bg="#86E44C",
        font=("Arial", 15),
        command=lambda: start_game(window))

    play_button.grid(row=0, column=0, padx=10)

    stats_button = tk.Button(
        frame_buttons,
        text="STATS",
        fg="black",
        bg="#86E44C",
        font=("Arial", 15),
        command=partial(view_stats_button, window))
    
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

def wordle_solver_gui():
    win = tk.Tk()
    win.geometry("1000x600")
    win.title("Solver Interface")
    win.resizable(False, False)

    title = tk.Label(
        text="Wordle Solver", fg="black", font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    frame = tk.Frame(
        win,
        bg="white",
        relief="solid",
        bd=2,
    )
    frame.place(x=30, y=80, width=950, height=550)

    title = tk.Label(
        frame,
        text="Guess:",
        font=("Arial", 13, "bold"),
        anchor="center"
    )
    title.pack(pady=(20, 5))    

    body = tk.Label(
        frame
    )
    body.pack(padx=10, pady=10)
    circles = []
    for i, letter in enumerate(word):
        circle_frame = tk.Frame(frame)
        circle_frame.pack(side=tk.LEFT, padx=10)

        circle = tk.Label(
            circle_frame,
            text=letter,
            font=("Arial", 20),
            width=4,
            height=2,
            bg="black",
            fg="white",
        )
        circle.pack()
        circles.append(circle)

        button_frame = tk.Frame(circle_frame)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame, text="G", bg="green", fg="white", command=lambda i=i: engine_module.update_feedback(i, 'g')
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            button_frame, text="Y", bg="yellow", fg="black", command=lambda i=i: engine_module.update_feedback(i, 'y')
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            button_frame, text="B", bg="black", fg="white", command=lambda i=i: engine_module.update_feedback(i, 'b')
        ).pack(side=tk.LEFT, padx=2)


def display_result(performance_data, success):
    """
    Display the results of the current game and performance statistics.

    Args:
        performance_data (dict): Dictionary containing performance statistics.
        success (bool): Whether the solver succeeded in guessing the word.
    """
    window = tk.Tk()
    window.geometry("400x400")
    window.title("Game Results")
    window.resizable(False, False)

    title = tk.Label(
        text="Game Results",
        fg="black",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    result_message = "The solver successfully guessed the word!" if success else "The solver failed to guess the word."
    result_label = tk.Label(
        text=result_message,
        fg="black",
        font=("Arial", 12)
    )
    result_label.pack(pady=10)

    total_games = performance_data.get('success_count', 0) + performance_data.get('failure_count', 0)
    average_guesses = (performance_data['total_guesses'] / performance_data['success_count']
                       if performance_data['success_count'] > 0 else 0)

    stats_text = (
        f"Total Games: {total_games}\n"
        f"Success Rate: {performance_data.get('success_count', 0)} / {total_games}\n"
        f"Average Guesses per Success: {average_guesses:.2f}"
    )

    stats_label = tk.Label(
        text=stats_text,
        fg="black",
        font=("Arial", 12),
        justify="left"
    )
    stats_label.pack(pady=20)

    close_button = tk.Button(
        window,
        text="Close",
        fg="black",
        bg="#E6494B",
        font=("Arial", 12),
        command=window.destroy
    )
    close_button.pack(pady=10)

    window.mainloop()

def view_stats_button(window):
    """Show statistics popup when stats button is pressed"""
    stats_window = tk.Toplevel(window)
    stats_window.geometry("300x200") 
    stats_window.title("Statistics")
    stats = {}
    # stats = engine_module.load_stats("performance_data.txt")
    stats_text = (
        f"Games Won: {stats['success_count']}\n"
        f"Games Lost: {stats['failure_count']}\n"
        f"Total Games: {stats['total_games']}\n"
        f"Success Rate: {stats['success_rate']:.1f}%\n"
        f"Average Guesses: {stats['avg_guesses']:.2f}"
    )

    stats_label = tk.Label(
        stats_window,
        text=stats_text,
        font=("Arial", 12),
        justify="left",
        padx=20,
        pady=20
    )
    stats_label.pack()

    close_button = tk.Button(
        stats_window,
        text="Close",
        command=stats_window.destroy
    )
    close_button.pack(pady=10)

def start_game(window):
    """Start the game by closing instruction screen"""
    window.quit()  # Use quit() instead of destroy() to exit mainloop properly
    return True  # Return True to indicate user wants to play
