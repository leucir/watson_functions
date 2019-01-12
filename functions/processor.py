PACKAGE_URL = 'git+https://github.com/leucir/watson_functions.git@'

from iotfunctions.preprocessor import BaseTransformer

class MyCustomFunction(BaseTransformer):
  '''
  Mutiply value by 3.14
  '''

  def __init__(self, input_item, output_item):
    self.input_item = input_item
    self.output_item = output_item
    super().__init__()

  def execute(self, df):
    df_new = df.copy()
    df_new[self.output_item] = df[self.input_item]*3.41
    return df_new
