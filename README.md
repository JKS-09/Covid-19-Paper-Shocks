## COVID19 Paper__ RA_Position Assignment
### This program requires Visual Studio Code (VSCode) to run. The main code for WebScraping has been written in Python (the app and not Jupyter Notebook). To run this code in Jupyter Notebook, please convert the file and the input and output locations to your desired location.

This code requires certain libraries to be installed before it can be run. These can be found in the requirements.txt file. Without these libraries and packages, the program will not run effectively. Certain libraries are also mentioned in the main.py file. Furthermore, the webscraping has been done in four steps. Kindly adhere to the order to ensure that the program runs smoothly. The final file obtained has been shared separately. 

Step 1: Execute the main.py file and make sure that the dates run, and restart the process in case the website crashes. Please note, due to website crashes/lags, the date may need to be changed in the main.py file to ensure that the downloading process runs smoothly. The speed of this downloading process will vary as per internet speed and/or website traffic. Please allow for sufficient time for this download to happen. 

Step 2: Convert the downloaded files to xlsx format through html_to_excel.ipynb 

Step 3: excel_cleaner.ipynb is to be used to clean all the data and add the respective dates for each state as per its daily prices, to allow for easier combination

Step 4: excel_combiner.ipynb is the final step which will compile the excel sheets that have been downloaded according to our needs and will be sorted by date. There will be 24 columns and 2237 rows for the 86 days worth of data.

