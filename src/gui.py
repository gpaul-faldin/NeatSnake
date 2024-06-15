import tkinter as tk

class PopulationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Population Size")
        self.root.minsize(200, 200)
        self.label = tk.Label(self.root, text="Population Size: 0")
        self.label.pack()
        self.root.update()

    def update_population_size(self, size):
        self.label.config(text=f"Population Size: {size}")
        self.root.update()

    def update_longest_living_thread(self, lifetime):
        longest_living_label = tk.Label(self.root, text=f"Longest Living Thread: {lifetime} seconds")
        longest_living_label.pack()
        self.root.update()

    def update_average_lifetime(self, average_lifetime):
        average_lifetime_label = tk.Label(self.root, text=f"Average Lifetime: {average_lifetime} seconds")
        average_lifetime_label.pack()
        self.root.update()

    def close(self):
        self.root.destroy()