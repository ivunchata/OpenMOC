import openmoc

###############################################################################
#                          Main Simulation Parameters
###############################################################################

options = openmoc.options.Options()

num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
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

circle = openmoc.Circle(x=0.0, y=0.0, radius=1.0, name='pin')
left = openmoc.XPlane(x=-3.0, name='left')
right = openmoc.XPlane(x=3.0, name='right')
top = openmoc.YPlane(y=3.0, name='top')
bottom = openmoc.YPlane(y=-3.0, name='bottom')

ileft = openmoc.XPlane(x=-2.0, name='left')     # inner surfaces
iright = openmoc.XPlane(x=2.0, name='right')
itop = openmoc.YPlane(y=2.0, name='top')
ibot = openmoc.YPlane(y=-2.0, name='bottom')


left.setBoundaryType(openmoc.PERIODIC)
right.setBoundaryType(openmoc.PERIODIC)
top.setBoundaryType(openmoc.PERIODIC)
bottom.setBoundaryType(openmoc.PERIODIC)


###############################################################################
#                             Creating Cells
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating cells...')

fuel = openmoc.Cell(name='fuel')
fuel.setFill(materials['UO2'])
fuel.addSurface(halfspace=-1, surface=circle)

moderator = openmoc.Cell(name='moderator')
moderator.setFill(materials['Water'])
moderator.addSurface(halfspace=+1, surface=circle)
moderator.addSurface(halfspace=+1, surface=ileft)
moderator.addSurface(halfspace=-1, surface=iright)
moderator.addSurface(halfspace=+1, surface=ibot)
moderator.addSurface(halfspace=-1, surface=itop)

cell11 = openmoc.Cell(name='top_left')
cell11.setFill(materials['Water'])
cell11.addSurface(halfspace=+1, surface=left)
cell11.addSurface(halfspace=-1, surface=ileft)
cell11.addSurface(halfspace=+1, surface=itop)
cell11.addSurface(halfspace=-1, surface=top)

cell12 = openmoc.Cell(name='top')
cell12.setFill(materials['Water'])
cell12.addSurface(halfspace=+1, surface=ileft)
cell12.addSurface(halfspace=-1, surface=iright)
cell12.addSurface(halfspace=+1, surface=itop)
cell12.addSurface(halfspace=-1, surface=top)

cell13 = openmoc.Cell(name='top_right')
cell13.setFill(materials['Water'])
cell13.addSurface(halfspace=+1, surface=iright)
cell13.addSurface(halfspace=-1, surface=right)
cell13.addSurface(halfspace=+1, surface=itop)
cell13.addSurface(halfspace=-1, surface=top)

cell21 = openmoc.Cell(name='left')
cell21.setFill(materials['Water'])
cell21.addSurface(halfspace=+1, surface=left)
cell21.addSurface(halfspace=-1, surface=ileft)
cell21.addSurface(halfspace=-1, surface=itop)
cell21.addSurface(halfspace=+1, surface=ibot)

cell23 = openmoc.Cell(name='right')
cell23.setFill(materials['Water'])
cell23.addSurface(halfspace=+1, surface=iright)
cell23.addSurface(halfspace=-1, surface=right)
cell23.addSurface(halfspace=-1, surface=itop)
cell23.addSurface(halfspace=+1, surface=ibot)

cell31 = openmoc.Cell(name='bot_left')
cell31.setFill(materials['Water'])
cell31.addSurface(halfspace=+1, surface=left)
cell31.addSurface(halfspace=-1, surface=ileft)
cell31.addSurface(halfspace=+1, surface=bottom)
cell31.addSurface(halfspace=-1, surface=ibot)

cell32 = openmoc.Cell(name='bot')
cell32.setFill(materials['Water'])
cell32.addSurface(halfspace=+1, surface=ileft)
cell32.addSurface(halfspace=-1, surface=iright)
cell32.addSurface(halfspace=+1, surface=bottom)
cell32.addSurface(halfspace=-1, surface=ibot)

cell33 = openmoc.Cell(name='bot_right')
cell33.setFill(materials['Water'])
cell33.addSurface(halfspace=+1, surface=iright)
cell33.addSurface(halfspace=-1, surface=right)
cell33.addSurface(halfspace=+1, surface=bottom)
cell33.addSurface(halfspace=-1, surface=ibot)


###############################################################################
#                            Creating Universes
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating universes...')

root_universe = openmoc.Universe(name='root universe')
root_universe.addCell(fuel)
root_universe.addCell(cell11)
root_universe.addCell(cell12)
root_universe.addCell(cell13)
root_universe.addCell(cell21)
root_universe.addCell(moderator)
root_universe.addCell(cell23)
root_universe.addCell(cell31)
root_universe.addCell(cell32)
root_universe.addCell(cell33)


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

openmoc.plotter.plot_tracks(track_generator)
openmoc.plotter.plot_segments(track_generator)
openmoc.plotter.plot_materials(geometry)
openmoc.plotter.plot_cells(geometry)
openmoc.plotter.plot_flat_source_regions(geometry)
openmoc.plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7])
openmoc.plotter.plot_energy_fluxes(solver, fsrs=range(geometry.getNumFSRs()))

openmoc.log.py_printf('TITLE', 'Finished')
