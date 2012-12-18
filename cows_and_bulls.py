import itertools
import random
import re

class Game():

    def __init__(self, game_size=4):
        self.possible_numbers = self.generate_all_possible_permutations()
        self.game_state = list()
        self.game_size = game_size
        self.number_to_be_guessed = self.pick_random_number()
        self.game_progress = 0
        self.current_step = 0
    
    def generate_all_possible_permutations(self):
        return filter(lambda x: x[0] != 0, itertools.permutations(range(0, 10), 4))
    
    def pick_random_number(self):
        return random.sample(self.possible_numbers, 1)[0]
        
    def ask_for_number(self, question):
        print("Is your number %s: " % ''.join(map(str, question)))
        answer = raw_input()
        return answer
    
    def parse_answer(self, answer):
        bulls = 0
        cows = 0
    
        match = re.match(r'((?P<bulls>\d)b)?\s*((?P<cows>\d)c)?\s*((?P<reverse_order_bulls>\d)b)?', answer)
        if match.group('bulls'):
            bulls = int(match.group('bulls'))
        elif match.group('reverse_order_bulls'):
            bulls = int(match.group('reverse_order_bulls'))
        if match.group('cows'):
            cows = int(match.group('cows'))
        
        return {'answer': answer, 'cows': cows, 'bulls': bulls}
    
    def is_valid_answer(self, parsed_answer):
        return not (parsed_answer['cows'] + parsed_answer['bulls'] > self.game_size or
                    parsed_answer['bulls'] == self.game_size - 1)
                
    def constrain(self, asked_number, parsed_answer):
        print parsed_answer
        asked_number_set = set(asked_number)
        possible_numbers = filter(lambda n: 
                        parsed_answer['bulls'] == len(filter(lambda x: x[0] == x[1], zip(n, asked_number))) and
                        parsed_answer['cows'] == len(asked_number_set & set(n)) - parsed_answer['bulls'],
                        self.possible_numbers)
        return possible_numbers
        
    def receive_players_question(self):
        asked_number = raw_input("Try to guess: ")
        while not (re.match(r'^\d+$', asked_number) and len(asked_number) == self.game_size):
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
        while True:
            self.game_progress += 1
            
            print
            print "Step %d" % self.game_progress
            print
            
            asked_number = self.receive_players_question()
            answer = self.answer_to_player(asked_number)
            if answer['bulls'] == self.game_size:
                print("Congratz! You won!")
            else:
                print("%db %dc" % (answer['bulls'], answer['cows']))
            
            sample_number = self.pick_random_number()
            answer = self.ask_for_number(sample_number)
            parsed_answer = self.parse_answer(answer)
            while not self.is_valid_answer(parsed_answer):
                print("Uh-oh, this can not be happening!")
                answer = self.ask_for_number(sample_number)
                parsed_answer = self.parse_answer(answer)
    
            self.game_state.append((sample_number, parsed_answer))
            self.possible_numbers = self.constrain(sample_number, parsed_answer)
    
            if parsed_answer['bulls'] == self.game_size:
                print("Hehe, I won!")
                exit()
            if len(self.possible_numbers) == 0:
                print("You, liar!")
                # todo, handle this situation by letting the player fix his/her mistake
                exit()
        
if __name__ == '__main__':
    cnb = Game()
    cnb.play()
    