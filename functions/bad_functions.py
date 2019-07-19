import inspect
import logging
import datetime as dt
import math
from sqlalchemy.sql.sqltypes import TIMESTAMP,VARCHAR
import numpy as np
import pandas as pd

from iotfunctions.base import BaseTransformer
from iotfunctions import ui

logger = logging.getLogger(__name__)


# Specify the URL to your package here.
# This URL must be accessible via pip install

PACKAGE_URL = 'git+https://github.com/leucir/watson_functions.git'


class XXXXX (BaseTransformer):

   def __init__(self, input_item, output_item='output_item'):
       self.input_item = input_item
       self.output_item = output_item
       super().__init__()

   def execute(self,df):
       df = df.copy()
       df[self.output_item] = df[self.input_item] - 1
       return df

   @classmethod
   def build_ui(cls):
       # define arguments that behave as function inputs
       inputs = []
       inputs.append(ui.UISingleItem(
           name='input_item',
           datatype=float,
           description='Data item to calculate average of same hour of previous day'
       ))
       # define arguments that behave as function outputs
       outputs = []
       outputs.append(ui.UIFunctionOutSingle(
           name='output_item',
           datatype=float,
           description='PrevDayHourlyAvgDiff'
       ))
       return inputs, outputs
