# myDomino
An easier way to run Domino - first version with basic functions

This is the beginning of a program that will greatly enhance research projects that use the theriak-domino software suite (a command-line (Fortran), Thermodynamic G-minimization program for geoscientists).  myDomino will include an interface (WUI/GUI) with options for easily calculating chemical systems (input for theriak), improved misfit functions for more precise optimization of domino models, and tools for producing quantitative and graphical output, for example with post-script editing capabilities.

This program is currently providing basic input file generation for common calculations that are iterated until an acceptable chemical system is achieved (typically includes batches of 10-14 files generated over 10-30 iterations).  For example, these input files are used in the MP13 program (see other repo), which will be coded in python and merged with myDomino in the future.


The EBC calculator will process chemical data to generate chemical bulk compositions for the systems modeled in myDomino.  The algorithm is currently a complex spreadsheet, so conversion to python is all that is needed.


### Example of Main GUI (for setting up the model or batches of models)

* Easy input of chemical system (aka bulk composition) by drag and drop, copy and paste, direct edit, etc. and automatic recognition of element vs oxide, etc.
* Searchable database for solution model selection with automatic model adjustments according to solution models.
* Easily choose calculation options with ability to save and document choices (associated with project/sample).  It will include suggested calculation options and other help/tutorial features.
* Easily setup batch runs to model several systems overnight or over days/weeks depending on model complexity and computation speeds.

<img src="https://github.com/ericdavidkelly/myDomino/blob/myDomino_GUI/Examples/gui_example4b.png"/>


### Examples of Analysis Output

* Ability to output typical plots and quantitative measures of model fit, custom choices of plot axes, or statistical values.
* Graphical tools for examining phase diagrams (layered vector graphics labeled for reactions and phase assemblages).  Layers can be viewed as transparent or simply hidden (like Illustrator).

<img src="https://github.com/ericdavidkelly/myDomino/blob/myDomino_analysis/Examples/EBC_example.png" width="400"/>

<img src="https://github.com/ericdavidkelly/myDomino/blob/myDomino_analysis/Examples/Vol_example.png" width="400"/>


### Examples of Graphical Analysis

* Graphical tools for examining phase diagrams (layered vector graphics labeled for reactions and phase assemblages).  Layers can be viewed as transparent or simply hidden (like Illustrator).  The upper image is a stack of typical raw layers.  The program will provide easy cleanup of raw files to generate graphical results like in the lower image.

<img src="https://github.com/ericdavidkelly/myDomino/blob/myDomino_analysis/Examples/IPD_raw_example.png" width="700"/>

<img src="https://github.com/ericdavidkelly/myDomino/blob/myDomino_analysis/Examples/IPD_example.png" width="525"/>

