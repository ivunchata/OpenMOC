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

fuel = Circle(x=0.0, y=0.0, radius=a/10, name='fuel surface')

# root cell/universe boundaries
root_left = XPlane(x=-a, name='outer left')
root_right = XPlane(x=a, name='outer right')
root_bot = YPlane(y=-a, name='outer bottom')
root_top = YPlane(y=a, name='outer top')
root_left.setBoundaryType(openmoc.REFLECTIVE)
root_right.setBoundaryType(openmoc.REFLECTIVE)
root_bot.setBoundaryType(openmoc.REFLECTIVE)
root_top.setBoundaryType(openmoc.REFLECTIVE)

# moderator surfaces and cells
mod_surface = []
for i in range(6):
    mod_surface.append(HexPlane(x=0.0, y=0.0, radius=a/2, hex_id=i, name='Hexagonal surface no. ' + str(i)))

# helper surfaces
mid_axis = XPlane(x=0.0, name='vertical trough the hexagon\'s center')

# Retrieve the materials
uo2 = materials['UO2']
water = materials['Water']
gt = materials['Guide Tube']


# setup cells
pin_fuel = CellBasic(name='pin cell fuel')
pin_mod = CellBasic(name='pin cell moderator')

mod_cell = []
for i in range(6):
    mod_cell.append(CellBasic(name='Surrounding cell no. '  + str(i)))

root_cell = CellFill(name='root cell')

# set materials
pin_fuel.setMaterial(uo2)
pin_mod.setMaterial(water)
for i in range(6):
    mod_cell[i].setMaterial(water)

# attach surfaces
pin_fuel.addSurface(halfspace=-1, surface=fuel)

pin_mod.addSurface(halfspace=+1, surface=fuel)
for i in range(6):
    sign_one = pow(-1, i+1)
    pin_mod.addSurface(halfspace=pow(-1, i+1), surface=mod_surface[i])

mod_cell[0].addSurface(halfspace=+1, surface=mod_surface[1])
mod_cell[0].addSurface(halfspace=-1, surface=mid_axis)
mod_cell[0].addSurface(halfspace=+1, surface=mod_surface[0])
mod_cell[0].addSurface(halfspace=-1, surface=root_top)

mod_cell[1].addSurface(halfspace=+1, surface=root_left)
mod_cell[1].addSurface(halfspace=-1, surface=mod_surface[1])
mod_cell[1].addSurface(halfspace=+1, surface=root_bot)
mod_cell[1].addSurface(halfspace=-1, surface=root_top)

mod_cell[2].addSurface(halfspace=+1, surface=mod_surface[1])
mod_cell[2].addSurface(halfspace=-1, surface=mid_axis)
mod_cell[2].addSurface(halfspace=+1, surface=root_bot)
mod_cell[2].addSurface(halfspace=-1, surface=mod_surface[2])

mod_cell[3].addSurface(halfspace=+1, surface=mid_axis)
mod_cell[3].addSurface(halfspace=-1, surface=mod_surface[4])
mod_cell[3].addSurface(halfspace=+1, surface=root_bot)
mod_cell[3].addSurface(halfspace=-1, surface=mod_surface[3])

mod_cell[1].addSurface(halfspace=+1, surface=mod_surface[4])
mod_cell[1].addSurface(halfspace=-1, surface=root_right)
mod_cell[1].addSurface(halfspace=+1, surface=root_bot)
mod_cell[1].addSurface(halfspace=-1, surface=root_top)

mod_cell[5].addSurface(halfspace=+1, surface=mid_axis)
mod_cell[5].addSurface(halfspace=-1, surface=mod_surface[4])
mod_cell[5].addSurface(halfspace=+1, surface=mod_surface[5])
mod_cell[5].addSurface(halfspace=-1, surface=root_top)

# Add the bounding planar surfaces to the root cell
root_cell.addSurface(halfspace=+1, surface=root_left)
root_cell.addSurface(halfspace=-1, surface=root_right)
root_cell.addSurface(halfspace=+1, surface=root_bot)
root_cell.addSurface(halfspace=-1, surface=root_top)

# Initialize a universes
pin_univ = Universe(name='pin universe')
root_univ = Universe(name='root univ')

# Add each cell to the universe
for i in range(6):
    pin_univ.addCell(mod_cell[i])

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

