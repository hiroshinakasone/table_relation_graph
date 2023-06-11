#!/usr/bin/env python3

import sys

import table


def main():
    dump_sql_fn = sys.argv[1]
    with open(dump_sql_fn) as f:
        sql = f.read()

    create_table_states = table.extract_create_table_state(sql)
    all_tables = table.gen_all_tables(create_table_states)
    for t in all_tables.values():
        t.traverse(lambda t, d: print("{}:{}{}".format(d, "\t"*d, t.name)))


if __name__ == '__main__':
    main()
