#!/usr/bin/env python3

import sys
import networkx as nx
from PIL import Image
import table

Image.MAX_IMAGE_PIXELS = 1000000000


def add_path(DG, t):
    DG.add_node(t.name)
    for r in t.children():
        nx.add_path(DG, [r.name, t.name])


def main():
    dump_sql_fn = sys.argv[1]
    with open(dump_sql_fn) as f:
        sql = f.read()

    create_table_states = table.extract_create_table_state(sql)
    all_tables = table.gen_all_tables(create_table_states)

    for t in all_tables.values():
        if len(t.parents()) > 0:
            continue
        DG = nx.DiGraph()
        t.traverse_children(lambda e, d: add_path(DG, e))
        nx.nx_agraph.to_agraph(DG).draw(prog='fdp', path=f'output/{t.name}.png')


if __name__ == '__main__':
    main()
