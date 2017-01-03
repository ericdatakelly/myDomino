#!C:\Python34
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
#import subprocess

class storage:
    """ Read and write files that contain default and previously used values.
    The values are used to populate the window as well. """

    def readCalcOptions(inputFile):
        inputFile = open(inputFile,'r')
        newDict = {}
        for line in inputFile:
            line = line.strip('\n')
            keyVal = line.split(':')
            newDict[keyVal[0]] = keyVal[1].split(',')
        inputFile.close()
        return newDict

    def readBulkComp(inputFile):
        inputFile = open(inputFile,'r')
        newDict = {}
        for line in inputFile:
            line = line.strip('\n')
            keyVal = line.split(':')
            newDict[keyVal[0]] = keyVal[1]
        inputFile.close()
        return newDict

    def writeBulkComp(bcDict):
        text = (     'SI:' + str(bcDict['SI']) + '\nAL:' + str(bcDict['AL'])
            + '\nFE:' + str(bcDict['FE']) + '\nMG:' + str(bcDict['MG'])
            + '\nMN:' + str(bcDict['MN']) + '\nCA:' + str(bcDict['CA'])
            + '\nNA:' + str(bcDict['NA']) + '\nK:'  + str(bcDict['K'])
            + '\nTI:' + str(bcDict['TI']) + '\nH:'  + str(bcDict['H'])
            + '\nO:'  + str(bcDict['O']))
        outputFile = open('bulkCompDict.txt','w')
        outputFile.write(text)
        outputFile.close()

    def writeCalcOptions(calcOptionsDict):
        outputFile = open('calcOptionsDict.txt','w')
        for k,v in sorted(calcOptionsDict.items()):
            text = (str(k) + ':' + str(v) + '\n')
            outputFile.write(text)
        outputFile.close()

    def bcDict2Text(bcDict):
        return (   'SI\t'  + str(bcDict['SI']) + '\nAL\t' + str(bcDict['AL'])
                + '\nFE\t' + str(bcDict['FE']) + '\nMG\t' + str(bcDict['MG'])
                + '\nMN\t' + str(bcDict['MN']) + '\nCA\t' + str(bcDict['CA'])
                + '\nNA\t' + str(bcDict['NA']) + '\nK\t'  + str(bcDict['K'])
                + '\nTI\t' + str(bcDict['TI']) + '\nH\t'  + str(bcDict['H'])
                + '\nO\t'  + str(bcDict['O']))

    def calcOpDict2Text(calcOPDict):
        # Better:
        # Use a grid instead of an open text editor?
        text = ''
        sep = '\t'
        for k,v in sorted(calcOPDict.items()):
            #text = text + ('{0:20} '.format(str(k)) + sep.join(v) + '\n')
            text = text + str(k) + '\t\t' + sep.join(v) + '\n'
        return (text)



