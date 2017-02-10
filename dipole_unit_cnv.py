import numpy as np

### physics constants
cl  = 299792458e0 # speed of light [m/s]
amu = 931.49432e6 # atomic mass unit [eV/c^2]
ics = 33.0/238.0  # ion charge state

### sample sbend/edipole parameter
L   = 1.0  # L in lattice file [m]
phi = 90.0 # phi in latticec file [deg.]


### sbend unit conversion
# bg to B [T]
def bg_to_B(bg):
	irho = phi/360.0*2.0*np.pi/L
	B =  irho/ics*amu/cl*bg
	return B

# B [T] to bg
def B_to_bg(B):
	irho = phi/360.0*2.0*np.pi/L
	bg = 1.0/irho*ics/amu*cl*B
	return bg

### edipole unit conversion
# beta to E [V/m]
def beta_to_E(beta):
	irho = phi/360.0*2.0*np.pi/L
	E = irho/ics*amu*beta*beta
	return E

# E [V/m] to beta
def E_to_beta(E):
	irho = phi/360.0*2.0*np.pi/L
	beta = np.sqrt(1.0/irho*ics/amu*E)
	return beta
