import itertools
import re

from player import Player
from ai import AI

class Game():

    def __init__(self, game_size=4):
        self.game_progress = 0
        self.game_steps = list()
        self.game_size = game_size
        self.player = Player(game_size)
        self.ai = AI(game_size)
        
    def play(self):
        while True:
            self.game_progress += 1
            
            print
            print "Step %d" % self.game_progress
            print
            
            answer = self.player.play()
            if answer['bulls'] == self.game_size:
                print("Congratz! You won!")
                exit()
            else:
                print("%db %dc" % (answer['bulls'], answer['cows']))

            repeat_question = None
            while self.game_progress > len(self.game_steps):
                asked_number, answer = self.ai.play(repeat_question)
                            
                self.game_steps.append((asked_number, answer))
                if answer['bulls'] == self.game_size:
                    print("Hehe, I won!")
                    exit()
                if len(self.ai.possible_numbers) == 0:
                    print("You, liar!")
                    step = raw_input("On which step did you lie: ")
                    while not re.match(r'^\d+$', step) or not (1 <= int(step) <= len(self.game_steps)):
                        print("Invalid step.")
                        step = raw_input("On which step did you lie: ")

                    step = int(step)-1
                    repeat_question = self.game_steps[step][0]
                    self.game_steps = self.game_steps[:step]
                    self.ai.replay(self.game_steps)
                else:
                    repeat_question = None
                
        
if __name__ == '__main__':
    game_size = 4
    print("Pick %d digit number with no 2 digits that are the same and without leading 0." % game_size)
    print("The goal of the game is to guess opponent's number first.")
    print("You are allowed to guess the number and receive response of matched digits.")
    print("If you have guessed correct a digit and position, then it is a Bull.")
    print("If you have guessed correct only a digit and not the position, then it is a Cow.")
    print
    print("Read more about the game and rules here: %s" % 'http://en.wikipedia.org/wiki/Bulls_and_cows')
    print
    cnb = Game(game_size)
    cnb.play()
    