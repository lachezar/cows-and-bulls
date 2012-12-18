import itertools
import random
import re

class Player():

    def __init__(self, game_size=4):
        self.game_size = game_size
        self.number_to_be_guessed = self.pick_random_number()
        
    def pick_random_number(self):
        possible_numbers = filter(lambda x: x[0] != 0, itertools.permutations(range(0, 10), 4))
        #return random.sample(possible_numbers, 1)[0]
        return possible_numbers[0]
        
    def ask_for_number(self):
        asked_number = raw_input("Try to guess: ")
        while not re.match(r'^\d+$', asked_number) or len(set(list(asked_number))) != self.game_size or asked_number[0] == '0':
            asked_number = raw_input("Wrong format of the question, try again: ")
        return map(int, asked_number)
        
    def answer_to_player(self, asked_number):
        bulls = len(filter(lambda x: x[0] == x[1], zip(self.number_to_be_guessed, asked_number)))
        cows = len(set(asked_number) & set(self.number_to_be_guessed)) - bulls
        answer = {
            'cows': cows,
            'bulls': bulls
        }
        return answer
        
    def play(self):
        asked_number = self.ask_for_number()
        answer = self.answer_to_player(asked_number)
        return answer
        