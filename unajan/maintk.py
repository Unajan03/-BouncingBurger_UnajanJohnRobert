import tkinter as tk
from PIL import Image, ImageTk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BURGER_SPEED_X = 5
BURGER_SPEED_Y = 5
FRAME_DELAY = 16  # ~60 FPS

# Main App
class BurgerBounceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bouncing Burger with Name")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        # Load and resize the image using the new Pillow method
        self.burger_image = Image.open("burger.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.tk_burger = ImageTk.PhotoImage(self.burger_image)
        self.burger_width = self.tk_burger.width()
        self.burger_height = self.tk_burger.height()

        # Initial position and velocity
        self.x = random.randint(0, WINDOW_WIDTH - self.burger_width)
        self.y = random.randint(0, WINDOW_HEIGHT - self.burger_height)
        self.vx = BURGER_SPEED_X
        self.vy = BURGER_SPEED_Y

        # Draw burger and name
        self.burger_id = self.canvas.create_image(self.x, self.y, image=self.tk_burger, anchor="nw")
        self.name_color = self.random_color()
        self.name_id = self.canvas.create_text(
            self.x + self.burger_width // 2,
            self.y + self.burger_height // 2,
            text="John Robert Unajan",
            fill=self.name_color,
            font=("Arial", 20, "bold")
        )

        # Animation control
        self.paused = False
        self.root.bind("<space>", self.toggle_pause)

        # Start animation
        self.animate()

    def animate(self):
        if not self.paused:
            self.move_burger()
        self.root.after(FRAME_DELAY, self.animate)

    def move_burger(self):
        self.x += self.vx
        self.y += self.vy

        hit_edge = False

        if self.x <= 0 or self.x + self.burger_width >= WINDOW_WIDTH:
            self.vx = -self.vx
            hit_edge = True

        if self.y <= 0 or self.y + self.burger_height >= WINDOW_HEIGHT:
            self.vy = -self.vy
            hit_edge = True

        # Change color on edge hit
        if hit_edge:
            self.name_color = self.random_color()
            self.canvas.itemconfig(self.name_id, fill=self.name_color)

        # Move burger and name together
        self.canvas.coords(self.burger_id, self.x, self.y)
        self.canvas.coords(self.name_id,
                           self.x + self.burger_width // 2,
                           self.y + self.burger_height // 2)

    def toggle_pause(self, event):
        self.paused = not self.paused

    def random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BurgerBounceApp(root)
    root.mainloop()