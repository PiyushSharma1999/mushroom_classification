from datetime import datetime
from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTypeValidation_Insertion_training.DataTypeValidation import dBOperation
from DataTransformation_Training.DataTransformation import dataTransform
from application_logging.logger import App_logger

class train_validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt",'a+')
        self.log_writer  = App_logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for Training!!')
            # extracting values from prediction schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            # getting the regex defined to validated filename
            regex = self.raw_data.manualRegexCreation()
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)
            # validating column length in the file
            self.raw_data.validateColumnLength()
            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object,'Raw Data Validation Complete!!')

            self.log_writer.log(self.file_object,'Starting Data Transformation!!')
            # below function adds quotes to the '?' values in some columns
            self.dataTransform.addQuotesToStringValuesInColumn()

            self.log_writer.log(self.file_object,"DataTransformation Completed!!")

            self.log_writer.log(self.file_object,
                                "Creating Training_Database and tables on the basis of given schema!!")
            # create database with given name, if present open the connection! Create table with columns given in the schema file
            self.dBOperation.createTableDb('Training',column_names)
            self.log_writer.log(self.file_object,"Table creation Completed!!")
            self.log_writer.log(self.file_object,"Deleting Good data Folder!!")
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object,"Good_Data folder deleted!!")
            self.log_writer.log(self.file_object,"Moving bad files to Archive and deleting Bad_Data folder!!")
            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object,"Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object,"Validating Operation completed!!")
            self.log_writer.log(self.file_object,"Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.file_object.close()

        except Exception as e:
            raise e


