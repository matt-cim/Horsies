import tkinter as tk
from PIL import Image, ImageTk
import random

NUM_HORSES = 12

class HorseRace:
    def __init__(self, root):
        self.root = root
        self.root.title("Horse Race Simulation")
        # TODO canvas size height will have to work in accordance with # of inputted horses
        # self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas = tk.Canvas(self.root, width=800, height=900, bg="white")
        self.canvas.pack()
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

    def create_horses(self):
        for i in range(NUM_HORSES):
            horse = self.canvas.create_image(50, i*70 + 75, image=self.horse_images[i], anchor=tk.CENTER)
            self.horses.append(horse)
            self.canvas.create_text(2, i*70 + 75, text=f"\tHorse {i+1}", font=('Arial', 12))

    def start_race(self):
        self.running = True
        self.move_horses()

    def move_horses(self):
        if self.running:
            for horse in self.horses:
                move_distance = random.randint(1, 10)
                self.canvas.move(horse, move_distance, 0)
                horse_coords = self.canvas.coords(horse)
                if horse_coords[0] >= self.finish_line:  # check the x-coordinate only
                    self.running = False
                    self.announce_winner(horse)
                    break
            self.root.after(100, self.move_horses)

    def announce_winner(self, winning_horse):
        winner_index = self.horses.index(winning_horse) + 1
        self.canvas.create_text(400, 200, text=f"Horse {winner_index} Wins!", font=('Arial', 24), fill='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = HorseRace(root)
    root.mainloop()
