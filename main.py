from gui import select_file, save_file
from gcode_utils import process_gcode
from tangencial import process_tangential

def main():
    # Prompt the user to select the original G-code file.
    file_path = select_file()
    
    # Check if a file was selected. If not, print an error message and exit.
    if not file_path:
        print("No file selected.")
        return
    
    # Open the selected G-code file and read its contents.
    with open(file_path, 'r') as file:
        gcode_lines = file.readlines()

    # Process the G-code to apply general adjustments such as arc subdivision.
    processed_gcode = process_gcode(gcode_lines)

    # Apply tangential adjustments to the processed G-code.
    # This step modifies the G-code to include tangential control for smoother transitions.
    final_gcode = process_tangential(processed_gcode)

    # Save the final processed G-code to a new file.
    # This file will contain the adjusted G-code ready for machine execution.
    save_file(final_gcode)

# Ensure that the main function runs when this script is executed directly.
if __name__ == "__main__":
    main()
