import json

def remove_positive(stats):
	new_stats = set(stats)
	for stat in stats:
		if stat[0] == "~":
			if stat.replace("~", "") in stats:
				new_stats.remove(stat.replace("~", ""))
	return new_stats

def remove_negatives(stats):
	new_stats = set(stats)
	for stat in stats:
		if stat[0] == "~":
			new_stats.remove(stat)
	return new_stats

with open("ex.json") as parse_file:
	contents = parse_file.read().upper()

start_rules = contents.find("@RULES") + 6
end_rules = contents.find("@STATEMENTS")

dic_temp = json.loads(contents[start_rules:end_rules])
dic_rules = dict(dic_temp)
for k, v in dic_temp["RULES"].items():
	dic_rules["RULES"][k]["CONDS"] = set(dic_rules["RULES"][k]["CONDS"])
	dic_rules["RULES"][k]["CONSEQ"] = set(dic_rules["RULES"][k]["CONSEQ"])

dic_stat = json.loads(contents[end_rules + 11:])

dic_stat["STATEMENTS"] = set(dic_stat["STATEMENTS"])
stat_backup = set(dic_stat["STATEMENTS"])

while True:
	stat_size = len(dic_stat["STATEMENTS"])
	for _,r in sorted(dic_rules["RULES"].items()):
		if r["CONDS"].issubset(dic_stat["STATEMENTS"]):
			dic_stat["STATEMENTS"] = dic_stat["STATEMENTS"].union(r["CONSEQ"])
	dic_stat["STATEMENTS"] = remove_positive(dic_stat["STATEMENTS"])

	if len(dic_stat["STATEMENTS"]) == stat_size:
		break

resp = dic_stat["STATEMENTS"] - stat_backup

resp = remove_negatives(resp)

print(resp)