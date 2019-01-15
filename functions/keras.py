from iotfunctions.preprocessor import BaseTransformer
from iotfunctions.ui import UIFunctionOutSingle, UISingle
from keras.models import load_model
from collections import OrderedDict
import numpy as np
import logging
import tempfile

logger = logging.getLogger(__name__)

PACKAGE_URL = 'git+https://github.com/leucir/watson_functions.git@'


class ForecastKerasModel(BaseTransformer):
    '''
    Predict a Keras model from inside the pipeline
    '''

    def __init__(self, dummy, predict1='predict1', predict2='predict2', predict3='predict3', predict4='predict4'):
        super().__init__()
        self.predict1 = predict1
        self.predict2 = predict2
        self.predict3 = predict3
        self.predict4 = predict4

        self.dummy = dummy

    def execute(self, df):
        df_final = df.copy()

        #main object to get access to DB, Messaging and infrastructure components
        db = self.get_entity_type().db

        #set model file name and bucket name
        #both should match the names defined when the model was created and stored
        file_name = 'base_model_LSTM64_LSTM32_Dropout0.375240min_new'
        bucket_name = db.tenant_id + '-' + 'models'

        #load model from COS
        model_cos_file = db.cos_load(filename=file_name, bucket=bucket_name, binary=True)

        #store in a tempfile in order to be loaded by Keras
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(model_cos_file)
            #Load function from file system for now
            model = load_model(temp.name)

        #randomize inputs
        #Shape of (1,n,m) is defined to make sure the results are in one dimenstion
        x = np.random.rand(1, 180, 59)

        #run prediction
        predict_results = model.predict(x, verbose=1)

        #add the prediction results to the data frame
        df_final[self.predict1] = predict_results[0][0]
        df_final[self.predict2] = predict_results[0][1]
        df_final[self.predict3] = predict_results[0][2]
        df_final[self.predict4] = predict_results[0][3]

        return df_final

    def _getMetadata(self, df=None, new_df=None, inputs=None, outputs=None, constants=None):
        '''
        Preload function has no dataframe in or out so standard _getMetadata() does not work
        '''
        # define arguments that behave as function inputs
        inputs = {}
        inputs['dummy'] = UISingle(name='dummy', datatype=str,
                                                description='Dummy attribute as input').to_metadata()

        # define arguments that behave as function outputs
        outputs = OrderedDict()

        outputs['predict1'] = UIFunctionOutSingle(name='predict1', datatype=str,
                                                     description='Returns a prediction value').to_metadata()

        outputs['predict2'] = UIFunctionOutSingle(name='predict2', datatype=str,
                                                     description='Returns a prediction value').to_metadata()

        outputs['predict3'] = UIFunctionOutSingle(name='predict3', datatype=str,
                                                     description='Returns a prediction value').to_metadata()

        outputs['predict4'] = UIFunctionOutSingle(name='predict4', datatype=str,
                                                     description='Returns a prediction value').to_metadata()

        return (inputs, outputs)