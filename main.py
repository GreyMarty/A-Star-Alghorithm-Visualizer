from tkinter import *

from panel import Panel
from visualizer import Visualizer
from pathfinder import AStarSearch


root = Tk()
root.minsize(800, 600)
root.title("A* Visualizer")

visualizer_area = Frame(root)
visualizer_area.pack(side="bottom", fill="both", expand=1)

visualizer = Visualizer(77, 60, pathfinder=AStarSearch, cell_size=9, master=visualizer_area)
visualizer.pack()

panel = Panel({"Clear": visualizer.clear, "Build Path": visualizer.build_path}, master=root, height=30)
panel.pack()

root.mainloop()
