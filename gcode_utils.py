import re
import math
from config import (
    ARC_SEGMENTS, PRECISION_COORD, DEFAULT_I, DEFAULT_J
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

def calculate_arc_angle(start_x, start_y, end_x, end_y, x_center, y_center, clockwise):
    """
    Calculates the start and end angles of an arc in radians.

    Args:
        start_x (float): The starting X coordinate of the arc.
        start_y (float): The starting Y coordinate of the arc.
        end_x (float): The ending X coordinate of the arc.
        end_y (float): The ending Y coordinate of the arc.
        x_center (float): The X coordinate of the arc's center.
        y_center (float): The Y coordinate of the arc's center.
        clockwise (bool): Direction of the arc; True for clockwise, False for counterclockwise.

    Returns:
        tuple: Start and end angles in radians.
    """
    start_angle = math.atan2(start_y - y_center, start_x - x_center)
    end_angle = math.atan2(end_y - y_center, end_x - x_center)
    
    if clockwise:
        if end_angle > start_angle:
            end_angle -= 2 * math.pi
    else:
        if end_angle < start_angle:
            end_angle += 2 * math.pi
    
    return start_angle, end_angle

def subdivide_arc(start_x, start_y, end_x, end_y, x_center, y_center, radius, clockwise, segments=ARC_SEGMENTS):
    """
    Divides an arc into smaller segments and calculates the points along the arc.

    Args:
        start_x (float): The starting X coordinate of the arc.
        start_y (float): The starting Y coordinate of the arc.
        end_x (float): The ending X coordinate of the arc.
        end_y (float): The ending Y coordinate of the arc.
        x_center (float): The X coordinate of the arc's center.
        y_center (float): The Y coordinate of the arc's center.
        radius (float): The radius of the arc.
        clockwise (bool): Direction of the arc; True for clockwise, False for counterclockwise.
        segments (int): Number of segments to divide the arc into.

    Returns:
        list: List of tuples, each containing the X and Y coordinates of a point along the arc.
    """
    start_angle, end_angle = calculate_arc_angle(start_x, start_y, end_x, end_y, x_center, y_center, clockwise)
    angle_step = (end_angle - start_angle) / segments
    points = []

    for i in range(segments + 1):
        angle = start_angle + i * angle_step
        x = x_center + radius * math.cos(angle)
        y = y_center + radius * math.sin(angle)
        points.append((x, y))

    return points

def process_gcode(gcode_lines):
    """
    Processes G-code lines to handle arc commands (G2 and G3) by subdividing arcs into smaller segments.

    Args:
        gcode_lines (list of str): List of G-code lines to process.

    Returns:
        list of str: Processed G-code lines with subdivided arcs.
    """
    processed_gcode = []
    current_x, current_y = 0.0, 0.0

    for line in gcode_lines:
        if line.startswith('G2') or line.startswith('G3'):
            # Extract the final coordinates and arc center offsets from the G-code line.
            x_final = extract_value(line, 'X') or current_x
            y_final = extract_value(line, 'Y') or current_y
            i_center = extract_value(line, 'I') or DEFAULT_I
            j_center = extract_value(line, 'J') or DEFAULT_J

            # Determine the direction of the arc and calculate the center and radius.
            clockwise = line.startswith('G2')
            x_center = current_x + i_center
            y_center = current_y + j_center
            radius = ((i_center) ** 2 + (j_center) ** 2) ** 0.5

            # Subdivide the arc into smaller segments for smooth movement.
            segments = subdivide_arc(current_x, current_y, x_final, y_final, x_center, y_center, radius, clockwise)
            for x, y in segments:
                processed_gcode.append(f'G1 X{x:.{PRECISION_COORD}f} Y{y:.{PRECISION_COORD}f}')
                current_x, current_y = x, y
        else:
            # For non-arc commands, simply append the line. Update current coordinates if necessary.
            processed_gcode.append(line.strip())
            if 'X' in line or 'Y' in line:
                current_x = extract_value(line, 'X') or current_x
                current_y = extract_value(line, 'Y') or current_y

    return processed_gcode
