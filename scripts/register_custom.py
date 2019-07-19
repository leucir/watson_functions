import json
from iotfunctions.db import Database

with open('credentials.json', encoding='utf-8') as F:
    credentials = json.loads(F.read())

db_schema = None

db = Database(credentials=credentials)

from functions.bad_functions import XXXXX
db.register_functions([XXXXX])