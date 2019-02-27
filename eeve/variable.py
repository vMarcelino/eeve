class Variable:
    def __init__(self, name: str, value):
        self.value = value
        self._name = name

    @property
    def name(self):
        return self._name


class VariableGroup:
    def __init__(self):
        self.vars = dict()

    def __getitem__(self, key):
        return self.vars[key].value

    def __setitem__(self, key, value):
        if type(value) is Variable:
            self.vars[key] = value
        else:
            self.vars[key] = Variable(name=key, value=value)

    def update(self, new: dict):
        for k, v in new.items():
            self.__setitem__(key=k, value=v)

    def get(self, var, default=None):
        if var.startswith('var'):
            var = var[3:]
        while var.startswith('$'):
            var = var[1:]

        if var in self.vars:
            return self[var]
        else:
            return default

    def get_var(self, var):
        if var not in self.vars:
            self.vars[var] = Variable(name=var, value=None)

        return self.vars[var]

    def to_kwargs(self) -> dict:
        result = dict()
        for k, v in self.vars.items():
            result[k] = v.value
        return result