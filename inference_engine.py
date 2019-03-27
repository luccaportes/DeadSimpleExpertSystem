class Inference_Engine:
    def __init__(self, dict_rules, dict_stats):
        self.dict_rules = dict_rules
        self.dict_stats = dict_stats
        self.inital_stats = set(self.dict_stats["STATEMENTS"])
    
    def infer(self):
        while True:
            stat_size = len(self.dict_stats["STATEMENTS"])
            for _,r in sorted(self.dict_rules["RULES"].items()):
                if r["CONDS"].issubset(self.dict_stats["STATEMENTS"]):
                    self.dict_stats["STATEMENTS"] = self.dict_stats["STATEMENTS"].union(r["CONSEQS"])
            self.dict_stats["STATEMENTS"] = self.remove_positive(self.dict_stats["STATEMENTS"])
            if len(self.dict_stats["STATEMENTS"]) == stat_size:
                break

        resp = self.dict_stats["STATEMENTS"] - self.inital_stats
        resp = self.remove_negatives(resp)

        return resp

    def remove_positive(self, stats):
        new_stats = set(stats)
        for stat in stats:
            if stat[0] == "~":
                if stat.replace("~", "") in stats:
                    new_stats.remove(stat.replace("~", ""))
        return new_stats

    def remove_negatives(self, stats):
        new_stats = set(stats)
        for stat in stats:
            if stat[0] == "~":
                new_stats.remove(stat)
        return new_stats