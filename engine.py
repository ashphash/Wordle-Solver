# import display

MAX_GUESSES = 6
sample_guesses = [
    [
        {"position": 0, "character": "c", "correctness": 0},
        {"position": 1, "character": "o", "correctness": 0},
        {"position": 2, "character": "u", "correctness": 0},
        {"position": 3, "character": "n", "correctness": 1},
        {"position": 4, "character": "t", "correctness": 0}
    ],
    [
        {"position": 0, "character": "n", "correctness": 1},
        {"position": 1, "character": "e", "correctness": 0},
        {"position": 2, "character": "v", "correctness": 0},
        {"position": 3, "character": "e", "correctness": 0},
        {"position": 4, "character": "r", "correctness": 0}
    ],
    [
        {"position": 0, "character": "a", "correctness": 0},
        {"position": 1, "character": "g", "correctness": 0},
        {"position": 2, "character": "a", "correctness": 2},
        {"position": 3, "character": "i", "correctness": 0},
        {"position": 4, "character": "n", "correctness": 2}
    ]
]


def run_game(word_list):
    ''' It run game '''
    reduced_list = word_list
    for i in range(MAX_GUESSES):
        if i >= len(sample_guesses):
            break
        # guess = display.get_guess()
        guess = sample_guesses[i]
        sorted_guess = sort_guess(guess)
        reduced_list = reduce_list(sorted_guess, reduced_list)
        # display.show_choice(reduced_list)
        print("Spawn? ", 'spawn' in reduced_list)
        if len(reduced_list):
            print("Try:", reduced_list[0])
        else:
            print("no words")
        input()

def reduce_list(guess: list, word_list: list) -> list:
    ''' It reduce list '''
    character_set = set()
    for letter in guess:
        if letter['correctness'] == 0 and letter['character'] not in character_set:
            word_list = [word for word in word_list if letter['character'] not in word]
        if letter['correctness'] == 1:
            word_list = [word for word in word_list if (letter['character'] in word and word[letter['position']] != letter['character'])]
        elif letter['correctness'] == 2:
            word_list = [word for word in word_list if word[letter['position']] == letter['character']]
        character_set.add(letter['character'])
    # print(len(word_list))
    return word_list

def sort_guess(guess):
    ''' It sort guess '''
    return sorted(guess, key=lambda letter: letter['correctness'], reverse=True)

if __name__ == "__main__":
    with open('word_list_ranked.txt', 'r') as file:
        word_list_main = [line.strip() for line in file]
    run_game(word_list_main)
