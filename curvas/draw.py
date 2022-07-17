# Bibliotecas
import numpy as np
import matplotlib.pyplot as plt

# Variáveis globais
PI = np.pi

# Classes
# - Seta
class Arrow:
    # Inicialização
    def __init__(self, x, y, theta, L, c):
        # Valores arbitrários
        angle = np.deg2rad(30)
        d = 0.5 * L
        w = 2

        x_start = x
        y_start = y
        x_end = x + L * np.cos(theta)
        y_end = y + L * np.sin(theta)

        theta_hat_L = theta + PI - angle
        theta_hat_R = theta + PI + angle

        x_hat_start = x_end
        x_hat_end_L = x_hat_start + d * np.cos(theta_hat_L)
        x_hat_end_R = x_hat_start + d * np.cos(theta_hat_R)

        y_hat_start = y_end
        y_hat_end_L = y_hat_start + d * np.sin(theta_hat_L)
        y_hat_end_R = y_hat_start + d * np.sin(theta_hat_R)

        # Plot início e fim
        plt.plot([x_start, x_end], [y_start, y_end], color = c, linewidth = w)
        
        # Plot lado esquerdo (Left)
        plt.plot(
            [x_hat_start, x_hat_end_L],
            [y_hat_start, y_hat_end_L], 
            color = c, 
            linewidth = w
        )

        # Plot lado direito (Right)
        plt.plot(
            [x_hat_start, x_hat_end_R],
            [y_hat_start, y_hat_end_R], 
            color = c, 
            linewidth = w
        )


# - Carro
class Car:
    # Inicialização
    def __init__(self, x, y, yaw, w, L):
        theta_B = PI + yaw

        xB = x + L / 4 * np.cos(theta_B)
        yB = y + L / 4 * np.sin(theta_B)

        theta_BL = theta_B + PI / 2
        theta_BR = theta_B - PI / 2

        # Bottom-Left vertex    
        x_BL = xB + w / 2 * np.cos(theta_BL)       
        y_BL = yB + w / 2 * np.sin(theta_BL)

        # Bottom-Right vertex
        x_BR = xB + w / 2 * np.cos(theta_BR)        
        y_BR = yB + w / 2 * np.sin(theta_BR)

        # Front-Left vertex
        x_FL = x_BL + L * np.cos(yaw)               
        y_FL = y_BL + L * np.sin(yaw)

        # Front-Right vertex
        x_FR = x_BR + L * np.cos(yaw)               
        y_FR = y_BR + L * np.sin(yaw)

        # Visualização dos resultados
        plt.plot(
            [x_BL, x_BR, x_FR, x_FL, x_BL],
            [y_BL, y_BR, y_FR, y_FL, y_BL],
            linewidth = 1, 
            color = 'black'
        )

        Arrow(x, y, yaw, L / 2, 'black')


# Execução da classe Carro
if __name__ == '__main__':
    Car(0, 0, 1, 2, 60)