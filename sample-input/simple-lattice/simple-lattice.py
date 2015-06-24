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
track_spacing = options.getTrackSpacing() / 2
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()*10
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
a = 12.0
left = XPlane(x=-a, name='left')
right = XPlane(x=a, name='right')
top = YPlane(y=-a, name='top')
bottom = YPlane(y=a, name='bottom')
boundaries = [left, right, top, bottom]

large_circle = Circle(x=0.0, y=0.0, radius=a/15, name='large pin')
medium_circle = Circle(x=0.0, y=0.0, radius=a/20, name='medium pin')
small_circle = Circle(x=0.0, y=0.0, radius=a/30, name='small pin')

for boundary in boundaries: boundary.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

large_fuel = CellBasic(name='large pin fuel', rings=1, sectors=8)
large_fuel.setMaterial(materials['UO2'])
large_fuel.addSurface(halfspace=-1, surface=large_circle)

large_moderator = CellBasic(name='large pin moderator', sectors=8)
large_moderator.setMaterial(materials['Water'])
large_moderator.addSurface(halfspace=+1, surface=large_circle)

medium_fuel = CellBasic(name='medium pin fuel', rings=3, sectors=5)
medium_fuel.setMaterial(materials['UO2'])
medium_fuel.addSurface(halfspace=-1, surface=medium_circle)

medium_moderator = CellBasic(name='medium pin moderator', sectors=3)
medium_moderator.setMaterial(materials['Water'])
medium_moderator.addSurface(halfspace=+1, surface=medium_circle)

small_fuel = CellBasic(name='small pin fuel', rings=3, sectors=8)
small_fuel.setMaterial(materials['UO2'])
small_fuel.addSurface(halfspace=-1, surface=small_circle)

small_moderator = CellBasic(name='small pin moderator', sectors=8)
small_moderator.setMaterial(materials['Water'])
small_moderator.addSurface(halfspace=+1, surface=small_circle)

root_cell = CellFill(name='root cell')
root_cell.addSurface(halfspace=+1, surface=boundaries[0])
root_cell.addSurface(halfspace=-1, surface=boundaries[1])
root_cell.addSurface(halfspace=+1, surface=boundaries[2])
root_cell.addSurface(halfspace=-1, surface=boundaries[3])


###############################################################################
#                            Creating Universes
###############################################################################

log.py_printf('NORMAL', 'Creating universes...')

pin1 = Universe(name='large pin cell')
pin2 = Universe(name='medium pin cell')
pin3 = Universe(name='small pin cell')
root_universe = Universe(name='root universe')

pin1.addCell(large_fuel)
pin1.addCell(large_moderator)
pin2.addCell(medium_fuel)
pin2.addCell(medium_moderator)
pin3.addCell(small_fuel)
pin3.addCell(small_moderator)
root_universe.addCell(root_cell)


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple 4 x 4 lattice...')

lattice = Lattice(name='5x5 lattice')
lattice.setWidth(width_x=a/3, width_y=a/3)
lattice.setNumX(2);
lattice.setNumY(2);
#lattice.setOffset(a/5, a/5)
# lattice.setUniverses([[pin1, pin2, pin1, pin2, pin1, pin2],
#                       [pin2, pin3, pin2, pin3, pin2, pin3],
#                       [pin1, pin2, pin1, pin2, pin1, pin2],
#                       [pin2, pin3, pin2, pin3, pin2, pin3],
#                       [pin1, pin3, pin1, pin3, pin1, pin2],
#                       [pin2, pin3, pin2, pin3, pin2, pin3]])
lattice.setUniverses([[pin1, pin2], [pin2, pin3]])
root_cell.setFill(lattice)


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
