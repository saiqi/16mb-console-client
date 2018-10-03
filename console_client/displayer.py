from terminaltables import AsciiTable
import yaml


def format_value(value):
    value_str = str(value).replace('\n', ' ')
    if len(value_str) > 50:
        return value_str[:50] + ' ...'
    return value_str


def extract_keys(data):
    keys = list()
    for r in data:
        if not isinstance(r, dict):
            return None
        for k in r.keys():
            if k not in keys:
                keys.append(k)
    return keys


def display(data):
    printed_data = list()
    if isinstance(data, list):
        keys = extract_keys(data)
        if keys:
            printed_data.append(keys)
            for r in data:
                row = list()
                for k in keys:
                    if k in r:
                        row.append(format_value(r[k]))
                    else:
                        row.append('N/A')
                printed_data.append(row)
            table = AsciiTable(printed_data)
            print(table.table)
        else:
            print(yaml.dump(data, default_flow_style=False))
    elif isinstance(data, dict):
        print(yaml.dump(data, default_flow_style=False))
    else:
        print(data)
