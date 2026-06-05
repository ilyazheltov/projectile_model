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

N = 4
t_span = (0, 2*v0/g)

lower_bounds = [0, 0, 0]
upper_bounds = [2*v0/g, np.pi/2, np.pi*2]

initial_guess_mas = []
for t in range(0, N):
    for teta in range(0, N):
        for phi in range(0, N):
            t1 = t*upper_bounds[0]/(N+1) - 1e-5 if t != 0 else 0.01
            teta1 = teta*upper_bounds[1]/(N+1) - 1e-5 if teta != 0 else 0.01
            phi1 = phi*upper_bounds[2]/(N+1) - 1e-5 if phi != 0 else 0.01
            initial_guess_mas.append([t1, teta1, phi1])

while True:
    try:
        xt = float(input("x coordinate of target: "))
        yt = float(input("y coordinate of target: "))
        zt = float(input("z coordinate of target: "))
        target_coordinates = [xt, yt, zt]
        start_coordinates = [x0, y0, z0]

        if np.sqrt(xt**2 + yt**2) <= (v0**2)/g and zt <= (v0**2)/(2*g):
            break

        else:
            print("Снаряд не долетит до этой точки")
            print("Введите новые координаты")

    except KeyboardInterrupt:
        print("Программа была принудительно остановлена пользователем.") 
        
    except ValueError:
        print("Ошибка: Введите числа!")

       

