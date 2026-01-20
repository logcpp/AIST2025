# Simulating transmittance of asymmetric MZM
# created on: 2026/01/21
# last change: 2026/01/21

import numpy as np
import matplotlib.pyplot as plt

phi_num = 6
phi_list = [np.pi * i/phi_num for i in range(phi_num)]

color_list = [
	'indianred',
	'sandybrown',
	'green',
	'lightseagreen',
	'blue',
	'darkorchid',
]

n_Si = 3.48
dL_list = [ # m, difference of optical path length
	1e-6,
	10e-6,
	20e-6,
	50e-6,
	100e-6,
	200e-6,
	500e-6,
]

lamb_min = 1530e-9 # m
lamb_max = 1565e-9 # m
lamb_num = 1000
lamb = np.linspace(lamb_min, lamb_max, lamb_num)

def amzm_transmittance(lamb, dL, phi):
	branch1 = 1/np.sqrt(2) # reference path
	branch2 = 1/np.sqrt(2) * np.exp(1j*2*np.pi*n_Si*dL/lamb + 1j*phi)
	return np.abs(1/np.sqrt(2) * (branch1 + branch2)) ** 2

def plot(x, y_list, phi_list, dL, color_list, filename):
	dlamb_FSR = (1550e-9*1550e-9)/(n_Si*dL)
	# print(f"[debug] dL={dL*1e6:.0f}um, dlamb_FSR={dlamb_FSR*1e9:.5f}nm")
	# multiple plot on one graph
	plt.rcParams["font.size"] = 16
	fig = plt.figure(figsize=(12,6))
	for i in range(len(y_list)):
		phi = phi_list[i]
		y = y_list[i]
		y_dB = 10*np.log10(y)
		color = color_list[i]
		plt.plot(x*1e9, y_dB, color=color, label="$\\phi=\\frac{"+f"{2*i}"+"\\pi}{"+f"{phi_num}"+"}$")
	plt.legend(loc='right', bbox_to_anchor=(1.2,0.5))
	plt.xlim([lamb_min*1e9, lamb_max*1e9])
	plt.ylim([-70, 0])
	plt.xlabel("Wavelength (nm)")
	plt.ylabel("Transmittance (dB)")
	plt.title(f"dL={dL*1e6:.0f}µm, "+"$\\Delta \\lambda_{FSR}="+f"{dlamb_FSR*1e9:.3f}$nm")
	plt.tight_layout()
	plt.savefig(filename)
	# free used memory
	plt.clf()
	plt.close()
	print(f"[out] saved figure as '{filename}'")

for dL in dL_list:
	y_list = []
	for i in range(phi_num):
		phi = phi_list[i]
		y = amzm_transmittance(lamb, dL, phi)
		y_list.append(y)
	plot(lamb, y_list, phi_list, dL, color_list, f"amzm_T_dL{dL*1e6:.0f}um.svg")
