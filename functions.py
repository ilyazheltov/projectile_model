import numpy as np
from constants_and_variables import *
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import sympy as sp

def func(t, state, params, ro0=ro0, Cd=Cd, A=A, H=H, g=g):
    x, y, z, vx, vy, vz = state
    z_safe = max(z, 0.0) 
    
    m, v0, W_funcs = params
    Wx_func, Wy_func, Wz_func = W_funcs

    Wx = Wx_func(x, y, z_safe, vx, vy, vz)
    Wy = Wy_func(x, y, z_safe, vx, vy, vz)
    Wz = Wz_func(x, y, z_safe, vx, vy, vz)

    k = -(ro0 * np.exp(-z_safe / H) * Cd * A) / (2 * m)

    Vrel_x = vx - Wx
    Vrel_y = vy - Wy
    Vrel_z = vz - Wz
    
    Vrel_mod = np.sqrt(Vrel_x**2 + Vrel_y**2 + Vrel_z**2)
    
    ax = k * Vrel_mod * Vrel_x
    ay = k * Vrel_mod * Vrel_y
    az = -g + k * Vrel_mod * Vrel_z
    
    return [vx, vy, vz, ax, ay, az]


def objective_function(vars, start_coordinates, target_coordinates, params):
    t_end, teta, phi = vars
    x0, y0, z0 = start_coordinates
    xt, yt, zt = target_coordinates
    m, v0, W_funcs = params

    vx0 = v0 * np.cos(teta) * np.cos(phi)
    vy0 = v0 * np.cos(teta) * np.sin(phi)
    vz0 = v0 * np.sin(teta)
    
    r0v0 = [x0, y0, z0, vx0, vy0, vz0]

    sol = solve_ivp(func, t_span=(0, t_end), y0=r0v0, args=(params,))
    
    return [
        sol.y[0, -1] - xt,
        sol.y[1, -1] - yt,
        sol.y[2, -1] - zt
    ]

def find_angles(start_coordinates, target_coordinates, params):
    m, v0, W_str = params
    Wx_str, Wy_str, Wz_str = W_str

    x_sym, y_sym, z_sym, vx_sym, vy_sym, vz_sym = sp.symbols('x y z vx vy vz')

    Wx_func = sp.lambdify((x_sym, y_sym, z_sym, vx_sym, vy_sym, vz_sym), sp.sympify(Wx_str), "numpy")
    Wy_func = sp.lambdify((x_sym, y_sym, z_sym, vx_sym, vy_sym, vz_sym), sp.sympify(Wy_str), "numpy")
    Wz_func = sp.lambdify((x_sym, y_sym, z_sym, vx_sym, vy_sym, vz_sym), sp.sympify(Wz_str), "numpy")

    new_params = [m, v0, [Wx_func, Wy_func, Wz_func]]

    MAX_ACCEPTABLE_COST = 0.5 
    status_of_solution = False

    for initial_guess in initial_guess_mas:

        result = least_squares(
            objective_function,
            initial_guess,
            bounds=(lower_bounds, upper_bounds),
            method='trf',
            jac='2-point',
            xtol = 0.01,
            args=(start_coordinates, target_coordinates, new_params)
        )

        if result.cost < MAX_ACCEPTABLE_COST:
            status_of_solution = True
            return result.x
        
    if not status_of_solution:
        print('Снаряд не сможет попасть в эту точку')
        return None