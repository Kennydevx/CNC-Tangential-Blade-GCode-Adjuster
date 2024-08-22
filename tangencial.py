import math
import re
from config import StepsX, StepsY

def extract_value(line, key):
    match = re.search(f"{key}([-+]?\d*\.?\d*)", line)
    return float(match.group(1)) if match else None

def calculate_angle(dx, dy, clockwise=True):
    # Calcula o ângulo em radianos
    angle_rad = math.atan2(dy * StepsY, dx * StepsX)
    
    # Converter o ângulo para graus
    angle_deg = math.degrees(angle_rad)
    
    if not clockwise:
        # Se for anti-horário, ajustar o ângulo
        angle_deg = -angle_deg
    
    # Normalizar o ângulo para o intervalo [0, 360)
    angle_deg = angle_deg % 360
    
    # Garantir que o ângulo esteja no intervalo de 0 a 1 para o eixo A
    return angle_deg / 360.0

def process_tangential(gcode_lines):
    processed_gcode = []
    current_x, current_y = 0.0, 0.0
    prev_angle_a = None

    for line in gcode_lines:
        # Extrair valores de X e Y da linha
        x_final = extract_value(line, 'X')
        y_final = extract_value(line, 'Y')

        if x_final is not None and y_final is not None:
            dx = x_final - current_x
            dy = y_final - current_y
            
            # Determine se o movimento é no sentido horário ou anti-horário
            # Note: Neste caso, não estamos usando 'clockwise' aqui, mas pode ser ajustado se necessário
            clockwise = False
            
            angle_a = calculate_angle(dx, dy, clockwise)
            
            # Se o ângulo anterior está disponível, ajusta o ângulo para a direção correta
            if prev_angle_a is not None:
                delta_a = angle_a - prev_angle_a
                if delta_a > 0.5:
                    angle_a -= 1.0
                elif delta_a < -0.5:
                    angle_a += 1.0

            # Adicionar o comando com o ângulo calculado
            processed_gcode.append(f"G1 A{angle_a:.2f}")
            processed_gcode.append(line.strip())
            
            prev_angle_a = angle_a
            current_x, current_y = x_final, y_final
        else:
            # Se não há valores de X e Y, apenas adicione a linha sem modificação
            processed_gcode.append(line.strip())

    return processed_gcode
