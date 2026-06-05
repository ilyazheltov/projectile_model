import numpy as np
from constants_and_variables import *
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

def func(t, state, ro0=ro0, Cd=Cd, A=A, m=m, H=H, g=g):

    x, y, z, vx, vy, vz = state
    
    z_safe = max(z, 0.0)
    
    Wx = 5.0 * np.log(10 * z_safe + 1)
    Wy = 2.0
    
    Vrel_x = vx - Wx
    Vrel_y = vy - Wy
    Vrel_z = vz
    
    Vrel_mod = np.sqrt(Vrel_x**2 + Vrel_y**2 + Vrel_z**2)
    
    k = -(ro0 * np.exp(-z_safe / H) * Cd * A) / (2 * m)
    
    ax = k * Vrel_mod * Vrel_x
    ay = k * Vrel_mod * Vrel_y
    az = -g + k * Vrel_mod * Vrel_z
    
    return [vx, vy, vz, ax, ay, az]


def objective_function(vars, start_coordinates = start_coordinates, target_coordinates = target_coordinates):

    t_end, teta, phi = vars
    x0, y0, z0 = start_coordinates
    xt, yt, zt = target_coordinates

    vx0 = v0 * np.cos(teta) * np.cos(phi)
    vy0 = v0 * np.cos(teta) * np.sin(phi)
    vz0 = v0 * np.sin(teta)
    
    r0v0 = [x0, y0, z0, vx0, vy0, vz0]

    sol = solve_ivp(func, t_span=(0, t_end), y0=r0v0)
    
    return [
        sol.y[0, -1] - xt,
        sol.y[1, -1] - yt,
        sol.y[2, -1] - zt
        ]

def find_angles():
    
    MAX_ACCEPTABLE_COST = 0.5 
    status_of_solution = False

    for initial_guess in initial_guess_mas:

        result = least_squares(
            objective_function,
            initial_guess,
            bounds=(lower_bounds, upper_bounds),
            method='trf',
            jac='2-point',
            xtol = 0.01
        )

        if result.cost < MAX_ACCEPTABLE_COST:
            status_of_solution = True
            return result.x
        
    if not status_of_solution:
        print('Снаряд не сможет попасть в эту точку')
        return None

