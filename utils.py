import config
import json
import pickle
import numpy as np


class MedicalInsurance():
    def __init__(self, user_data):
        self.model_file_path =  "RidgeCV_model.pkl"
        self.user_data= user_data
    
    def load_saved_data(self):
        # loading the model
        with open(self.model_file_path  ,"rb") as f:
            self.model = pickle.load(f)
          
            
        # loading the project data file
        with open("project_data.json","r") as f:
            self.project_data = json.load(f)
            
    
    def get_predicted_price(self):
        #print("This is Get Price")
        self.load_saved_data()
        age = self.user_data["age"]
        gender  = self.user_data['gender']
    
        bmi = self.user_data['bmi']
        children= self.user_data['children']
        discount_eligibility= self.user_data['discount_eligibility']
        region  = self.user_data['region']

        ## converting region, gender & discount_eligibility to numerical values
        gender_enc = self.project_data['gender'][gender]
        discount_eligibility_enc = self.project_data['discount_eligibility'][discount_eligibility]

        region = "region_"+ region
        region_index = np.where(np.array(self.project_data['Columns']) == region)[0][0]
        #print('region_index :',region_index)
        
        ## Creating a test array

        col_count = len(self.project_data['Columns'])
        test_array = np.zeros(col_count)
        test_array[0] = eval(self.user_data['age'])
        test_array[1] = gender_enc
        test_array[2] = eval(self.user_data['bmi'])
        test_array[3] = eval(self.user_data['children'])
        test_array[4] = discount_eligibility_enc
        test_array[region_index] = 1
        #print(test_array)
       

        predicted_charges = np.around(self.model.predict([test_array])[0],3)
        print('predicted_charges :',predicted_charges)
        return predicted_charges

 
if __name__ =="__main__":
    ins = MedicalInsurance()
    ins
    
