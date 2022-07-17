# Bibliotecas
import draw

import numpy as np
import matplotlib.pyplot as plt

from scipy.special import comb


# Funções
# - Calcula caminho de Bézier
def calc_bezier_path(control_points, n_points = 100):
    traj = []

    for t in np.linspace(0, 1, n_points):
        traj.append(bezier(t, control_points))

    return np.array(traj)

# - Calcula caminho de Bézieer dado 4 pontos de controle
def calc_4points_bezier_path(sx, sy, syaw, gx, gy, gyaw, offset):

    dist = np.hypot(sx - gx, sy - gy) / offset

    control_points = np.array([
        [sx, sy],
        [sx + dist * np.cos(syaw), sy + dist * np.sin(syaw)],
        [gx - dist * np.cos(gyaw), gy - dist * np.sin(gyaw)],
        [gx, gy]
    ])

    path = calc_bezier_path(control_points, n_points = 100)

    return path, control_points


# - Combinação
def Comb(n, i, t):
    return comb(n, i) * t ** i * (1 - t) ** (n - i)


# - Curvas cúbicas de Bézier
def bezier(t, control_points):
    n = len(control_points) - 1
    return np.sum([Comb(n, i, t) * control_points[i] for i in range(n + 1)], axis=0)


# - Derivadas dos pontos de controle
def bezier_derivatives_control_points(control_points, n_derivatives):
    w = {0: control_points}

    for i in range(n_derivatives):
        n = len(w[i])
        w[i + 1] = np.array([(n - 1) * (w[i][j + 1] - w[i][j]) for j in range(n - 1)])

    return w


# - Curvatura da curva
def curvature(dx, dy, ddx, ddy):
    return (dx * ddy - dy * ddx) / (dx ** 2 + dy ** 2) ** (3 / 2)


# - Fluxo principal
def main():
    # Premissas escolhidas arbitrariamente
    sx, sy, syaw = 10.0, 1.0, np.deg2rad(180.0)
    gx, gy, gyaw = 0.0, -3.0, np.deg2rad(-45.0)
    offset = 3.0

    # Cálculo da curva cúbica de Bézier para os pontos dados, considerando o offset
    path, control_points = calc_4points_bezier_path(sx, sy, syaw, gx, gy, gyaw, offset)

    # Número qualquer entre 0 e 1
    t = 0.8 

    # Cálculo dos pontos das curvas cúbicas 
    x_target, y_target = bezier(t, control_points)
    point = bezier(t, control_points)
    
    # Cálculo da primeira e segunda derivada dos pontos de controle
    derivatives_cp = bezier_derivatives_control_points(control_points, 2)
    dt = bezier(t, derivatives_cp[1])
    ddt = bezier(t, derivatives_cp[2])

    # Raio da curva
    radius = 1 / curvature(dt[0], dt[1], ddt[0], ddt[1])
    
    # Normalização das derivadas
    dt /= np.linalg.norm(dt, 2)
    tangent = np.array([point, point + dt])
    normal = np.array([point, point + [- dt[1], dt[0]]])
    curvature_center = point + np.array([- dt[1], dt[0]]) * radius
    circle = plt.Circle(
        tuple(curvature_center), 
        radius,
        color = (0, 0.8, 0.8), 
        fill = False, 
        linewidth = 1
    )

    # Conferindo resultados
    assert path.T[0][0] == sx, "path is invalid"
    assert path.T[1][0] == sy, "path is invalid"
    assert path.T[0][-1] == gx, "path is invalid"
    assert path.T[1][-1] == gy, "path is invalid"

    # Visualização dos resultados
    fig, ax = plt.subplots()
    ax.plot(path.T[0], path.T[1], label = "Bézier Path")
    ax.plot(control_points.T[0], control_points.T[1], '--o', label = "Control Points")
    ax.plot(x_target, y_target)
    ax.plot(tangent[:, 0], tangent[:, 1], label = "Tangent")
    ax.plot(normal[:, 0], normal[:, 1], label = "Normal")
    ax.add_artist(circle)
    ax.axis("equal")
    ax.legend()
    
    draw.Arrow(sx, sy, syaw, 1, "darkorange")
    draw.Arrow(gx, gy, gyaw, 1, "darkorange")
    
    plt.grid(True)
    plt.title("Bézier Path")
    plt.show()


# Executa fluxo principal
if __name__ == '__main__':
    main()