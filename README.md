# myDomino
An easier way to run Domino - first version with basic functions

This is the beginning of a program that will greatly enhance research projects that use the theriak-domino software suite (a command-line (Fortran), Thermodynamic G-minimization program for geoscientists).  myDomino will include an interface (WUI/GUI) with options for easily calculating chemical systems (input for theriak), improved misfit functions for more precise optimization of domino models, and tools for producing quantitative and graphical output, for example with post-script editing capabilities.

This program is currently providing basic input file generation for common calculations that are iterated until an acceptable chemical system is achieved (typically includes batches of 10-14 files generated over 10-30 iterations).  For example, these input files are used in the MP13 program (see other repo), which will be coded in python and merged with myDomino in the future.
