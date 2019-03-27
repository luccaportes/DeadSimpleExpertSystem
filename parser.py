import json

class Parser:
	def __init__(self, path):
		self.path = path
		self.content = None
		self.start_rules, self.end_rules = None, None
		self.dict_rules = None
		self.dict_stat = None

	def parse(self):
		self.content = self.load_file()
		self.start_rules, self.end_rules = self.determine_bounds()
		self.dict_rules = self.parse_rules()
		self.dict_stat = self.parse_statements()

	def get_dict_rules(self):
		return self.dict_rules
	
	def get_dict_stat(self):
		return self.dict_stat
	
	def load_file(self):
		with open(self.path) as parse_file:
			content = parse_file.read().upper()
		return content

	def determine_bounds(self):
		start_rules = self.content.find("@RULES") + 6
		if start_rules == -1:
			raise Exception("No '@RULES' declarated.")
		end_rules = self.content.find("@STATEMENTS")
		if end_rules == -1:
			raise Exception("No '@STATEMENTS' declarated.")
		return start_rules, end_rules
	
	def parse_rules(self):
		dic_temp = json.loads(self.content[self.start_rules:self.end_rules])
		if "RULES" not in dic_temp:
			raise Exception("No 'RULES' key declarated in the RULES JSON.")
		dic_rules = dict(dic_temp)
		for k, v in dic_temp["RULES"].items():
			if "CONDS" not in dic_rules["RULES"][k]:
				raise Exception("No 'CONDS' key declarated in the RULE " + k + ".")
			if "CONSEQS" not in dic_rules["RULES"][k]:
				raise Exception("No 'CONSEQS' key declarated in the RULE " + k + ".")
			dic_rules["RULES"][k]["CONDS"] = set(dic_rules["RULES"][k]["CONDS"])
			dic_rules["RULES"][k]["CONSEQS"] = set(dic_rules["RULES"][k]["CONSEQS"])
		return dic_rules

	def parse_statements(self):
		dic_stat = json.loads(self.content[self.end_rules + 11:])
		dic_stat["STATEMENTS"] = set(dic_stat["STATEMENTS"])
		return dic_stat
