import openmoc

###############################################################################
#                          Main Simulation Parameters
###############################################################################

options = openmoc.options.Options()

num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing() / 2
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()*10
max_iters = options.getMaxIterations()

openmoc.log.set_log_level('NORMAL')


###############################################################################
#                            Creating Materials
###############################################################################

openmoc.log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = openmoc.materialize.materialize('../c5g7-materials.h5')


###############################################################################
#                            Creating Surfaces
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating surfaces...')

left = openmoc.XPlane(x=-2.0, name='left')
right = openmoc.XPlane(x=2.0, name='right')
bottom = openmoc.YPlane(y=-2.0, name='bottom')
top = openmoc.YPlane(y=2.0, name='top')
boundaries = [left, right, bottom, top]

large_circle = openmoc.Circle(x=0.0, y=0.0, radius=0.4, name='large pin')
medium_circle = openmoc.Circle(x=0.0, y=0.0, radius=0.3, name='medium pin')
small_circle = openmoc.Circle(x=0.0, y=0.0, radius=0.2, name='small pin')

for boundary in boundaries: boundary.setBoundaryType(openmoc.PERIODIC)


###############################################################################
#                             Creating Cells
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating cells...')

<<<<<<< HEAD
large_fuel = CellBasic(name='large pin fuel', rings=1, sectors=8)
large_fuel.setMaterial(materials['UO2'])
=======
large_fuel = openmoc.Cell(name='large pin fuel')
large_fuel.setNumRings(3)
large_fuel.setNumSectors(8)
large_fuel.setFill(materials['UO2'])
>>>>>>> upstream/develop
large_fuel.addSurface(halfspace=-1, surface=large_circle)

large_moderator = openmoc.Cell(name='large pin moderator')
large_fuel.setNumSectors(8)
large_moderator.setFill(materials['Water'])
large_moderator.addSurface(halfspace=+1, surface=large_circle)

<<<<<<< HEAD
medium_fuel = CellBasic(name='medium pin fuel', rings=3, sectors=5)
medium_fuel.setMaterial(materials['UO2'])
medium_fuel.addSurface(halfspace=-1, surface=medium_circle)

medium_moderator = CellBasic(name='medium pin moderator', sectors=3)
medium_moderator.setMaterial(materials['Water'])
=======
medium_fuel = openmoc.Cell(name='medium pin fuel')
medium_fuel.setNumRings(3)
medium_fuel.setNumSectors(8)
medium_fuel.setFill(materials['UO2'])
medium_fuel.addSurface(halfspace=-1, surface=medium_circle)

medium_moderator = openmoc.Cell(name='medium pin moderator')
medium_moderator.setNumSectors(8)
medium_moderator.setFill(materials['Water'])
>>>>>>> upstream/develop
medium_moderator.addSurface(halfspace=+1, surface=medium_circle)

small_fuel = openmoc.Cell(name='small pin fuel')
small_fuel.setNumRings(3)
small_fuel.setNumSectors(8)
small_fuel.setFill(materials['UO2'])
small_fuel.addSurface(halfspace=-1, surface=small_circle)

small_moderator = openmoc.Cell(name='small pin moderator')
small_moderator.setNumSectors(8)
small_moderator.setFill(materials['Water'])
small_moderator.addSurface(halfspace=+1, surface=small_circle)

root_cell = openmoc.Cell(name='root cell')
root_cell.addSurface(halfspace=+1, surface=boundaries[0])
root_cell.addSurface(halfspace=-1, surface=boundaries[1])
root_cell.addSurface(halfspace=+1, surface=boundaries[2])
root_cell.addSurface(halfspace=-1, surface=boundaries[3])


###############################################################################
#                            Creating Universes
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating universes...')

pin1 = openmoc.Universe(name='large pin cell')
pin2 = openmoc.Universe(name='medium pin cell')
pin3 = openmoc.Universe(name='small pin cell')
root_universe = openmoc.Universe(name='root universe')

pin1.addCell(large_fuel)
pin1.addCell(large_moderator)
pin2.addCell(medium_fuel)
pin2.addCell(medium_moderator)
pin3.addCell(small_fuel)
pin3.addCell(small_moderator)
root_universe.addCell(root_cell)


###############################################################################
#                            Creating Lattices
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating simple 4 x 4 lattice...')

<<<<<<< HEAD
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
=======
lattice = openmoc.Lattice(name='4x4 lattice')
lattice.setWidth(width_x=1.0, width_y=1.0)
lattice.setUniverses([[pin1, pin2, pin1, pin2],
                      [pin2, pin3, pin2, pin3],
                      [pin1, pin2, pin1, pin2],
                      [pin2, pin3, pin2, pin3]])
>>>>>>> upstream/develop
root_cell.setFill(lattice)


###############################################################################
#                         Creating the Geometry
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating geometry...')

geometry = openmoc.Geometry()
geometry.setRootUniverse(root_universe)
geometry.initializeFlatSourceRegions()


###############################################################################
#                          Creating the TrackGenerator
###############################################################################

openmoc.log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = openmoc.TrackGenerator(geometry, num_azim, track_spacing)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
#                            Running a Simulation
###############################################################################

solver = openmoc.CPUSolver(track_generator)
solver.setNumThreads(num_threads)
solver.setConvergenceThreshold(tolerance)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()


###############################################################################
#                             Generating Plots
###############################################################################

openmoc.log.py_printf('NORMAL', 'Plotting data...')

openmoc.plotter.plot_segments(track_generator)
openmoc.plotter.plot_materials(geometry, gridsize=500)
openmoc.plotter.plot_cells(geometry, gridsize=500)
openmoc.plotter.plot_flat_source_regions(geometry, gridsize=500, centroids=True)
openmoc.plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7])

openmoc.log.py_printf('TITLE', 'Finished')
