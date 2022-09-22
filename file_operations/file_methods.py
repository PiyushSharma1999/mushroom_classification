import pickle 
import os
import shutil

class File_Operations:
    """
        This class shall be used to save the model after training
        and load the saved model for prediction.
    """
    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self,model,filename):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Ouput: File gets saved
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_directory,filename) # createss separate directory for each cluster
            if os.path.isdir(path): # remove previously existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path+'/'+filename+'.sav','wb') as f:
                pickle.dump(model,f) # save the model to file
            self.logger_object.log(self.file_object,'Model File '+filename+' saved. Exitedd the save_model method of the File_Operation class')
            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in save_model method of  the File_Operations class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Model File '+filename+' could not be saved. Exited the save_model method of the File_Operations class.')
            raise Exception()
    
    def load_model(self,filename):
        """
            Method Name: load_model
            Description: load the model file to memory
            Output: The model file loaded in memory
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename+'/'+filename+'.sav','rb') as f:
                self.logger_object.log(self.file_object,'Model file '+filename+' loaded. Exited the load_model method of the. Exited the load_model method of the File_Operation class.')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in load_model method of the File_Operation class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Mode File '+filename+' could not be saved. Exited the load_model method of the File_Operations class')
            raise Exception()
    
    def find_correct_model(self,cluster_name):
        """
            Method Name: find_correct_model
            Description: Select the correct model based on cluster number
            Output: The Model file
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,'Entered the find_correct_model_file method of the File_Operation class.')
        try:
            self.cluster_number = cluster_name
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file  in self.list_of_files:
                try:
                    if (self.file.index(str(self.cluster_number))!=1):
                        self.model_name = self.file
                except:
                    continue
        
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in find_correct_model_file method of the File_Operation class.')
            self.logger_object.log(self.file_object,'Exited the find_correc_model_file method of the File_Operation class with Failure')
            raise Exception()
            