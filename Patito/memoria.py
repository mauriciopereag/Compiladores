MEM = {
    'global': {'entero': 1000, 'flotante': 2000},
    'local':  {'entero': 3000, 'flotante': 4000},
    'temp':   {'entero': 5000, 'flotante': 6000},
    'cte':    {'entero': 7000, 'flotante': 8000},
}

cte_table  = {}
addr_count = {k: dict(v) for k, v in MEM.items()}

def next_addr(segment, tipo):
    addr = addr_count[segment][tipo]
    addr_count[segment][tipo] += 1
    return addr

def get_cte_addr(value, tipo):
    if value not in cte_table:
        cte_table[value] = next_addr('cte', tipo)
    return cte_table[value]

def reset_addresses():
    global cte_table, addr_count
    cte_table  = {}
    addr_count = {k: dict(v) for k, v in MEM.items()}