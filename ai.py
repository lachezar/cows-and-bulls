import itertools
import random
import re

class AI():

    def __init__(self, game_size=4):
        self.possible_numbers = self.generate_all_possible_permutations()
        self.game_size = game_size
    
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
                    (parsed_answer['bulls'] == self.game_size - 1 and parsed_answer['cows'] == 1))
                
    def constrain(self, asked_number, parsed_answer):
        print parsed_answer
        asked_number_set = set(asked_number)
        possible_numbers = filter(lambda n: 
                        parsed_answer['bulls'] == len(filter(lambda x: x[0] == x[1], zip(n, asked_number))) and
                        parsed_answer['cows'] == len(asked_number_set & set(n)) - parsed_answer['bulls'],
                        self.possible_numbers)
        return possible_numbers
        
    def replay(self, steps):
        print "replay %d steps" % len(steps)
        self.possible_numbers = self.generate_all_possible_permutations()
        for rs in steps:
            self.possible_numbers = self.constrain(*rs)
        
    def play(self, sample_number=None):
        sample_number = sample_number or self.pick_random_number()
        answer = self.ask_for_number(sample_number)
        parsed_answer = self.parse_answer(answer)
        while not self.is_valid_answer(parsed_answer):
            print("Uh-oh, this can not be happening!")
            answer = self.ask_for_number(sample_number)
            parsed_answer = self.parse_answer(answer)
    
        #self.game_state.append((sample_number, parsed_answer))
        self.possible_numbers = self.constrain(sample_number, parsed_answer)
        
        return (sample_number, parsed_answer)
    
        
