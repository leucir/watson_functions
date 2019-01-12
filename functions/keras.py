from iotfunctions.preprocessor import BaseTransformer
from iotfunctions.ui import UIFunctionOutSingle, UISingle
from keras.models import load_model
import numpy as np

PACKAGE_URL = 'git+https://github.com/leucir/watson_functions.git@'


class ForecastKerasModel(BaseTransformer):
    '''
    Predict a Keras model from inside the pipeline
    '''

    def __init__(self, features, output_item='prediction'):
        self.output_name = output_item
        super().__init__()

        self.features = features

        self.inputs = ['features']
        self.outputs = ['output_item']


    def execute(self, df):
        df_final = df.copy()

        #Load function from file system for now
        model = load_model('../models/base_model_LSTM64_LSTM32_Dropout0.375240min_new')

        #randomize inputs
        #Shape of (1,n,m) is defined to make sure the results are in one dimenstion
        x = np.random.rand(1, 180, 59)

        predict_results = model.predict(x, verbose=1)

        df_final[self.output_name] = predict_results[0][1]

        '''
        if (predict_results is not None):
            count = 1
            for row in predict_results[0]:
                outputname = self.output_name + '_' + str(count)
                df_final[outputname] = row
                count +=1
        '''

        return df_final

    def _getMetadata(self, df=None, new_df=None, inputs=None, outputs=None, constants=None):
        '''
        Preload function has no dataframe in or out so standard _getMetadata() does not work
        '''
        # define arguments that behave as function inputs
        inputs = {}
        inputs['features'] = UISingle(name='features', datatype=str,
                                                description='Dummy feature as input').to_metadata()

        # define arguments that behave as function outputs
        outputs = {}
        outputs['output_item'] = UIFunctionOutSingle(name='prediction', datatype=str,
                                                     description='Returns a prediction value').to_metadata()

        return (inputs, outputs)