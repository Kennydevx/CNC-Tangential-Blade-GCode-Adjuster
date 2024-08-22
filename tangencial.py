import math
import re
from config import (
    StepsX, StepsY, CLOCKWISE_COMMAND, ANGLE_PRECISION, ANGLE_ADJUST_THRESHOLD,
    NORMALIZE_ANGLE, SUPPORTED_COMMANDS, INITIAL_X, INITIAL_Y, INVERT_DIRECTION,
    ENABLE_TANGENTIAL_CONTROL, MIN_MOVEMENT_THRESHOLD, DEFAULT_FEEDRATE
)

def extract_value(line, key):
    """
    Extracts a numerical value from a G-code line based on a specified key.

    Args:
        line (str): The G-code line to search.
        key (str): The key to look for in the line (e.g., 'X', 'Y').

    Returns:
        float: The extracted value if found, otherwise None.
    """
    match = re.search(f"{key}([-+]?\d*\.?\d*)", line)
    return float(match.group(1)) if match else None

def calculate_angle(dx, dy, clockwise=True):
    """
    Calculates the tangential angle based on the movement in X and Y coordinates.

    Args:
        dx (float): Movement in the X direction.
        dy (float): Movement in the Y direction.
        clockwise (bool): Direction of movement; True for clockwise, False for counterclockwise.

    Returns:
        float: The calculated angle for the A axis, normalized to the range [0, 1].
    """
    # Calculate the angle in radians using the atan2 function.
    angle_rad = math.atan2(dy * StepsY, dx * StepsX)
    
    # Convert the angle from radians to degrees.
    angle_deg = math.degrees(angle_rad)
    
    if not clockwise:
        # If the movement is counterclockwise, invert the angle.
        angle_deg = -angle_deg
    
    # If the direction inversion is enabled, invert the angle.
    if INVERT_DIRECTION:
        angle_deg = -angle_deg
    
    # Normalize the angle to the range [0, 360) if normalization is enabled.
    if NORMALIZE_ANGLE:
        angle_deg = angle_deg % 360
    
    # Convert the angle to a normalized value in the range [0, 1] for the A axis.
    # This is useful if the A axis expects a normalized input.
    return angle_deg / 360.0

def process_tangential(gcode_lines):
    """
    Processes G-code lines to add tangential control commands based on the movement direction.

    Args:
        gcode_lines (list of str): List of G-code lines to process.

    Returns:
        list of str: Processed G-code lines with tangential control commands added.
    """
    # Return the original G-code if tangential control is disabled.
    if not ENABLE_TANGENTIAL_CONTROL:
        return gcode_lines

    processed_gcode = []
    current_x, current_y = INITIAL_X, INITIAL_Y
    prev_angle_a = None

    for line in gcode_lines:
        # Check if the line contains a supported G-code command (e.g., G1, G2, G3).
        if any(cmd in line for cmd in SUPPORTED_COMMANDS):
            x_final = extract_value(line, 'X') or current_x
            y_final = extract_value(line, 'Y') or current_y
            
            # Calculate movement in X and Y directions.
            dx = x_final - current_x
            dy = y_final - current_y
            
            # Skip small movements that are below the minimum threshold.
            if abs(dx) < MIN_MOVEMENT_THRESHOLD and abs(dy) < MIN_MOVEMENT_THRESHOLD:
                continue

            # Determine if the movement is clockwise based on the presence of the CLOCKWISE_COMMAND.
            clockwise = CLOCKWISE_COMMAND in line
            angle_a = calculate_angle(dx, dy, clockwise)
            
            # If there is a previous angle, adjust the current angle to ensure smooth transitions.
            if prev_angle_a is not None:
                delta_a = angle_a - prev_angle_a
                # Adjust angle to avoid large jumps between consecutive commands.
                if delta_a > ANGLE_ADJUST_THRESHOLD:
                    angle_a -= 1.0
                elif delta_a < -ANGLE_ADJUST_THRESHOLD:
                    angle_a += 1.0

            # Append the tangential control command with the configured angle precision.
            processed_gcode.append(f"G1 A{angle_a:.{ANGLE_PRECISION}f}")
            
            # Apply the default feedrate if not already specified in the line.
            if 'F' not in line:
                processed_gcode.append(f"G1 F{DEFAULT_FEEDRATE}")
            
            # Append the original G-code line for continuity.
            processed_gcode.append(line.strip())
            
            # Update the current position and the previous angle for the next iteration.
            prev_angle_a = angle_a
            current_x, current_y = x_final, y_final
        else:
            # For lines not containing supported commands, append them directly.
            processed_gcode.append(line.strip())

    return processed_gcode
