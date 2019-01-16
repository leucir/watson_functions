import json
import os
from sqlalchemy import Column, Float
from functions.keras import ForecastKerasModel

from iotfunctions.preprocessor import EntityDataGenerator
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database

# replace with a credentials dictionary or provide a credentials file
with open('credentials.json', encoding='utf-8') as F:
    credentials = json.loads(F.read())

'''
Developing Test Pipelines
-------------------------

When creating a set of functions you can test how they these functions will
work together by creating a test pipeline. You can also connect the test
pipeline to real entity data so that you can what the actual results that the
function will deliver.

'''

'''
A database object is our connection to the mother ship
'''
db = Database(credentials=credentials)
db_schema = None  # set if you are not using the default

'''
To do anything with IoT Platform Analytics, you will need one or more entity type. 
You can create entity types through the IoT Platform or using the python API.
Here is a basic entity type that has three data items: company_code, temperature and pressure
'''
entity_name = 'keras_model'
db_schema = None  # replace if you are not using the default schema
db.drop_table(entity_name, schema=db_schema)
entity = EntityType(entity_name, db,
                    Column('speed', Float()),
                    Column('temp', Float()),
                    Column('pressure', Float()),
                    **{
                        '_timestamp': 'evt_timestamp',
                        '_db_schema': db_schema
                    })
'''
When creating an EntityType object you will need to specify the name of the entity, the database
object that will contain entity data

After creating an EntityType you will need to register it so that it visible in the UI.
'''
entity.register()


'''
Entities can get pretty lonely without data. You can feed your entity data by
writing directly to the entity table or you can cheat and generate data.

'''
entity.generate_data(days=0.5, drop_existing=True)
df = db.read_table(table_name=entity_name, schema=db_schema)
df.head()



'''
To retrieve the model when the predictions function will execute, 
we are storing the model in a object storage bucket.
In a production environment, the model will be trained and stored on object storage using a different approach.
This sample is considering a model already trained and serialized.
'''
#model file is loaded in memory
rel_path = 'models/base_model_LSTM64_LSTM32_Dropout0.375240min_new' #relative path for the model
script_dir = os.path.dirname(__file__) #absolute dir the script is in
abs_file_path = os.path.join(script_dir, rel_path)
model_file = open(abs_file_path, 'rb')


#create bucket on COS to store the model
bucket_name = credentials['tennant_id'] + '-analytics-' + 'models'
db.cos_create_bucket(bucket=bucket_name)


#store model on COS
db.cos_save(persisted_object=model_file.read(),
            filename='base_model_LSTM64_LSTM32_Dropout0.375240min_new',
            bucket=bucket_name,
            binary=True)


'''
We now have 12 hours of historical data. We can use it to do some calculations.
The calculations will be placed into a container called a pipeline. The 
pipeline is constructed from multiple stages. Each stage performs a transforms
the data. 


The execute() method retrieves entity data and carries out the transformations.
By specifying 'to_csv = True', we also csv output dumped at the end of 
each stage. This is useful for testing. 
'register=true' took care of function registration so the ForecastKerasModel 
function will be available in the ui.
You can use the outputs of one calculation in another. This function is receiving a dummy value as input,
and will generate four predictions as outputs. The output definitions are declared in the function class.
'''
k_fn = ForecastKerasModel(dummy=['dummy'])


'''
The 12 hours of historical data we loaded  won't keep these widgets
happy for very long. IoT Platform Analytics performs calculations on new data
received, so if we add a stage to the pipeline that generates new data each time
the pipeline runs, we can keep our widgets well fed with new data.
'''
g_fn = EntityDataGenerator(dummy_items=['temp'])


'''
When this pipeline executed, it added more data to the widgets input table
and then completed the tranform and filter stages.

To register all of the functions tested, use register = True
'''
df = entity.exec_pipeline(g_fn, k_fn, register=True)
df.head(1).transpose()