class domjob:
    """Run domino using a series of commands stored in a batch file."""
    
    def writeScript(name,datasetName,bulkComp,bulkCompName,rangeOfX,rangeOfY,
                    typeOfCalc):

        # Open a file for writing
        outputFile = open('script_' + name + '.txt','w')

        # Write the lines of the file
        outputFile.write('script.script_' + name + '.txt\n')    # "script." is a required keyword for Theriak
        outputFile.write('script_' + name + '.plt\n')           # Graphics output name
        outputFile.write(datasetName + '\n')                    # Name of database
        outputFile.write('    1.0000    300    0.010000   ' +
                         '0.1000000E-08   0.1000000E-08   ' +
                         '0.1000000E+01 0.1000000E-03     ' +
                         '25      25     500\n')                # Calculation parameters for theriak
                                                                # (get the names from the guide and call them advanced options)
        outputFile.write(bulkComp + bulkCompName + '\n')        # Chemical information (bulk composition)
        outputFile.write('\n\n\n\n\n')                          # These lines are commonly empty
        outputFile.write(rangeOfX + '\n')                       # Parameters for abscissa
        outputFile.write(rangeOfY + '\n')                       # Parameters for ordinate
        outputFile.write(typeOfCalc + '\n')                     # Calculation type and associated parameters
        outputFile.write('1\n')                                 # Label option (Assemblages, reactions, etc.)
        outputFile.write(' 0.0000000E+00   0.0000000E+00\n')    # T and P, if constant
        outputFile.write('_script_' + name + '_pix\\\n')        # Folder name for pixel map (if pixel map is calculation type)

        # Close the file
        outputFile.close()

    def formatRangeOfX(minX,maxX,unitsX,unitsY):
        return str(unitsX) + '  ' + str(minX) + '  ' + str(maxX)

    def formatRangeOfY(minY,maxY,unitsX,unitsY):
        return str(unitsY) + '  ' + str(minY) + '  ' + str(maxY)

    def formatBulkCompForTD(bcDict): 
    # The order of the elements matters for the Moynihan and Pattison (2013) Matlab script.
        return ('1   '
                + 'SI('  + str(bcDict['SI']) + ')AL(' + str(bcDict['AL'])
                + ')FE(' + str(bcDict['FE']) + ')MG(' + str(bcDict['MG'])
                + ')MN(' + str(bcDict['MN']) + ')CA(' + str(bcDict['CA'])
                + ')NA(' + str(bcDict['NA']) + ')K('  + str(bcDict['K'])
                + ')TI(' + str(bcDict['TI']) + ')H('  + str(bcDict['H'])
                + ')O('  + str(bcDict['O'])  + ')  *  ')

    def formatTypeOfCalc(scriptName):
        newString = ''
        for item in scriptName:
            newString = newString + '  ' + str(item)
        return newString[2:] # Remove the first two spaces
    

    #def writeBatch # This would write the batch file called "domjob.bat"
        
    #def runTD  # This would start TD and run the domjob.bat file

    #def noLabels # This would replot the results without labels ("clean" plots)

# class domino:

# class theriak:

# class therbin:

# Make a dialog window to edit the calculation options
class dialogCalcOptions(Gtk.Dialog):

    def __init__(self,parent):
        #Gtk.Window.__init__(self,title='MyTD') # This doesn't work.  Using Glade to set title instead.
        self.builder = Gtk.Builder()
        self.builder.add_from_file('MyTD_calcOptions2.glade')
         
        # Define handlers for signals from window
        handlersCalcOpDict = {
            'on_windowCalcOp_destroy':self.on_windowCalcOp_destroy,
            'on_buttonApplyCalcOp_clicked':self.on_buttonApplyCalcOp_clicked,
            'on_buttonCancelCalcOp_clicked':self.on_buttonCancelCalcOp_clicked
            }


        # Get the objects with signals from the window
        self.dialog = self.builder.get_object('windowCalcOp')
        self.buttonApplyCalcOp = self.builder.get_object('buttonApplyCalcOp')
        self.buttonCancelCalcOp = self.builder.get_object('buttonCancelCalcOp')

        
        # Connect the signals with their handlers
        self.builder.connect_signals(handlersCalcOpDict)


        # Look for previous or default values
        calcOpText = storage.readCalcOptions('calcOptionsDict.txt')


        # Load the values into the textview oject
        calcOpObject = self.builder.get_object('textbufferCalcOp')
        calcOpTextString = storage.calcOpDict2Text(calcOpText)
        calcOpObject.set_text(calcOpTextString)



        # ***** The text needs formatting before putting it in the window******
        # Edit the function, calcOpDict2Text, so that it replaces the tuples(?)
        # with space delimited values.  Replace the colon with a tab.













        
    def on_windowCalcOp_destroy(self,widget):
        return(Gtk.ResponseType.CANCEL)

    def on_buttonCancelCalcOp_clicked(self,widget):
        #del(self)
        #self.destroy()
        return(Gtk.ResponseType.CANCEL)

    def on_buttonApplyCalcOp_clicked(self,widget):
        # # Get the textview object
        # textviewCalcOpObj = self.builder.get_object('textviewCalcOp')
                
        # # Get the text from the object
        # calcOpStart = textviewCalcOpObj.get_start_iter()
        # calcOpEnd = textviewCalcOpObj.get_end_iter()
        # calcOpText = textviewCalcOpObj.get_text(calcOpStart,calcOpEnd,True)

        print('Apply clicked')
        return(Gtk.ResponseType.OK)
        #print(dir(self))

        # ****** After the text is formatted for the window, continue with this section******

        # # format calcOpText and construct a list using multiple delimiters
        # bulkCompText = bulkCompText.upper()
        # bulkCompText = bulkCompText.replace('FE2+','FE').replace('FE2','FE')
        # bulkCompText = bulkCompText.replace('FE3+','F3').replace('FE3','F3 ')
        # bulkCompList = bulkCompText.replace(',',' ').replace('(',' ').replace(')',' ').split()

        # # If the list starts with a value instead of an element, reverse the order of each
        # # pair while building the dictionary.
        # try:
        #     val = float(bulkCompList[0])
        # except ValueError:
        #     bulkCompDict = dict([(k, v) for k,v in 
        #         zip (bulkCompList[::2],bulkCompList[1::2])])
        # else:
        #     bulkCompDict = dict([(k, v) for k,v in 
        #         zip (bulkCompList[1::2],bulkCompList[::2])])

        # # Check for missing elements
        # if 'H' not in bulkCompDict:
        #     bulkCompDict['H'] = '100'
        #     print("\n'H 100' added to bulk comp\n")
        # if 'O' not in bulkCompDict:
        #     bulkCompDict['O'] = '?'
        #     print("\n'O ?' added to bulk comp\n")






        # Put text into dictionary
        

        # Write the dictionary to a file
        # storage.writeCalcOptions(dictionary)

        
