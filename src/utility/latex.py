pdfLatexBinaryPath = 'C:\\Program Files\\MiKTeX 2.9\\miktex\\bin\\x64\\pdflatex.exe'


import debugging
import os
import shutil
import subprocess

class LatexDocument(object):
    def __init__(self,directory,packages=['pxfonts','units','graphicx']):
        self.packages = packages
        self.preamble = ''
        self.body = ''
        self.directory = directory
        self.figuresDirectory = os.path.join(self.directory,'figures')        
        
        try:
            shutil.rmtree(self.directory)
        except:
            pass
        os.mkdir(self.directory)
        os.mkdir(self.figuresDirectory)

    def appendBody(self,text):
        self.body += text
    def appendTitle(self,title,author=None):
        if not author:
            self.body += '\\begin{center} { \\huge \\bfseries ' + self.texEscape(title) + ' }\\end{center}\n\n'
        else:
            self.body += '\\title{'+title+'}\n\\author{'+author+'}\n\\maketitle\n\n'
    
    def appendGraph(self,graph,name,caption,arguments='width=0.8\\textwidth'):
        figureFileName = name.replace(' ','_')
        graph.savefig(os.path.join(self.figuresDirectory,figureFileName+'.pdf'))
            
#        self.appendBody('\\includegraphics['+arguments+']{figures/'+figureFileName+'}\\\\\n')
        self.appendBody('''
\\begin{figure}[h!!]
    \\centering        
    \\includegraphics['''+arguments+''']{figures/'''+figureFileName+'''}\\\\
    \\caption{'''+self.texEscape(caption)+'''}\\label{fig:'''+figureFileName+'''}
\\end{figure}
''')

    
    def writeOut(self,fileName='report.tex'):
        latexFilePath = os.path.join(self.directory,'report.tex')
        with open(latexFilePath,'w') as latexFile:
            latexFile.write(str(self))

        typesetter = subprocess.Popen([pdfLatexBinaryPath,latexFilePath,'-output-directory='+self.directory])
        typesetter.wait()
    
    def __str__(self):
        documentString = '''\\documentclass{article}\n\n'''
        for packageName in self.packages:
            documentString += '\usepackage{'+packageName+'}\n'
        documentString += '\n'
        documentString += '\\begin{document}\n\n'+self.body+'\n\\end{document}'
        
        return documentString

    def texQuantity(self,value,unit='dB',emphasis=False):
        if emphasis:
            return '$\\mathbf{\\unit['+str(value)+']{\\textbf{'+unit+'}}}$'
        else:
            return '$\\unit['+value+']{'+unit+'}$'
            
    def texEscape(self,rawText):
        return rawText.replace('\\','\\textbackslash ').replace('_','\_ ').replace('~','\\textasciitilde ').replace('<','$<$').replace('>','$>$')           
            
    def appendTabular(self,listOfTuples=[],alignment='rl'):
        self.body += '\\begin{tabular}{'+alignment+'}\n'
        for row in listOfTuples:
            self.body += '\t' + ' & '.join(row) + '\\\\\n'
                
        self.body += '\\end{tabular}\n'

#
#\begin{tabular}{rl}
#	Test start & 24 september 2013 14:50:44 \\
#	Test end & \\
#	Operator & Sjoerd Op 't Land 	
#\end{tabular}
#
#
#
#\end{document}

if __name__ == '__main__':
    reportDirectory = os.path.join(debugging.currentDirectory(),'report')    

    testReport = LatexDocument(reportDirectory)  
    
    testReport.appendTitle('LL4490 Integration Test Report','EmcTestbench')
    testReport.appendBody('This is the automatically generated report of the LL4490 integration test.\n')
    testReport.appendTabular([('Date','Today'),('Operator','Sjoerd'),('Power',testReport.texQuantity(-3,'dB',emphasis=True))],alignment='rl')
    testReport.writeOut()
    