import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn_pandas import CategoricalImputer

class Preprocessing:
    """
        This class shall be used to clean and transform the data before training.
    """

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
    
    def remove_column(self,data,columns):
        """
            Method Name: remove_columns
            Description: This method removes the given columns from a pandas dataframe
            Output: A pandas DataFrame after removing the specified columns.
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try: 
            self.useful_data = self.data.drop(labels=self.columns,axis=1) # drop the labels specified in the columns
            self.logger_object.log(self.file_object,
                                    'Column removal Successful. Exited the remove_columns method ofthe Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_column method of the Preprocessor class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,
                                    'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class.')
            raise Exception()
    
    def separate_label_feature(self,data,label_column_name):
        """
            Method Name: separate_label_feature
            Description: This method separates  the features and a Label Columns.
            Output: Returns two separate DataFrames, one containing features and other containing Labels.
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(labels=label_column_name,axis=1) # drop columns specified and separate the feature columns
            self.Y = data[label_column_name] # Filter the Label columns
            self.logger_object.log(self.file_object,
                                    'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X , self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preproccessor class. Exception message: %s'+str(e))
            self.logger_object.log(self.file_object,'Label Separation Unsuccessful. Exited the separate_label_feature of the Preproccesor class')
            raise Exception()

    def dropUnnecessaryColumns(self,data,columnNameList):
        """
            Method Name: is_null_present
            Description: This method drops the unwanted columns.
        """
        data = data.drop(columnNameList,axis=1)
        return data
    
    def replaceInvalidValuesWithNull(self,data):
        """
            Method Name: replaceInvalidValuesWithNull
            Description: This method replaces invalid values i.e '?' with null.
        """
        for column in data.columns:
            count = data[column][data[column]=='?'].count()
            if count !=0:
                data[column] = data[column].replace('?',np.nan)
        return data