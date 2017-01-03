# pyEBC

# Note: MC method uses samples from probability ranges, not uniform ranges. 
# The input must define the deviate range


# Read input (modes and compositions of phases, deviates, criteria for match)
# Compositions are constants
# Modes are to be varied and deviates are ranges of the modes following Gaussian distribution
# Qz should have full range from 0 to 100



# Enter modes and comps here, do the bc calc, generate the new bc, and run theriak



# Sample the input within the deviates to create new modes (this is the MC section)
# There is probably a library for MC that I can call here.





# Calculate the bulk composition (make independent function following my spreadsheet - use
# my more efficient chemical evolution algorithm to calculate the bc.
# Steps
# 1: convert oxides to ...


# Call theriak and check phase stability at various P-T points.  Do a quick check to see if the
# basic criteria are met (garnet stable above P-T range and Bt stable above P-T range, etc.)
# Maybe include an option to skip this step and just generate many Domino plots overnight or
# over a few days.

# If basic criteria are not met, go back and resample the modes to generate a new bulk
# composition.
# Include a max iterations value to avoid an infinite loop

# Else if basic criteria are met, call Domino and make a diagram within the specified P-T range.

# Display the diagram (python must have a ps plotting library)

# Alternatively (later), have pyEBC read the plt file from the Domino run and refine the bulk
# comp again.  It appears that the assemblages in the plt file are defined (like dominos!) with
# P-T on either side of mismatched phase assemblages.  I can read those assemblages and build
# a matrix of the stable phases and their P-T ranges.  This can be compared with misfit criteria
# and the program can decide whether or not to try again.
# Careful: some P-T points are label locations (notice PHNG is spaced farther than ru when plotted)
# So what would this misfti criteria be?  What do I look for?  Grt-in, Bt-in, Chl-out, St-in, etc.
# Maybe just check isopleth convergence instead of general phase locations?
# If it saves the bc and diagram for each run, I can just let it keep going and periodically 
# check in to see if a diagram looks right.
