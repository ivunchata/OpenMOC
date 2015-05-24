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

pin = Circle(x=0.0, y=0.0, radius=1.0, name='pin')

#core = Circle(x=0.0, y=0.0, radius=3.0, name='core')
core0 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=0, name='core0')
core1 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=1, name='core1')
core2 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=2, name='core2')
core3 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=3, name='core3')
core4 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=4, name='core4')
core5 = HexPlane(x=0.0, y=0.0, radius=2.0, hex_id=5, name='core5')

left = XPlane(x=-10.0, name='left')
right = XPlane(x=10.0, name='right')
top = YPlane(y=10.0, name='top')
bottom = YPlane(y=-10.0, name='bottom')

left.setBoundaryType(VACUUM)
right.setBoundaryType(VACUUM)
top.setBoundaryType(VACUUM)
bottom.setBoundaryType(VACUUM)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

fuel = CellBasic(name='fuel')
fuel.setMaterial(materials['UO2'])
fuel.addSurface(halfspace=-1, surface=pin)

moderator = CellBasic(name='moderator')
moderator.setMaterial(materials['Water'])
moderator.addSurface(halfspace=+1, surface=pin)
moderator.addSurface(halfspace=-1, surface=core0)
moderator.addSurface(halfspace=+1, surface=core1)
moderator.addSurface(halfspace=-1, surface=core2)
moderator.addSurface(halfspace=+1, surface=core3)
moderator.addSurface(halfspace=-1, surface=core4)
moderator.addSurface(halfspace=+1, surface=core5)

empty = CellBasic(name='empty')
empty.setMaterial(materials['Water'])
empty.addSurface(halfspace=+1, surface=core0)
empty.addSurface(halfspace=-1, surface=core1)
empty.addSurface(halfspace=+1, surface=core2)
empty.addSurface(halfspace=-1, surface=core3)
empty.addSurface(halfspace=+1, surface=core4)
empty.addSurface(halfspace=-1, surface=core5)
empty.addSurface(halfspace=+1, surface=left)
empty.addSurface(halfspace=-1, surface=right)
empty.addSurface(halfspace=+1, surface=bottom)
empty.addSurface(halfspace=-1, surface=top)


###############################################################################
###########################   Creating Universes   ############################
###############################################################################

log.py_printf('NORMAL', 'Creating universes...')

root_universe = Universe(name='root universe')
root_universe.addCell(fuel)
root_universe.addCell(moderator)
root_universe.addCell(empty)


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
