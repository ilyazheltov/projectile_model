import numpy as np
from constants_and_variables import *
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares


def func(t, xyzdxdydz, ro0 = ro0, Cd = Cd, A = A, m = m, H = H, g = g):

    x, vx, y, vy, z, vz = xyzdxdydz
    
    dx_dt = vx
    dy_dt = vy
    dz_dt = vz

    temp = -(ro0 * Cd * A) / (2 * m)

    with np.errstate(invalid='ignore', divide='ignore'):
        return [
                dx_dt, 
                temp * np.e**(-z/H) * np.sqrt((dx_dt - np.log(10*z+1))**2 + (dy_dt - 2)**2 + dz_dt**2) * (dx_dt - 5*np.log(10*z+1)),
                dy_dt, 
                temp * np.e**(-z/H) * np.sqrt((dx_dt - np.log(10*z+1))**2 + (dy_dt - 2)**2 + dz_dt**2) * (dy_dt - 2),
                dz_dt, 
                -g + temp * np.e**(-z/H) * np.sqrt((dx_dt - np.log(10*z+1))**2 + (dy_dt - 2)**2 + dz_dt**2) * dz_dt
                ]

def objective_function(vars, start_coordinates = start_coordinates, target_coordinates = target_coordinates):

    t_end, teta, phi = vars
    x0, y0, z0 = start_coordinates
    xt, yt, zt = target_coordinates

    vx0 = v0 * np.cos(teta) * np.cos(phi)
    vy0 = v0 * np.cos(teta) * np.sin(phi)
    vz0 = v0 * np.sin(teta)
    
    r0v0 = [x0, vx0, y0, vy0, z0, vz0]

    sol = solve_ivp(func, t_span=(0, t_end), y0=r0v0)
    
    return [
        sol.y[0, -1] - xt,
        sol.y[2, -1] - yt,
        sol.y[4, -1] - zt
        ]

def find_angles():
    
    MAX_ACCEPTABLE_COST = 0.05 
    status_of_solution = False

    for initial_guess in initial_guess_mas:

        result = least_squares(
            objective_function,
            initial_guess,
            bounds=(lower_bounds, upper_bounds),
            method='trf',
            jac='2-point',
            xtol = 1e-2
        )

        if result.cost > MAX_ACCEPTABLE_COST:
            print(initial_guess, 'с такими числами большая погрешность')
            continue
        else:
            status_of_solution = True
            return result.x
        
    if not status_of_solution:
        print('Снаряд не сможет попасть в эту точку')
        return None

    
