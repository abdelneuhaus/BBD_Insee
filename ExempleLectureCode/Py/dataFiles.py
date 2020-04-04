"""
Script for the Python Workshop - Part 11 : Write/Read data files
Dec 2017
Just un-comment the part you want to execute
"""

##########################

import pandas as pd
# To install pandas: conda install pandas
import pylab as plt

# Excel file
myFile = 'mice.xlsx'

# Excel spreadsheet
sp = pd.ExcelFile(myFile)

# Print the sheet names
print(sp.sheet_names)

# Load a sheet into a DataFrame named myData
myData = sp.parse('Feuil1')

print(myData.head())

print(myData["Mouse1"])


##########################

# import pandas as pd
# import pylab as plt

# # Excel file
# myFile = 'mice.xlsx'

# # Excel spreadsheet
# sp = pd.ExcelFile(myFile)

# # Load a sheet into a DataFrame named myData
# myData = sp.parse('Feuil1')

# for mouse in myData.keys():
# 	# print(mouse, ":", myData[mouse])
# 	print(mouse)
# 	if (mouse != "Weights"):
# 		plt.plot(range(len(myData[mouse])), myData[mouse], label=mouse)

# plt.legend(title="Mice IDs", loc="lower right")
# plt.title("Evolution of the weights")
# plt.xlabel("Days")
# plt.ylabel("Weights (g)")
# plt.ylim(0, 25)
# plt.show()