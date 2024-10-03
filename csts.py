import numpy as np

colors_name = {
    0 : 'joker',
    1 : 'rouge' ,
    2 : 'jaune' ,
    3 : 'bleu' ,
    4 : 'noir' ,
    None : 'None'
}

colors_code = {
    'joker' : '\033[35m',
    'rouge' : '\033[91m',
    'jaune' : '\033[93m',
    'bleu'  : '\033[94m',
    'noir'  : '\033[30m',

    'reset' : '\033[0m',
    'None'  : ''
}