# which of these is correct?
#        self.window.destroy()
#        calcOptionsWindow_quit()

# Make a window to control the program (basic for now, but expanding...)
class MyTDWindow(Gtk.Window):

    def __init__(self):
        #Gtk.Window.__init__(self,title='MyTD') # This doesn't work.  Using Glade to set title instead.
        self.builder = Gtk.Builder()
        self.builder.add_from_file('MyTD.glade')
         
        # Define handlers for signals from window
        handlersDict = {
            'on_applicationTDWindow_destroy':Gtk.main_quit,
            'on_comboProgram_changed':self.on_comboProgram_changed,
            'on_buttonEditProgOp_clicked':self.on_buttonEditProgOp_clicked,
            'on_buttonEditDatasetOp_clicked':self.on_buttonEditDatasetOp_clicked,
            'on_buttonEditCalcOp_clicked':self.on_buttonEditCalcOp_clicked,
            'on_buttonRun_clicked':self.on_buttonRun_clicked,
            'on_buttonClose_clicked':self.on_buttonClose_clicked
            }


        # Get the objects with singals from the window
        self.window = self.builder.get_object('applicationTDWindow')
        self.comboProgram = self.builder.get_object('comboProgram')
        self.buttonEditProgOp = self.builder.get_object('buttonEditProgOp')
        self.buttonEditDatasetOp = self.builder.get_object('buttonEditDatasetOp')
        self.entryBulkCompName = self.builder.get_object('entryBulkCompName')
        self.buttonEditCalcOp = self.builder.get_object('buttonEditCalcOp')
        self.buttonRun2 = self.builder.get_object('buttonRun2')
        self.buttonClose = self.builder.get_object('buttonClose')

        
        # Connect the signals with their handlers
        self.builder.connect_signals(handlersDict)


        # Look for previous or default values
        bulkCompText = storage.readBulkComp('bulkCompDict.txt')


        # Load the values into the ojects of the window
        bulkCompObj = self.builder.get_object('textBufferBulkComp')
        bulkCompTextString = storage.bcDict2Text(bulkCompText)
        bulkCompObj.set_text(bulkCompTextString)
 

    # Add a menu item of program preferences
        # Move "show log window" to the program preferences
        # Add an option to choose previous or default values to load at start

    def on_comboProgram_changed(self,widget):
        print('Not implemented yet')
        # X and Y labels to should change according to the program chosen.

    def on_buttonEditProgOp_clicked(self,widget):
        print('Not implemented yet')
        # Get the program name
        # Open a window of options specific to the program chosen
        # The program options will be written to the script files (but I'm not
        # sure what those options are yet)
    
    def on_buttonEditDatasetOp_clicked(self,widget):
        print('Not implemented yet')
        # Get the dataset name
        # Open a window for choosing phases and activity models

    def on_buttonEditCalcOp_clicked(self,widget):
        # Open a dialog window to enter the calculation options
        dialog = dialogCalcOptions(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The Apply button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

        #win2 = calcOptionsWindow()
 
    # def on_buttonCancelCalcOp_clicked(self,widget):
    #     win2.destroy()

    def on_buttonRun_clicked(self,widget):
        # Get the objects with text from the window
        comboProgramObj = self.builder.get_object('comboProgram')
        comboMinXObj = self.builder.get_object('comboMinX')
        comboMaxXObj = self.builder.get_object('comboMaxX')
        comboMinYObj = self.builder.get_object('comboMinY')
        comboMaxYObj = self.builder.get_object('comboMaxY')
        datasetNameObj = self.builder.get_object('comboDataset')
        entryBulkCompNameObj = self.builder.get_object('entryBulkCompName')
        bulkCompObj = self.builder.get_object('textBufferBulkComp')
        
        # Get the text from the objects
        programName = comboProgramObj.get_active_text()
        minX = comboMinXObj.get_active_text()
        maxX = comboMaxXObj.get_active_text()
        minY = comboMinYObj.get_active_text()
        maxY = comboMaxYObj.get_active_text()
        datasetName = datasetNameObj.get_active_text()
        bulkCompName = entryBulkCompNameObj.get_text()
        bulkCompStart = bulkCompObj.get_start_iter()
        bulkCompEnd = bulkCompObj.get_end_iter()
        bulkCompText = bulkCompObj.get_text(bulkCompStart,bulkCompEnd,True)

        # format bulkCompText and construct a list using multiple delimiters
        bulkCompText = bulkCompText.upper()
        bulkCompText = bulkCompText.replace('FE2+','FE').replace('FE2','FE')
        bulkCompText = bulkCompText.replace('FE3+','F3').replace('FE3','F3 ')
        bulkCompList = bulkCompText.replace(',',' ').replace('(',' ').replace(')',' ').split()

        # If the list starts with a value instead of an element, reverse the order of each
        # pair while building the dictionary.
        try:
            val = float(bulkCompList[0])
        except ValueError:
            bulkCompDict = dict([(k, v) for k,v in 
                zip (bulkCompList[::2],bulkCompList[1::2])])
        else:
            bulkCompDict = dict([(k, v) for k,v in 
                zip (bulkCompList[1::2],bulkCompList[::2])])

        # Check for missing elements
        if 'H' not in bulkCompDict:
            bulkCompDict['H'] = '100'
            print("\n'H 100' added to bulk comp\n")
        if 'O' not in bulkCompDict:
            bulkCompDict['O'] = '?'
            print("\n'O ?' added to bulk comp\n")

        # Load the value into the oject of the window ---> this should be a function instead
        bulkCompObj = self.builder.get_object('textBufferBulkComp')
        bulkCompTextString = storage.bcDict2Text(bulkCompDict)
        bulkCompObj.set_text(bulkCompTextString)
        
        # Store some values in files
        storage.writeBulkComp(bulkCompDict)

        # Not implemented yet
        unitsX = 'TC'
        unitsY = 'P'

        # Read some values from files
        calcOptionsDict = storage.readCalcOptions('calcOptionsDict.txt')

        # Format some strings
        rangeOfX = domjob.formatRangeOfX(minX,maxX,unitsX,unitsY)
        rangeOfY = domjob.formatRangeOfY(minY,maxY,unitsX,unitsY)
        bulkComp = domjob.formatBulkCompForTD(bulkCompDict)


        # Cycle through each script name and write a script file
        for k in calcOptionsDict: # Each key (k) is a script name and 
                                  # each value (tuple) contains the calculation paramters
            typeOfCalc = domjob.formatTypeOfCalc(calcOptionsDict[k])
            domjob.writeScript(k,datasetName,bulkComp,bulkCompName,
                rangeOfX,rangeOfY,typeOfCalc)

        print('Finished writing script files')

    def on_buttonClose_clicked(self,widget):
        print('MyTD Closed')
        Gtk.main_quit()

# Add a class that reads and writes text files
# One method would read the previous calculation options
# or load default options (or just tell the user to choose some)

def main():
    win = MyTDWindow()
    Gtk.main()

if __name__ == '__main__':
    main()
    
