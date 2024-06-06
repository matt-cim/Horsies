import tkinter as tk
from PIL import Image, ImageTk
import datetime
import numpy as np
from numpy.random import choice

# https://en.wikipedia.org/wiki/Linear_congruential_generator
# r+1 = ((r * a) + c) mod m

# r+1 = ((r * 41) + 7) mod 16 (note 14 is max # of horses)
# Hull–Dobell Theorem
# 1. gcd(7, 16) = 1 GOOD
# - prime factor(s) of 16 is 2 (explain prime factorization)
# 2. 41 - 1 = 40 and 40 is divisble by 2 GOOD
# - note 41 is a prime number
# 3. 16 is divisble by 4 and 41 - 1 = 40 is divisble by 4 GOOD


NUM_HORSES = 12
MOVE_COUNT = 0

class HorseRace:
    def __init__(self, root):
        self.root = root
        self.root.title("Horse Race Simulation")
        # TODO canvas size height will have to work in accordance with # of inputted horses
        # self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas = tk.Canvas(self.root, width=800, height=900, bg="white")
        self.canvas.pack()

        self.dice = [[0] * 6] * NUM_HORSES # init. to all zeros
        percentage = self.odds_to_percentage(7, 2)
        percentage /= 100
        percentage = round(percentage, 2)
        for i in range(NUM_HORSES):
            self.dice[i][0] = percentage
            remainPerc = round((1 - percentage) / 10, 2)
            self.dice[i][1] = round(remainPerc * 3, 2) # slight bias compared to following
            self.dice[i][2] = round(remainPerc * 5, 2) # slight bias compared to following
            self.dice[i][3] = remainPerc
            self.dice[i][4] = remainPerc
            self.dice[i][5] = remainPerc

        print(self.dice)

        self.distances = [10, 8, 6, 4, 2, 1]
        self.horses = []
        self.horse_images = []

        for i in range(NUM_HORSES):
            image = Image.open(f"horsies/horseHead{i+1}.png")
            image = image.resize((60, 60))
            photo = ImageTk.PhotoImage(image)
            self.horse_images.append(photo)
        
        self.finish_line = 750
        self.create_horses()

        self.start_race()

    def odds_to_percentage(self, numerator, denominator):
        # fractional odds so using implied probability where (A/B) -> (B / (A+B)) * 100
        ret = (denominator / (numerator + denominator)) * 100
        return round(ret, 1)

    def guess_rand_winner(self, seed):
        # outright guess who will win without considering odds (assuming # of total horses works)
        print("SEED:")
        print(seed)
        print("RANDOMLY GUESSED WINNER:")
        return ((seed * 41) + 7) % 16

    def create_horses(self):
        for i in range(NUM_HORSES):
            horse = self.canvas.create_image(50, i*70 + 75, image=self.horse_images[i], anchor=tk.CENTER)
            self.horses.append(horse)
            self.canvas.create_text(2, i*70 + 75, text=f"\tHorse {i+1}", font=('Arial', 12))

    def start_race(self):
        self.running = True
        print(self.guess_rand_winner(int(datetime.datetime.now().strftime("%H%M%S"))))
        self.move_horses()

    def move_horses(self):
        global MOVE_COUNT
        MOVE_COUNT += 1
        
        if self.running:
            i = 0
            for horse in self.horses:
                probs = np.array(self.dice[i])
                probs /= probs.sum()  # normalize bc sum may be decimals over 1 ex: 1.00006
                randomNumberList = choice(self.distances, 1, p=probs)
                print(randomNumberList)
                move_distance = randomNumberList[0]
                i += 1

                self.canvas.move(horse, move_distance, 0)
                horse_coords = self.canvas.coords(horse)
                # TODO this conditional check here favors horses earlier in self.horses -> verify by setting move_distance to a const.
                if horse_coords[0] >= self.finish_line:  # check the x-coordinate only
                    self.running = False
                    self.announce_winner(horse)
                    break
            self.root.after(100, self.move_horses)

    def announce_winner(self, winning_horse):
        print("TOTAL MOVES:")
        print(MOVE_COUNT)
        winner_index = self.horses.index(winning_horse) + 1
        self.canvas.create_text(400, 200, text=f"Horse {winner_index} Wins!", font=('Arial', 24), fill='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = HorseRace(root)
    root.mainloop()
