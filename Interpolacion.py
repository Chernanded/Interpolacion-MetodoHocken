"""Diseño óptimo de mecanismos de cuatro barras de línea recta
"""
import pandas as pd
from scipy.interpolate import interp1d
import math
import statistics

# Arrays con los datos de la tabla 3-1
# ||Range of motion||:|Crack angle range|;|Theta start|;|Percent of cycle|
#ΔB
crack_angle_range = [20,40,60,80,100,120,140,160,180]

#theta_start (deg)
θ1= [170,160,150,140,130,120,110,100,90]#Deg
θ1 = [math.radians(x) for x in θ1]#Trasformamos los grados a radianes
θ1 = [round(x,3) for x in θ1]#Redondeamos a 3 decimales es decir w2 velocidad angular

#percent_of_cycle (Porcentaje de ciclo)
percent_of_cycle = [5.6,11.1,16.7,22.2,27.8,33.3,38.9,44.4,50.0]

#range_of_motion (Rango de movimiento)
#Creamos un diccionario llamado range_of_motion con los 3 anteriores arrays, luego imprimios el diccionario
range_of_motion = {'crack_angle_range':crack_angle_range,'θ1':θ1,'percent_of_cycle':percent_of_cycle}
print(f'El diccionario range_of_motion es:\n {range_of_motion}')


#Creamos un dataframe llamado range_of_motion_df con los 3 anteriores arrays, luego imprimios el dataframe
range_of_motion_df = pd.DataFrame(range_of_motion)
print(f'El dataframe range_of_motion_df es: {range_of_motion_df} \n')


# #||Optimized for straightness||:|Minimum ΔCy percent|;|ΔV percent|;|Vx /(L2*W2)|;|L1/L2|;|L3/L2|;|ΔX/L2|

#minimum_ΔCy_percent
minimum_ΔCy_percent = [0.00001,0.00004,0.00027,0.001,0.004,0.010,0.023,0.047,0.096]
#ΔV_percent
ΔV_percent = [0.38,1.53,3.48,6.27,9.90,14.68,20.48,27.15,35.31]
#Vx_L2_W2
Vx_L2_W2 = [1.725,1.717,1.702,1.679,1.646,1.611,1.565,1.504,1.436]
# L1/L2
L1_L2_opt1 = [2.975,2.950,2.900,2.825,2.725,2.625,2.500,2.350,2.200]

# L3/L2
L3_L2_opt1 = [3.963,3.925,3.850,3.738,3.588,3.438,3.250,3.025,2.800]

#ΔX/L2
ΔX_L2_opt1 = [0.601,1.193,1.763,2.299,2.790,3.238,3.623,3.933,4.181]

#Creamos un diccionario llamado optimized_for_straightness con los 6 anteriores arrays, luego imprimios el diccionario
optimized_for_straightness = {'minimum_ΔCy_percent':minimum_ΔCy_percent,'ΔV_percent':ΔV_percent,'Vx_L2_W2':Vx_L2_W2,'L1_L2_opt':L1_L2_opt1,'L3_L2_opt':L3_L2_opt1,'ΔX_L2_opt':ΔX_L2_opt1}
#Creamos un dataframe llamado optimized_for_straightness_df con los 6 anteriores arrays, luego imprimios el dataframe
optimized_for_straightness_df = pd.DataFrame(optimized_for_straightness)
#print(f'El dataframe optimized_for_straightness_df es:\n {optimized_for_straightness_df}\n')

# Interpolación polinómica de los valores óptimos de percent_of_cycle
interp_percent_of_cycle = interp1d(crack_angle_range, percent_of_cycle, kind='cubic')
print(f'El valor de interp_percent_of_cycle es:\n {interp_percent_of_cycle}\n')

# # Valor del ángulo de las barras para el cual se desea calcular las razones geométricas óptimas
angle = 55
# # Cálculo de las razones geométricas óptimas
percent_of_cycle_interp = interp_percent_of_cycle(angle)
print(f'El valor de percent_of_cycle_interp es: {percent_of_cycle_interp.round(3)}\n')

# Interpolación polinómica de los valores óptimos de L1/L2
interp_L1_L2 = interp1d(crack_angle_range, L1_L2_opt1, kind='cubic')

#Interpolación polinómica de los valores óptimos de L3/L2
interp_L3_L2 = interp1d(crack_angle_range, L3_L2_opt1, kind='cubic')

#Interpolación polinómica de los valores óptimos de ΔX/L2
interp_ΔX_L2 = interp1d(crack_angle_range, ΔX_L2_opt1, kind='cubic')

#Para redondear los valores de las razones geométricas óptimas en 3 decimales
fix=3
#Cálculo de las razones geométricas óptimas
L1_L2_opt_interp = interp_L1_L2(angle).round(fix)
L3_L2_opt_interp = interp_L3_L2(angle).round(fix)
ΔX_L2_opt_interp = interp_ΔX_L2(angle).round(fix)

