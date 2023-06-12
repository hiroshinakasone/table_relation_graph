import re


class Table:
    def __init__(self, name):
        self.name = name
        self._parents = {}
        self._children = {}

    def add_parent(self, table):
        self._parents.setdefault(table.name, table)

    def add_child(self, table):
        self._children.setdefault(table.name, table)

    def parents(self):
        return [self._parents[k] for k in sorted(self._parents.keys())]

    def children(self):
        return [self._children[k] for k in sorted(self._children.keys())]

    def traverse_children(self, action):
        stack = [{"item": self, "depth": 0}]
        pass_count = {}
        while len(stack) > 0:
            node = stack.pop(-1)
            table = node["item"]
            depth = node["depth"]
            action(table, depth)
            pass_count.setdefault(table.name, 0)
            pass_count[table.name] += 1
            for child_table in table.children():
                pass_count.setdefault(child_table.name, 0)
                if pass_count[child_table.name] < 2:
                    stack.append({"item": child_table, "depth": depth + 1})


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
        child_table_name = extract_table_name(state)
        parent_table_names = extract_referred_table_names(state)

        child_table = all_tables.setdefault(
            child_table_name, Table(child_table_name))
        for paranet_table_name in parent_table_names:
            parent_table = all_tables.setdefault(
                paranet_table_name, Table(paranet_table_name))
            child_table.add_parent(parent_table)
            parent_table.add_child(child_table)

    return all_tables
