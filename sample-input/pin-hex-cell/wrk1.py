from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = 1 #options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()

#log.set_log_level('DEBUG')
log.set_log_level('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../c5g7-materials.h5')

###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')
a=10.0
circle = Circle(x=0.0, y=0.0, radius=a/20, name='fuel radius')

# small cell within the root
sleft = XPlane(x=-a/2, name='inner left')
sright = XPlane(x=a/2, name='inner right')
sbot = YPlane(y=-a/2, name='inner bottom')
stop = YPlane(y=a/2, name='inner top')

# root cell/universe boundaries
lleft = XPlane(x=-a, name='outer left')
lright = XPlane(x=a, name='outer right')
lbot = YPlane(y=-a, name='outer bottom')
ltop = YPlane(y=a, name='outer top')
lleft.setBoundaryType(openmoc.REFLECTIVE)
lright.setBoundaryType(openmoc.REFLECTIVE)
lbot.setBoundaryType(openmoc.REFLECTIVE)
ltop.setBoundaryType(openmoc.REFLECTIVE)

# Retrieve the fuel and pid_mod materials
uo2 = materials['UO2']
water = materials['Water']
gt = materials['Guide Tube']

# Initialize the cells 
pin_fuel = CellBasic(name='fuel in the pin cell')
pin_mod = CellBasic(name='moderator in the pin cell')
left_cell = CellBasic(name='cell left from the pin')
right_cell = CellBasic(name='cell right from the pin')
top_cell = CellBasic(name='cell top from the pin')
bot_cell = CellBasic(name='cell bot from the pin')

root_cell = CellFill(name='root cell')

# set materials
pin_fuel.setMaterial(uo2)
pin_mod.setMaterial(water)
left_cell.setMaterial(water)
right_cell.setMaterial(water)
top_cell.setMaterial(water)
bot_cell.setMaterial(water)

# add surfaces
pin_fuel.addSurface(halfspace=-1, surface=circle)

pin_mod.addSurface(halfspace=+1, surface=circle)
pin_mod.addSurface(halfspace=+1, surface=sleft)
pin_mod.addSurface(halfspace=-1, surface=sright)
pin_mod.addSurface(halfspace=+1, surface=sbot)
pin_mod.addSurface(halfspace=-1, surface=stop)

left_cell.addSurface(halfspace=+1, surface=lleft)
left_cell.addSurface(halfspace=-1, surface=sleft)
left_cell.addSurface(halfspace=+1, surface=lbot)
left_cell.addSurface(halfspace=-1, surface=ltop)

right_cell.addSurface(halfspace=+1, surface=sright)
right_cell.addSurface(halfspace=-1, surface=lright)
right_cell.addSurface(halfspace=+1, surface=lbot)
right_cell.addSurface(halfspace=-1, surface=ltop)

top_cell.addSurface(halfspace=+1, surface=sleft)
top_cell.addSurface(halfspace=-1, surface=sright)
top_cell.addSurface(halfspace=+1, surface=stop)
top_cell.addSurface(halfspace=-1, surface=ltop)

bot_cell.addSurface(halfspace=+1, surface=sleft)
bot_cell.addSurface(halfspace=-1, surface=sright)
bot_cell.addSurface(halfspace=+1, surface=lbot)
bot_cell.addSurface(halfspace=-1, surface=sbot)

# Add the bounding planar surfaces to the root cell
root_cell.addSurface(halfspace=+1, surface=lleft)
root_cell.addSurface(halfspace=-1, surface=lright)
root_cell.addSurface(halfspace=+1, surface=lbot)
root_cell.addSurface(halfspace=-1, surface=ltop)

# Initialize a universes 
pin_univ = Universe(name='pin universe')
root_univ = Universe(name='root univ')

# Add each cell to the universe
pin_univ.addCell(pin_fuel)
pin_univ.addCell(pin_mod)
pin_univ.addCell(left_cell)
pin_univ.addCell(right_cell)
pin_univ.addCell(top_cell)
pin_univ.addCell(bot_cell)

root_univ.addCell(root_cell)
root_cell.setFill(pin_univ)


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
geometry.setRootUniverse(root_univ)
geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = CPUSolver(geometry, track_generator)
solver.setNumThreads(num_threads)
solver.setSourceConvergenceThreshold(tolerance)
solver.convergeSource(max_iters)
solver.printTimerReport()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

#plotter.plot_tracks(track_generator)
#plotter.plot_segments(track_generator)
#plotter.plot_materials(geometry, gridsize=500)
plotter.plot_cells(geometry, gridsize=500)
#plotter.plot_flat_source_regions(geometry, gridsize=500)
#plotter.plot_fluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')

