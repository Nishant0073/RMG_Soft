import tkinter as tk
from tkinter import filedialog
import os

def process_files_for_output(files):
    for i in files:
        print(i)

def process_folder(selected_folder):
    # Hypothetical processing: Display the list of files in the selected folder
    files_in_folder = os.listdir(selected_folder)
    #  process_files(files_in_folder,select_folder,requirement_file)
    return files_in_folder

def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, folder_path)

def process_and_display():
    selected_folder = folder_entry.get()

    if selected_folder:
        files_in_folder = process_folder(selected_folder)
        process_files_for_output(files_in_folder)
        result_label.config(text=f"Files in selected folder:\n{', '.join(files_in_folder)}")
    else:
        result_label.config(text="Please select a folder.")

def select_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

# Create the main Tkinter window
root = tk.Tk()
root.title("Folder Processing App")

# Folder selection
folder_label = tk.Label(root, text="Select Folder of Employees:")
folder_label.grid(row=0, column=0, padx=10, pady=10)

folder_entry = tk.Entry(root, width=40)
folder_entry.grid(row=0, column=1, padx=10, pady=10)

folder_button = tk.Button(root, text="Browse", command=lambda: select_folder(folder_entry))
folder_button.grid(row=0, column=2, padx=10, pady=10)



# File 2 selection
file2_label = tk.Label(root, text="Select Requirement File:")
file2_label.grid(row=1, column=0, padx=10, pady=10)

requirement_filepath = tk.Entry(root, width=40)
requirement_filepath.grid(row=1, column=1, padx=10, pady=10)

file2_button = tk.Button(root, text="Browse", command=lambda: select_file(requirement_filepath))
file2_button.grid(row=1, column=2, padx=10, pady=10)



# Process button
process_button = tk.Button(root, text="Process Folder", command=process_and_display)
process_button.grid(row=2, column=1, pady=20)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, columnspan=3)

# Start the Tkinter event loop
root.mainloop()
