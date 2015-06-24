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

log.set_log_level('DEBUG')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../c5g7-materials.h5')

###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circle = Circle(x=0.0, y=0.0, radius=0.45, name='fuel radius')

left = XPlane(x=-2.52, name='left')
right = XPlane(x=2.52, name='right')
bot = YPlane(y=-2.52, name='bottom')
top = YPlane(y=2.52, name='top')

left.setBoundaryType(openmoc.REFLECTIVE)
right.setBoundaryType(openmoc.REFLECTIVE)
bot.setBoundaryType(openmoc.REFLECTIVE)
top.setBoundaryType(openmoc.REFLECTIVE)

# Retrieve the fuel and moderator materials
uo2 = materials['UO2']
water = materials['Water']

# Initialize the cells for the fuel pin and moderator
# with optional string names
fuel = CellBasic(name='fuel cell')
moderator = CellBasic(name='moderator cell')

# Assign the appropriate materials to fill each cell
fuel.setMaterial(uo2)
moderator.setMaterial(water)

# Add the circle surface to each cell
fuel.addSurface(halfspace=-1, surface=circle)
moderator.addSurface(halfspace=+1, surface=circle)

# Initialize a universe with an optional string name
pin_univ = Universe(name='pin universe')
root_univ = Universe(name='root univ')

# Add each cell to the universe
pin_univ.addCell(fuel)
pin_univ.addCell(moderator)

root_cell = CellFill(name='root cell')
root_cell.setFill(pin_univ)

# Add the bounding planar surfaces to the root cell
root_cell.addSurface(halfspace=+1, surface=left)
root_cell.addSurface(halfspace=-1, surface=right)
root_cell.addSurface(halfspace=+1, surface=bot)
root_cell.addSurface(halfspace=-1, surface=top)

root_univ.addCell(root_cell)

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

