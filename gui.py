import tkinter as tk
from tkinter import filedialog, messagebox

def select_file():
    """
    Opens a file dialog for the user to select a G-code file.

    Returns:
        str: The path to the selected file.
    """
    # Open a file dialog to select a G-code file
    file_path = filedialog.askopenfilename(filetypes=[("G-code Files", "*.nc")])
    return file_path

def save_file(processed_gcode):
    """
    Opens a file dialog for the user to save the processed G-code to a file.

    Args:
        processed_gcode (list of str): List of processed G-code lines to save.

    Returns:
        None
    """
    # Open a file dialog to select where to save the processed G-code
    file_path = filedialog.asksaveasfilename(defaultextension=".nc", filetypes=[("G-code Files", "*.nc")])
    
    if file_path:
        # Write the processed G-code to the selected file
        with open(file_path, 'w') as file:
            file.write("\n".join(processed_gcode))
        # Show a success message once the file is saved
        messagebox.showinfo("Success", f"File saved to: {file_path}")
