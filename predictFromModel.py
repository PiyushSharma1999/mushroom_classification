import pandas 
from file_operations import file_methods
from data_preprocessing import preprocessing
from data_ingestion import data_loader_prediction
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation

class prediction:

    def __init__(self,path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt",'a+')
        self.log_writer = logger.App_logger()
        self.pred_data_val = Prediction_Data_validation(path)
    
    def predictionFromModel(self):

        try:
            self.pred_data_val.deletedPredictionFile() # deletes the existing prediction file from last run
            self.log_writer.log(self.file_object,'Start of Prediction')
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object,self.log_writer)
            data = data_getter.get_data()

            preprocessor = preprocessing.Preprocessing(self.file_object,self.log_writer)
            data = preprocessor.dropUnnecessaryColumns(data,['veiltype'])

            # replacing '?' values ith np.nan 
            data = preprocessor.replaceInvalidValuesWithNull(data)

            is_null_present, cols_with_missing_values=preprocessor.is_null_present(data)
            if(is_null_present):
                data = preprocessor.impute_missing_values(data,cols_with_missing_values)

            # get encode values from categorical data
            data = preprocessor.encodeCategoricalValuesPrediction(data)

            file_loader = file_methods.File_Operations(self.file_object,self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(data)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            result = [] # initializing blank list for storing predictions

            for i in clusters:
                cluster_data = data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                for val in (model.predict(cluster_data)):
                    result.append(val)
            
            result = pandas.DataFrame(result,columns=['Predictions'])
            path = "Prediction_Output_File/Predictions.csv"
            result.to_csv("Prediction_Output_File/Predictions.csv",header=True) # append result to prediction file
            self.log_writer.log(self.file_object,'End of Prediction')
        except Exception as e:
            self.log_writer.log(self.file_object,'Error occured while running the prediction!! Error:: %s'%e)
            raise e
        return path
                