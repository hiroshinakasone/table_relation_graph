import re
import networkx as nx


def extract_create_table_state(sql):
    return re.findall('CREATE TABLE [^;]+;', sql)


def extract_table_name(create_table_state):
    m = re.match('CREATE TABLE `(.+)` .+', create_table_state)
    return m.groups()[0].strip()


def extract_referred_table_names(create_table_state):
    return map(lambda x: x.strip(), re.findall('.+ REFERENCES `(.+)` .+', create_table_state))


def extract_tables_and_relations(stmts):
    nodes = []
    edges = []
    for stmt in stmts:
        table_name = extract_table_name(stmt)
        nodes.append(table_name.strip())

        referred_table_names = extract_referred_table_names(stmt)
        for rtn in referred_table_names:
            edges.append((table_name.strip(), rtn.strip()))

    return nodes, edges


def gen_relation_graph_from_sql_dump(fn):
    with open(fn) as f:
        sql = f.read()

    create_table_stmts = extract_create_table_state(sql)
    tables, relations = extract_tables_and_relations(create_table_stmts)

    DG = nx.DiGraph()
    DG.add_nodes_from(tables)
    DG.add_edges_from(relations)

    return DG
