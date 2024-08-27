def collect_none_values(self):
    obj = {key: value for key, value in self.items() if value is None}
    return obj
