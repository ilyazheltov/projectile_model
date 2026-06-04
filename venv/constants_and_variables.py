import numpy as np

g = 9.81
ro0 = 1.225
H = 10000
m = 45
A = 0.02
Cd = 0.3
v0 = 800

x0 = 0
y0 = 0
z0 = 0

N = 1000
t_span = (0, 2.2*v0/g)
t_eval = np.linspace(0, 2.2*v0/g, 2000)

initial_guess = [60, np.pi/4, np.pi/4]
lower_bounds = [0, 0, 0]
upper_bounds = [2.2*v0/g, np.pi/2, np.pi*2]

while True:
    try:
        xt = float(input("x coordinate of target: "))
        yt = float(input("y coordinate of target: "))
        zt = float(input("z coordinate of target: "))
        target_coordinates = [xt, yt, zt]
        start_coordinates = [x0, y0, z0]
        break
    except ValueError:
        print("Ошибка: Введите числа!")
