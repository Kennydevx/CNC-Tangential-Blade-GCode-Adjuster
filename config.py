# ============= Configurations ==================

# General Settings
StepsX = 200  
# Number of motor steps per unit on the X axis.
# This value is crucial for converting desired movements into physical motor steps.

StepsY = 200  
# Number of motor steps per unit on the Y axis.
# Similar to StepsX, this is important for movement precision on the Y axis.

# Coordinate Precision
PRECISION_COORD = 4  
# Precision for X and Y coordinates when processing G-Code.
# Defines the number of decimal places used for X and Y coordinates.

# Arc Subdivision
ARC_SEGMENTS = 50  
# Number of segments to subdivide arcs.
# The higher the number of segments, the smoother the arc subdivision will be, but it will also increase the number of points generated.

# Default I and J Values (for arc center)
DEFAULT_I = 0.0  
# Default value for coordinate I, which defines the X offset of the arc center.
# Used when the I value is not specified in the G-Code command.

DEFAULT_J = 0.0  
# Default value for coordinate J, which defines the Y offset of the arc center.
# Used when the J value is not specified in the G-Code command.

# ===============================================
