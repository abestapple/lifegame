import numpy as np
import tkinter as tk
import time

# Global variables
N = 40
ON = 1
OFF = 0
RUNNING = False
cell_size = 20

# Initialize the grid with all cells initially OFF
grid = np.zeros((N, N), dtype=int)

# Create a variable to store custom cell positions
custom_cells = set()

# Function to toggle cell state using mouse click
def toggle_cell(event):
    global grid, custom_cells
    if not RUNNING:
        x = event.x // cell_size
        y = event.y // cell_size
        if 0 <= x < N and 0 <= y < N:
            if (x, y) not in custom_cells:
                custom_cells.add((x, y))
                grid[y, x] = ON
            else:
                custom_cells.remove((x, y))
                grid[y, x] = OFF
            draw_cell(x, y)

# Function to update the grid based on Conway's rules
def update_grid():
    global grid
    neighbor_sum = (
        np.roll(grid, (-1, -1), axis=(0, 1)) +
        np.roll(grid, (-1, 0), axis=(0, 1)) +
        np.roll(grid, (-1, 1), axis=(0, 1)) +
        np.roll(grid, (0, -1), axis=(0, 1)) +
        np.roll(grid, (0, 1), axis=(0, 1)) +
        np.roll(grid, (1, -1), axis=(0, 1)) +
        np.roll(grid, (1, 0), axis=(0, 1)) +
        np.roll(grid, (1, 1), axis=(0, 1))
    )
    new_grid = np.where(((grid == ON) & ((neighbor_sum == 2) | (neighbor_sum == 3))) | ((grid == OFF) & (neighbor_sum == 3)), ON, OFF)
    custom_cells.clear()
    grid = new_grid
    if grid.sum()==0:
        reset_simulation()
    draw_grid()
    if RUNNING:
        root.after(100, update_grid)
# Function to draw the entire grid on the canvas
def draw_grid():
    canvas.delete("all")
    for y in range(N):
        for x in range(N):
            draw_cell(x, y)

# Function to draw a cell on the canvas
def draw_cell(x, y):
    if grid[y, x] == ON:
        canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="black")
    else:
        canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="white")

# Function to start the simulation
def start_simulation():
    global RUNNING
    RUNNING = True
    random_init_checkbox.config(state=tk.DISABLED)
    start_button.config(state=tk.DISABLED)
    if random_init_var.get():
        grid[:] = np.random.randint(0, 2, size=(N, N))
        canvas.delete("all")
        draw_grid_lines()  # Redraw grid lines
        update_grid()
    else:
        update_grid()

# Function to pause the simulation
def pause_simulation():
    global RUNNING
    RUNNING = False
    random_init_checkbox.config(state=tk.NORMAL)
    start_button.config(state=tk.NORMAL)

# Function to reset the simulation
def reset_simulation():
    global grid, RUNNING
    RUNNING = False
    grid = np.zeros((N, N), dtype=int)
    custom_cells.clear()
    random_init_checkbox.config(state=tk.NORMAL)
    draw_grid()
def draw_grid_lines():
    for i in range(N):
        canvas.create_line(0, i * cell_size, N * cell_size, i * cell_size, fill="gray")
        canvas.create_line(i * cell_size, 0, i * cell_size, N * cell_size, fill="gray")
# Create the main window
root = tk.Tk()
root.title("Conway's Game of Life")

# Create a Canvas widget to display the grid
canvas = tk.Canvas(root, width=N * cell_size, height=N * cell_size)
canvas.grid(row=0, column=0, columnspan=3)

# Bind mouse clicks to canvas events for customizing cell positions
canvas.bind("<Button-1>", toggle_cell)

# Checkbox for customizing initial cell positions
random_init_var = tk.IntVar()
random_init_checkbox = tk.Checkbutton(root, text="Random Initialization", variable=random_init_var)
random_init_checkbox.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

# Create buttons for control
start_button = tk.Button(root, text="Start", command=start_simulation)
pause_button = tk.Button(root, text="Pause", command=pause_simulation)
reset_button = tk.Button(root, text="Reset", command=reset_simulation)

# Place buttons in the last row, spanning all columns
start_button.grid(row=2, column=0, padx=10, pady=10)
pause_button.grid(row=2, column=1, padx=10, pady=10)
reset_button.grid(row=2, column=2, padx=10, pady=10)
draw_grid_lines()
# Start the tkinter main loop
root.mainloop()
