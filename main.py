import sys
from parser import Parser
from inference_engine import Inference_Engine

path = sys.argv[1]

parser = Parser(path)
parser.parse()

dict_rules = parser.get_dict_rules()
dict_stats = parser.get_dict_stat()

infer = Inference_Engine(dict_rules, dict_stats)

resp = infer.infer()

print(resp)