import pandas as pd

# -----------------------------
# 1. Load Excel
# -----------------------------
df = pd.read_excel('customers_mock_up.xlsx')

# clean column
df.columns = df.columns.str.strip()
print("Columns:", df.columns)

# -----------------------------
# 2. Clean data
# -----------------------------
df['type'] = df['type'].astype(str).str.strip()

df['arrival'] = pd.to_numeric(df['arrival'], errors='coerce')
df['dining'] = pd.to_numeric(df['dining'], errors='coerce')

df = df.dropna(subset=['arrival', 'dining', 'type'])

df['arrival'] = df['arrival'].astype(int)
df['dining'] = df['dining'].astype(int)

# -----------------------------
# 3. Convert to list
# -----------------------------
customers = df.to_dict(orient='records')
customers = sorted(customers, key=lambda x: x['arrival'])

# -----------------------------
# 4. FIFO Simulation (29 tables)
# -----------------------------
tables = [0] * 6

fifo_wait = []
fifo_type = []

for c in customers:
    next_table_time = min(tables)
    table_index = tables.index(next_table_time)
    
    start = max(next_table_time, c['arrival'])
    wait = start - c['arrival']
    
    fifo_wait.append(wait)
    fifo_type.append(c['type'])
    
    tables[table_index] = start + c['dining']

# -----------------------------
# 5. Alternating Simulation (29 tables)
# -----------------------------
inhouse_q = [c for c in customers if c['type'] == 'In house']
walkin_q = [c for c in customers if c['type'] == 'Walk in']

tables = [0] * 6
turn = 0

alt_wait = []
alt_type = []

while inhouse_q or walkin_q:

    if turn % 2 == 0 and inhouse_q:
        c = inhouse_q.pop(0)
    elif turn % 2 == 1 and walkin_q:
        c = walkin_q.pop(0)
    else:
        if inhouse_q:
            c = inhouse_q.pop(0)
        elif walkin_q:
            c = walkin_q.pop(0)
        else:
            break

    next_table_time = min(tables)
    table_index = tables.index(next_table_time)
    
    start = max(next_table_time, c['arrival'])
    wait = start - c['arrival']
    
    alt_wait.append(wait)
    alt_type.append(c['type'])
    
    tables[table_index] = start + c['dining']
    turn += 1

# -----------------------------
# 6. Helper
# -----------------------------
def avg_by_type(wait_list, type_list, target):
    vals = [w for w, t in zip(wait_list, type_list) if t == target]
    return sum(vals)/len(vals) if vals else 0

# -----------------------------
# 7. Summary
# -----------------------------
total_customers = len(customers)
total_inhouse = sum(1 for c in customers if c['type'] == 'In house')
total_walkin = sum(1 for c in customers if c['type'] == 'Walk in')

print("\n=== Customer Summary ===")
print("Total customers:", total_customers)
print("In house:", total_inhouse)
print("Walk in:", total_walkin)

# -----------------------------
# 8. Results
# -----------------------------
print("\n=== FIFO (29 tables) ===")
print("In house:", avg_by_type(fifo_wait, fifo_type, 'In house'))
print("Walk in:", avg_by_type(fifo_wait, fifo_type, 'Walk in'))

print("\n=== Alternating (29 tables) ===")
print("In house:", avg_by_type(alt_wait, alt_type, 'In house'))
print("Walk in:", avg_by_type(alt_wait, alt_type, 'Walk in'))

# -----------------------------
# 9. Extra metrics (pro level)
# -----------------------------
print("\n=== Overall Avg Wait ===")
print("FIFO:", sum(fifo_wait)/len(fifo_wait))
print("ALT:", sum(alt_wait)/len(alt_wait))

print("\n=== Max Wait ===")
print("FIFO:", max(fifo_wait))
print("ALT:", max(alt_wait))

# -----------------------------
# แปลงผลลัพธ์เป็น DataFrame
# -----------------------------
data = {
    'Guest Type': ['In house', 'Walk in'],
    'FIFO': [
        avg_by_type(fifo_wait, fifo_type, 'In house'),
        avg_by_type(fifo_wait, fifo_type, 'Walk in')
    ],
    'Alternating': [
        avg_by_type(alt_wait, alt_type, 'In house'),
        avg_by_type(alt_wait, alt_type, 'Walk in')
    ]
}

df_plot = pd.DataFrame(data)


# -----------------------------
# เตรียมข้อมูล
# -----------------------------

def avg_by_type(wait_list, type_list, target):
    vals = [w for w, t in zip(wait_list, type_list) if t == target]
    return sum(vals)/len(vals) if vals else 0
guest_types = ['In house', 'Walk in']

fifo_values = [
    avg_by_type(fifo_wait, fifo_type, 'In house'),
    avg_by_type(fifo_wait, fifo_type, 'Walk in')
]

alt_values = [
    avg_by_type(alt_wait, alt_type, 'In house'),
    avg_by_type(alt_wait, alt_type, 'Walk in')
]