class Record:
    def __init__(self, record):
        _fields = []
        for key, val in record.items():
            setattr(self, key, val)
            _fields.append(key)


def safe_eval(expr, globals_dict=None):
    if not globals_dict:
        globals_dict = {}
    else:
        globals_dict = dict(globals_dict)
    globals_dict['__builtins__'] = {}
    return eval(expr, globals_dict)
