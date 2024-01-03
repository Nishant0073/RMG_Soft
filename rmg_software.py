
import tkinter as tk
from tkinter import filedialog
from controller import *
from controller import select_file
from controller import process_and_display

# Create the main Tkinter window
root = tk.Tk()
root.title("Resource Locator App")

# File 1 selection
file1_label = tk.Label(root, text="Select Profiles File:")
file1_label.grid(row=0, column=0, padx=10, pady=10)

employee_filepath = tk.Entry(root, width=40)
employee_filepath.grid(row=0, column=1, padx=10, pady=10)

file1_button = tk.Button(root, text="Browse", command=lambda: select_file(employee_filepath))
file1_button.grid(row=0, column=2, padx=10, pady=10)

# File 2 selection
file2_label = tk.Label(root, text="Select Open Requirements File:")
file2_label.grid(row=1, column=0, padx=10, pady=10)

requirement_filepath = tk.Entry(root, width=40)
requirement_filepath.grid(row=1, column=1, padx=10, pady=10)

file2_button = tk.Button(root, text="Browse", command=lambda: select_file(requirement_filepath))
file2_button.grid(row=1, column=2, padx=10, pady=10)

# Process button
process_button = tk.Button(root, text="Process Files", command=process_and_display)
process_button.grid(row=2, column=1, pady=20)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

# Start the Tkinter event loop
root.mainloop()