#Traigo las interpolaciones de las razones geométricas óptimas
print(f'Razón geométrica L1/L2 óptima:  {L1_L2_opt_interp}')
print(f'Razón geométrica L3/L2 óptima: { L3_L2_opt_interp }')
print(f'Razón geométrica ΔX/L2 óptima: {ΔX_L2_opt_interp}')
#Hallamos L1, L2 y L3, mediante las razones geométricas óptimas
ΔX=200 #mm (20 cm)
L2=(ΔX/ΔX_L2_opt_interp).round(fix)
print(f'L2 = {L2} mm')
L1=(L1_L2_opt_interp*L2).round(fix)
print(f'L1 = {L1} mm')
L3=(L3_L2_opt_interp*L2).round(fix)
print(f'L3 = {L3} mm')
#Mediante list comprehension hallamos  Vx multiplicando L2 por la lista θ1y redondiamos a 3 cifras decimales
Vx=[(L2*θ1).round(fix) for θ1 in θ1]
print(f'Vx = {Vx} mm/s\n')


# Error en rectitud
error_straightness = ((max(Vx) - min(Vx)) / (ΔX)).round(fix)
print(f'El error en rectitud es: {error_straightness}\n')



##################################################################################################################################################################################################


# |Optimized for constant velocity|:|Minimum ΔVx percent|;|ΔCy percent|;|Vx /(L2*W2)|;|L1/L2|;|L3/L2|;|ΔX/L2|
# minimum_ΔVx_percent
minimum_ΔVx_percent = [0.006,0.038,0.106,0.340,0.910,1.885,3.327,5.878,9.299]
#ΔCy_percent
ΔCy_percent = [0.137,0.274,0.387,0.503,0.640,0.752,0.888,1.067,1.446]
#Vx_L2_W2
Vx_L2_W2_2 = [1.374,1.361,1.347,1.319,1.275,1.229,1.178,1.124,1.045]
# L1/L2
L1_L2_opt2 = [2.075,2.050,2.025,1.975,1.900,1.825,1.750,1.675,1.575]
# L3/L2
L3_L2_opt2 = [2.613,2.575,2.538,2.463,2.350,2.238,2.125,2.013,1.863]
#ΔX/L2
ΔX_L2_opt2 = [0.480,0.950,1.411,1.845,2.237,2.600,2.932,3.232,3.456]
#Creamos un diccionario llamado optimized_for_constant_velocity con los 6 anteriores arrays, luego imprimios el diccionario
optimized_for_constant_velocity = {'minimum_ΔVx_percent':minimum_ΔVx_percent,'ΔCy_percent':ΔCy_percent,'Vx_L2_W2':Vx_L2_W2_2,'L1_L2_opt2':L1_L2_opt2,'L3_L2_opt2':L3_L2_opt2,'ΔX_L2_opt_2':ΔX_L2_opt2}
#Creamos un dataframe llamado optimized_for_constant_velocity_df con los 6 anteriores arrays, luego imprimios el dataframe
optimized_for_constant_velocity_df = pd.DataFrame(optimized_for_constant_velocity)
# print(f'El dataframe optimized_for_constant_velocity_df es:\n {optimized_for_constant_velocity_df}\n')

# Interpolación polinómica de los valores óptimos de L1/L2
interp_L1_L2_2 = interp1d(crack_angle_range, L1_L2_opt2, kind='cubic')

#Interpolación polinómica de los valores óptimos de L3/L2
interp_L3_L2_2 = interp1d(crack_angle_range, L3_L2_opt2, kind='cubic')

#Interpolación polinómica de los valores óptimos de ΔX/L2
interp_ΔX_L2_2 = interp1d(crack_angle_range, ΔX_L2_opt2, kind='cubic')

fix=3
#Cálculo de las razones geométricas óptimas
L1_L2_opt_interp_2 = interp_L1_L2_2(angle).round(fix)
L3_L2_opt_interp_2 = interp_L3_L2_2(angle).round(fix)
ΔX_L2_opt_interp_2 = interp_ΔX_L2_2(angle).round(fix)

print(f'Razón geométrica L1/L2 óptima:  {L1_L2_opt_interp_2}')
print(f'Razón geométrica L3/L2 óptima: { L3_L2_opt_interp_2}')
print(f'Razón geométrica ΔX/L2 óptima: {ΔX_L2_opt_interp_2}')
#Hallamos L1, L2 y L3, mediante las razones geométricas óptimas
ΔX=200 #mm
L2_2=(ΔX/ΔX_L2_opt_interp_2).round(fix)
print(f'L2 = {L2_2} mm')
L1_2=(L1_L2_opt_interp_2*L2_2).round(fix)
print(f'L1 = {L1_2} mm')
L3_2=(L3_L2_opt_interp_2*L2_2).round(fix)
print(f'L3 = {L3_2} mm')
#Mediante list comprehension hallamos  Vx multiplicando L2 por la lista θ1y redondiamos a 3 cifras decimales
Vx_2=[(L2_2*θ1).round(fix) for θ1 in θ1]
print(f'Vx = {Vx_2} mm/s \n')


# # Error en velocidad
error_velocity = ((max(Vx_2) - min(Vx_2)) / statistics.mean(Vx_2)).round(fix)

print(f'El error en rectitud:  {error_straightness}\n')

##################################################################################################################################################################################################
print(f'Error en rectitud:  {error_straightness}')
print(f'Error en velocidad: {error_velocity}')



