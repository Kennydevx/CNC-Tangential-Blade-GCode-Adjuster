# ============= Configurations ==================

# General Settings
StepsX = 200  
# Number of motor steps per unit on the X axis.
# This value is crucial for converting desired movements into physical motor steps.

StepsY = 200  
# Number of motor steps per unit on the Y axis.
# Similar to StepsX, this is important for movement precision on the Y axis.

INVERT_DIRECTION = False  
# Determines whether the angle calculation direction should be inverted.
# If True, the angle calculation will be inverted (e.g., counter-clockwise instead of clockwise).

# Movement Settings
CLOCKWISE_COMMAND = 'G2'  
# G-Code command used for clockwise movements.
# G2 is a standard G-Code command for drawing arcs in the clockwise direction.

ANGLE_PRECISION = 2  
# Precision of the angle in decimal places.
# Defines how many decimal places will be used when calculating and displaying angles.

ANGLE_ADJUST_THRESHOLD = 0.5  
# Angle adjustment threshold.
# If the difference between the current angle and the previous angle exceeds this value, the angle will be adjusted.

NORMALIZE_ANGLE = True  
# Defines whether the angle should be normalized to the [0, 360) degree range.
# Normalizing the angle can help ensure that it remains within a standard range.

SUPPORTED_COMMANDS = ['G1', 'G2', 'G3']  
# List of supported G-Code commands.
# G1 is for linear movements, G2 for clockwise arcs, and G3 for counter-clockwise arcs.

MIN_MOVEMENT_THRESHOLD = 0.01  
# Minimum movement threshold required to process a command.
# If the movement is less than this value, it might be ignored to prevent unnecessary processing.

ENABLE_TANGENTIAL_CONTROL = True  
# Defines whether tangential control should be enabled or disabled.
# Tangential control can be used to adjust the angle to follow a tangential path.

DEFAULT_FEEDRATE = 1200  
# Default feedrate in millimeters per minute.
# Defines the speed at which the machine moves when executing G-Code commands.

# Initial Position
INITIAL_X = 0.0  
# Initial position on the X axis.
# Sets the starting position of the X axis at the beginning of G-Code processing.

INITIAL_Y = 0.0  
# Initial position on the Y axis.
# Sets the starting position of the Y axis at the beginning of G-Code processing.

# Coordinate Precision
PRECISION_COORD = 4  
# Precision for X and Y coordinates when processing G-Code.
# Defines the number of decimal places used for X and Y coordinates.

# Arc Subdivision
ARC_SEGMENTS = 50  
# Number of segments to subdivide arcs.
# The higher the number of segments, the smoother the arc subdivision will be, but it will also increase the number of points generated.

# Logging Configuration
LOG_LEVEL = 'INFO'  
# Logging level configured for the system.
# Can be DEBUG, INFO, WARNING, or ERROR. Defines the level of detail for logging messages.

# Unit of Measurement
UNITS = 'mm'  
# Unit of measurement used (millimeters or inches).
# Defines the unit of measurement for all coordinates and movements in G-Code.

# Default I and J Values (for arc center)
DEFAULT_I = 0.0  
# Default value for coordinate I, which defines the X offset of the arc center.
# Used when the I value is not specified in the G-Code command.

DEFAULT_J = 0.0  
# Default value for coordinate J, which defines the Y offset of the arc center.
# Used when the J value is not specified in the G-Code command.

# ===============================================
