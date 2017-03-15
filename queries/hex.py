def parse_hex_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            row = row.split(':')
            res.append(row[1]) 

    f.close()
    return res


hex_values = parse_hex_list('../query_results/colors.txt')
