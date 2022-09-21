from datetime import datetime
from os import listdir
import pandas as pd
from application_logging.logger import App_logger

class dataTransformPredict:
    """
        This class shall be used for transforming the Good Raw Training Data before loading it in Database!!
    """
    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_logger()

    def addQuotesToStringValuesInColumn(self):
        """
            Method Name: addQuotesToStringValuesInColumn
            Description: This method replaces the missing values in columns with "NULL" to
                         store in the table. We are using substring in the first column to
                         keep only "Integer" data for ease up the loading.
                         This column is anyways going to be removed during prediction.
            Output:  None
            On Failure: Raise Exception      
        """
        try:
            log_file = open("Prediction_Logs/dataTransformationLog.txt",'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                data = pd.read_csv(self.goodDataPath+"/"+file)
                data['stalk-root'] = data['stalk-root'].replace('?',"'?'")
                data.to_csv(self.goodDataPath+"/"+file,index=None,header=True)
                self.logger.log(log_file," %s: Quotes added successfully!!"%file)
        
        except Exception as e:
            log_file = open("Prediction_Logs/dataTransformLog.txt",'a+')
            self.logger.log(log_file,"Data Transformation failed because:: %s"%e)
            log_file.close()
            raise e
        log_file.close()