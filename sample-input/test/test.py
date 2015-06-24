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
sleft = XPlane(x=-a/2, name='sleft')
sright = XPlane(x=a/2, name='sright')
sbot = YPlane(y=-a/2, name='sbottom')
stop = YPlane(y=a/2, name='stop')

# root cell/universe boundaries
left = XPlane(x=-a, name='left')
right = XPlane(x=a, name='right')
bot = YPlane(y=-a, name='bottom')
top = YPlane(y=a, name='top')
left.setBoundaryType(openmoc.REFLECTIVE)
right.setBoundaryType(openmoc.REFLECTIVE)
bot.setBoundaryType(openmoc.REFLECTIVE)
top.setBoundaryType(openmoc.REFLECTIVE)

# Retrieve the fuel and moderator materials
uo2 = materials['UO2']
water = materials['Water']
gt = materials['Guide Tube']

# Initialize the cells 
fuel = CellBasic(name='fuel cell')
moderator = CellBasic(name='moderator cell')
remainder = CellBasic(name='wut?')
root_cell = CellFill(name='root cell')

# set materials
fuel.setMaterial(uo2)
moderator.setMaterial(water)
remainder.setMaterial(uo2)

# add surfaces
fuel.addSurface(halfspace=-1, surface=circle)

moderator.addSurface(halfspace=+1, surface=circle)
moderator.addSurface(halfspace=+1, surface=sleft)
moderator.addSurface(halfspace=-1, surface=sright)
moderator.addSurface(halfspace=+1, surface=sbot)
moderator.addSurface(halfspace=-1, surface=stop)
moderator.printString()

remainder.addSurface(halfspace=-1, surface=sleft)
remainder.addSurface(halfspace=+1, surface=sright)
remainder.addSurface(halfspace=-1, surface=sbot)
remainder.addSurface(halfspace=+1, surface=stop)
remainder.addSurface(halfspace=+1, surface=left)
remainder.addSurface(halfspace=-1, surface=right)
remainder.addSurface(halfspace=+1, surface=bot)
remainder.addSurface(halfspace=-1, surface=top)
remainder.printString()

# Add the bounding planar surfaces to the root cell
root_cell.addSurface(halfspace=+1, surface=left)
root_cell.addSurface(halfspace=-1, surface=right)
root_cell.addSurface(halfspace=+1, surface=bot)
root_cell.addSurface(halfspace=-1, surface=top)

# Initialize a universes 
pin_univ = Universe(name='pin universe')
root_univ = Universe(name='root univ')

# Add each cell to the universe
pin_univ.addCell(fuel)
pin_univ.addCell(moderator)
pin_univ.addCell(remainder)
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

