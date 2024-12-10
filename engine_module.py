import display_module
import os

def load_words(word_file):
    #Load the ranked words from a file and return them as a list.
    potential_words = []
    with open(word_file, 'r') as file:
        for line in file:
            potential_words.append(line.strip())
    if not potential_words:
        print("Error: Word list file is empty or not properly formatted.")
    return potential_words

def start_game():
    # lolol i made this change
    filter_words()
    update_feedback()
    update_performance_data()

def update_performance_data(success, num_guesses):
    data = {}

    # Check if the performance data file exists
    if os.path.exists("performance_data.txt"):
        with open("performance_data.txt", 'r+') as f:
            for line in f:
                key, value = line.strip().split(":")
                data[key.strip()] = int(value)
                
            data["total_guesses"] += num_guesses
            if success:
                data["success_count"] += 1
            else:
                data["failure_count"] += 1
                
            f.seek(0)
            f.truncate()
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
    else:
        # Initialize new performance file if it doesn't exist
        with open("performance_data.txt", 'w') as f:
            f.write(f"success_count: {1 if success else 0}\n")
            f.write(f"failure_count: {0 if success else 1}\n")
            f.write(f"total_guesses: {num_guesses}\n")
            
    return success, num_guesses

def filter_words(potential_words, feedback):

    for guess, feedback in potential_words:
        filtered_words = []
        for feedback in potential_words:
            if update_feedback(potential_words, guess, feedback):
                filtered_words.append(potential_words)
        potential_words = filtered_words
    return potential_words

def update_feedback(word, guess, feedback):

    for i in range(5):
        if feedback[i] == 'g':  # Green - correct letter and position
            if word[i] != guess[i]:
                return False
        elif feedback[i] == 'y':  # Yellow - correct letter, wrong position
            if guess[i] not in word or word[i] == guess[i]:
                return False
        elif feedback[i] == 'b':  # Black - letter not in the word
            if guess[i] in word:
                return False
    return True

def suggest_next_word(words):
    """
    Suggest the next word based on the current filtered word list.

    Args:
        words (list): Filtered list of potential words.

    Returns:
        str: Suggested word.
    """
    return words[0] if words else None

def solve_wordle(initial_word_list):
    """
    Main solving loop for Wordle.
    
    Args:
        initial_word_list (list): Initial list of possible words
        
    Returns:
        tuple: (success (bool), num_guesses (int))
    """
    potential_words = initial_word_list.copy()
    user_guess = []
    max_attempts = 6
    
    while len(user_guess) < max_attempts:
        # Get next suggestion
        suggested_word = suggest_next_word(potential_words)
        if not suggested_word:
            return False, len(user_guess)
            
        # Get feedback from user
        feedback = display_module.get_user_feedback(suggested_word)
        user_guess.append((suggested_word, feedback))
        
        # Check if word was guessed correctly
        if feedback == "ggggg":
            return True, len(user_guess)
            
        # Filter word list based on feedback
        potential_words = filter_words(words, user_guess)
        
        # Check if no valid words remain
        if not words:
            return False, len(guesses)
            
    return False, max_attempts

def get_user_feedback(word):
    """
    Get feedback from the user for a given word using a graphical interface.
    Returns: str: Feedback string ('g', 'y', 'b').
    """
    feedback = ['b'] * 5  # Default feedback is black
    
    
def update_feedback(index, color):
    feedback[index] = color
    if color == 'g':
        circles[index].config(bg="green")
    elif color == 'y':
        circles[index].config(bg="yellow")
    else:
        circles[index].config(bg="black")



def submit_feedback():
    win.destroy()

submit_btn = tk.Button(
    win, text="Submit", command=submit_feedback
)
submit_btn.pack(pady=20)

win.mainloop()
return ''.join(feedback)