# TFY41xx Fysikk vaaren 2021.
#
# Programmet tar utgangspunkt i hoeyden til de 8 festepunktene.
# Deretter beregnes baneformen y(x) ved hjelp av 7 tredjegradspolynomer, 
# et for hvert intervall mellom to festepunkter, slik at baade banen y, 
# dens stigningstall y' = dy/dx og dens andrederiverte
# y'' = d2y/dx2 er kontinuerlige i de 6 indre festepunktene.
# I tillegg velges null krumning (andrederivert) 
# i banens to ytterste festepunkter (med bc_type='natural' nedenfor).
# Dette gir i alt 28 ligninger som fastlegger de 28 koeffisientene
# i de i alt 7 tredjegradspolynomene.

# De ulike banene er satt opp med tanke paa at kula skal 
# (1) fullfoere hele banen selv om den taper noe mekanisk energi underveis;
# (2) rulle rent, uten aa gli ("slure").

# Vi importerer noedvendige biblioteker:
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from math import atan2

# Horisontal avstand mellom festepunktene er 0.200 m
h = 0.200
xfast = np.asarray([0, h, 2 * h, 3 * h, 4 * h, 5 * h, 6 * h, 7 * h])

# Vi begrenser starthøyden (og samtidig den maksimale høyden) til
# å ligge mellom 250 og 300 mm
ymax = 300
# yfast: tabell med 8 heltall mellom 50 og 300 (mm); representerer
# høyden i de 8 festepunktene
yfast = np.array([0.28, 0.231, 0.216, 0.155, 0.128, 0.147, 0.121, 0.069])

# Omregning fra mm til m:
# xfast = xfast/1000
# yfast = yfast/1000

# Når programmet her har avsluttet while-løkka, betyr det at
# tallverdiene i tabellen yfast vil resultere i en tilfredsstillende bane. 

# Programmet beregner deretter de 7 tredjegradspolynomene, et
# for hvert intervall mellom to nabofestepunkter.


# Med scipy.interpolate-funksjonen CubicSpline:
cs = CubicSpline(xfast, yfast, bc_type='natural')

xmin = 0.000
xmax = 1.401
dx = 0.001

x = np.arange(xmin, xmax, dx)

# funksjonen arange returnerer verdier paa det "halvaapne" intervallet
# [xmin,xmax), dvs slik at xmin er med mens xmax ikke er med. Her blir
# dermed x[0]=xmin=0.000, x[1]=xmin+1*dx=0.001, ..., x[1400]=xmax-dx=1.400,
# dvs x blir en tabell med 1401 elementer
Nx = len(x)
y = cs(x)  # y=tabell med 1401 verdier for y(x)
dy = cs(x, 1)  # dy=tabell med 1401 verdier for y'(x)
d2y = cs(x, 2)  # d2y=tabell med 1401 verdier for y''(x)

# Eksempel: Plotter banens form y(x)

# Figurer kan lagres i det formatet du foretrekker:
# baneform.savefig("baneform.pdf", bbox_inches='tight')
# baneform.savefig("baneform.png", bbox_inches='tight')
# baneform.savefig("baneform.eps", bbox_inches='tight')

highest_point = np.max(y)

g = 9.81
c = 0.4
M = 0.031  # PLACEHOLDER
speed = np.sqrt((highest_point - y) * g * 2 / (1 + c))

angles = np.arctan(dy)
speedx = speed * np.cos(angles)
curvature = d2y / (np.power(1 + np.power(dy, 2), 3 / 2))
centripetal_acceleration = speed ** 2 * curvature
normal = M * (g * np.cos(angles) + centripetal_acceleration) / (M * g)

friction = c * M * g * np.sin(angles) / (1 + c)
time = np.concatenate((np.array([0]), (2 * dx * np.cumsum(1 / (speedx[1:] + speedx[:-1])))))

print('Festepunkthøyder (m)', yfast)
print('Banens høyeste punkt (m)', np.max(y))

print('NB: SKRIV NED festepunkthøydene når du/dere er fornøyd med banen.')
print('Eller kjør programmet på nytt inntil en attraktiv baneform vises.')

print(time)
baneform = plt.figure('y(x)', figsize=(12, 6))


def plot(x, y, x_name, y_name, title, /, x_points=[], y_points=[]):
    if (len(x_points) and len(y_points)):
        plt.plot(x, y, x_points, y_points, '*')
    else:
        plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_name, fontsize=20)
    plt.ylabel(y_name, fontsize=20)
    plt.grid()
    plt.show()


plot(x, y, "$x$ (m)", "$y(x)$ (m)", "Banens form", x_points=xfast, y_points=yfast)
plot(x, speed, "$x$ (m)", "v (m/s)", "Fart")
plot(x, angles, "$x$ (m)", "β (°)", "Vinkel")
plot(x, curvature, "$x$ (m)", "K(x) (m⁻¹)", "Kurve")
plot(x, normal, "$x$ (m)", "N/Mg", "Normalkraft")
plot(x, abs(friction / normal), "$x$ (m)", "|f/N|", "Friksjon / Normalkraft")
plot(time, x, "$t$ (s)", "x (m)", "Posisjon pr tid")
plot(time, speed, "$t$ (s)", "v (m/s)", "Fart pr tid")
