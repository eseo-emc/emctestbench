'''
Created on 18 janv. 2011

@author: optland
'''


import xlwt

testBook = xlwt.Workbook()
testSheet = testBook.add_sheet('Testsheet')
testSheet.write(5,4,'Hoi')
testSheet.write(1,1,[1,2,3,4])
testBook.save('../../results/testBook.xls')