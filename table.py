import re


class Table:
    def __init__(self, name):
        self.name = name
        self._referrers = {}

    def referenced_from(self, table):
        self._referrers.setdefault(table.name, table)

    def referrers(self):
        return [self._referrers[k] for k in sorted(self._referrers.keys())]

    def traverse(self, action):
        stack = [{"item": self, "depth": 0}]
        pass_count = {}
        while len(stack) > 0:
            node = stack.pop(-1)
            table = node["item"]
            depth = node["depth"]
            action(table, depth)
            pass_count.setdefault(table.name, 0)
            pass_count[table.name] += 1
            for referrer_table in table.referrers():
                pass_count.setdefault(referrer_table.name, 0)
                if pass_count[referrer_table.name] < 2:
                    stack.append({"item": referrer_table, "depth": depth + 1})


def extract_create_table_state(sql):
    return re.findall('CREATE TABLE [^;]+;', sql)


def extract_table_name(create_table_state):
    m = re.match('CREATE TABLE `(.+)` .+', create_table_state)
    return m.groups()[0].strip()


def extract_referred_table_names(create_table_state):
    return map(lambda x: x.strip(), re.findall('.+ REFERENCES `(.+)` .+', create_table_state))


def gen_all_tables(create_table_states):
    all_tables = {}
    for state in create_table_states:
        referrer_table_name = extract_table_name(state)
        referred_table_names = extract_referred_table_names(state)

        referrer_table = all_tables.setdefault(
            referrer_table_name, Table(referrer_table_name))
        for referred_table_name in referred_table_names:
            referred_table = all_tables.setdefault(
                referred_table_name, Table(referred_table_name))
            referred_table.referenced_from(referrer_table)
    return all_tables
