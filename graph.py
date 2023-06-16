#!/usr/bin/env python3

import sys
import networkx as nx
from PIL import Image
import extract

Image.MAX_IMAGE_PIXELS = 1000000000


def main():
    dump_sql_fn = sys.argv[1]
    DG = extract.gen_relation_graph_from_sql_dump(dump_sql_fn)
    nx.nx_agraph.to_agraph(DG).draw(prog='dot', path=f'output/all_dot.png')
    nx.nx_agraph.to_agraph(DG).draw(prog='fdp', path=f'output/all_fdp.png')


if __name__ == '__main__':
    main()
