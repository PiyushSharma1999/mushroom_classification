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

    def is_null_present(self,data):
        """
            Method Name: is_null_present
            Description: This method checks whether there are null values present in the pandas Dataframe or not.
            Output: Return True if null values are present in the DataFrame, False if they are not present and 
                    returns the list of columns for which null values area present.
            On Failure: Rasie Exception
        """
        self.logger_object.log(self.file_object,'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values = []
        self.cols = data.columns
        try:
            self.null_counts = data.isna().sum() #check for the count of null values per column
            for i  in range(len(self.null_counts)):
                if self.null_counts[i]>0:
                    self.null_present=True
                    self.cols_with_missing_values.append(self.cols[i])
            if(self.null_present): # write logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing value count'] = np.asarray(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'Finding missing values is a success. Data written to the null values file. Exited the is_null_present method of the Preprocessor class.')
            return self.null_present,self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed . Exited the is_null_present method of the Preprocessor class.')
            raise Exception()

    def encodeECategoricalValues(self,data):
        """
            Method Name: encodeECategoricalValues
            Desription: This method encodes all the categorical values in the training set.
            Output" A DataFrame which all the categorical values encoded.
            On Failure: Rais Exception
        """
        data["class"] = data["class"].map({'p': 1,'e': 2})

        for column in data.drop(['class'],axis=1).columns:
            data = pd.get_dummies(data, columns=[column])
        return data