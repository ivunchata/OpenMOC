from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
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

# fuel surface
fuel_srf = Circle(x=0.0, y=0.0, radius=1.0, name='fuel surface')

# moderator surfaces
mod0 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=0, name='top left moderator surface')
mod1 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=1, name='left moderator surface')
mod2 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=2, name='bottom left moderator surface')
mod3 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=3, name='bottom right moderator surface')
mod4 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=4, name='right moderator surface')
mod5 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=5, name='top right moderator surface')

# bounding surfaces
a = 10.0
left  = XPlane(x=-a, name='left')
right = XPlane(x= a, name='right')
top   = YPlane(y=-a, name='top')
bot   = YPlane(y= a, name='bottom')
boundaries = [left, right, top, bot]

for boundary in boundaries: boundary.setBoundaryType(REFLECTIVE)

###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

fuel = CellBasic(name='fuel')
fuel.setMaterial(materials['UO2'])
fuel.addSurface(halfspace=-1, surface=fuel_srf)


root_cell = CellFill(name='root cell')
root_cell.addSurface(halfspace=+1, surface=boundaries[0])
root_cell.addSurface(halfspace=-1, surface=boundaries[1])
root_cell.addSurface(halfspace=+1, surface=boundaries[2])
root_cell.addSurface(halfspace=-1, surface=boundaries[3])


moderator = CellBasic(name='moderator')
moderator.setMaterial(materials['Water'])
moderator.addSurface(halfspace=+1, surface=fuel_srf)
moderator.addSurface(halfspace=-1, surface=mod0)
moderator.addSurface(halfspace=+1, surface=mod1)
moderator.addSurface(halfspace=-1, surface=mod2)
moderator.addSurface(halfspace=+1, surface=mod3)
moderator.addSurface(halfspace=-1, surface=mod4)
moderator.addSurface(halfspace=+1, surface=mod5)


###############################################################################
###########################   Creating Universes   ############################
###############################################################################

log.py_printf('NORMAL', 'Creating universes...')

pin_universe = Universe(name='fuel pin')
pin_universe.addCell(fuel)
pin_universe.addCell(moderator)

root_universe = Universe(name='root universe')
root_universe.addCell(root_cell)


###############################################################################
##########################   Creating Lattices   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating lattices...')
pin = Lattice(name='trivial one cell lattice')
pin.setWidth(width_x=a/2, width_y=a/2)
pin.setUniverses([pin_universe])

root_cell.setFill(pin)


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
geometry.setRootUniverse(root_universe)
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
