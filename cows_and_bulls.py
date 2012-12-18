import itertools
import re

class CowsAndBulls():

    def __init__(self, game_size=4):
        self.possible_numbers = self.generate_all_possible_permutations()
        self.game_state = list()
        self.game_size = game_size
    
    def generate_all_possible_permutations(self):
        return filter(lambda x: x[0] != 0, itertools.permutations(range(0, 10), 4))
    
    def pick_number_to_ask(self):
        return self.possible_numbers.pop()
    
    def parse_answer(self, answer):
        bulls = 0
        cows = 0
    
        match = re.match(r'((?P<bulls>\d)b)?((?P<cows>\d)c)?', answer)
        if match.group('bulls'):
            bulls = int(match.group('bulls'))
        if match.group('cows'):
            cows = int(match.group('cows'))
        
        return {'answer': answer, 'cows': cows, 'bulls': bulls}
    
    def is_valid_answer(self, parsed_answer):
        return not (parsed_answer['cows'] + parsed_answer['bulls'] > self.game_size or
                    parsed_answer['bulls'] == self.game_size - 1)
                
    def constrain(self, asked_number, parsed_answer):
        asked_number_set = set(asked_number)
        possible_numbers = filter(lambda n: 
                        parsed_answer['bulls'] == len(filter(lambda x: x[0] == x[1], zip(n, asked_number))) and
                        parsed_answer['cows'] == len(asked_number_set - set(n)) - parsed_answer['bulls'],
                        self.possible_numbers)
        return possible_numbers
    
    def run(self):
        while True:
            question = self.pick_number_to_ask()
            print("Is your number %s: " % ''.join(map(str, question)))
            answer = raw_input()
            parsed_answer = self.parse_answer(answer)
            while not self.is_valid_answer(parsed_answer):
                print("Why are you doing this?? Try again!")
                print("Is your number %s: " % ''.join(map(str, question)))
                answer = raw_input()
                parsed_answer = self.parse_answer(answer)
    
            self.game_state.append((question, parsed_answer))
            self.possible_numbers = self.constrain(question, parsed_answer)
    
            if parsed_answer['bulls'] == self.game_size:
                print("Hehe, I won!")
                exit()
            if len(self.possible_numbers) == 0:
                print("You, liar!")
                # todo, handle this situation by letting the player fix his/her mistake
                exit()
        
if __name__ == '__main__':
    cnb = CowsAndBulls()
    cnb.run()
    