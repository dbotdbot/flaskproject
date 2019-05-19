
from flask_table import Table, Col
 
class Results(Table):
    id = Col('Id', show=False)
    timeStamp = Col('Time Stamp')
    weight = Col('weight')
    foodtype = Col('foodtype')