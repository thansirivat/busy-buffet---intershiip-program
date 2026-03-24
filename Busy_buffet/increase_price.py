import numpy as np
import pandas as pd

# เตรียมข้อมูล
file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'

sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}

# รวมข้อมูลทุก sheet
dfs = []
for day, sheet in sheets.items():
    df = pd.read_excel(file, sheet_name=sheet)
    df['day'] = day
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# กรอง Walk-in
walk_in_pax_normalday = combined_df[
    (combined_df['Guest_type'] == 'Walk in') &
    (combined_df['pax'] > 0) &
    (combined_df['day'].isin(['tues', 'wed','fri']))
]
# รวมจำนวนคน
total_pax_normalday = walk_in_pax_normalday['pax'].sum()

#--------------------------------------------------------------

#หา รายได้ ในราคาเดิม
walk_in_pax_weekend = combined_df[
    (combined_df['Guest_type'] == 'Walk in') &
    (combined_df['pax'] > 0) &
    (combined_df['day'].isin(['sun', 'sat']))
]
# รวมจำนวนคน
total_pax_weekend = walk_in_pax_weekend['pax'].sum()
total_pax = total_pax_normalday + total_pax_weekend

normal_day_revenue = total_pax_normalday * 159
week_end_revenue = total_pax_weekend * 199

total_same_price = normal_day_revenue + week_end_revenue

print(total_same_price)

#-------------------------------------------------------------------------------
# increase_price.py

def customer_lost_calculation(total_pax, percent):
    total_lost = total_pax * (100 * percent) // 100
    revenue = total_lost * 259
    return revenue


def generate_data(total_pax):
    percent_list = list(range(10, 71, 1))
    revenue_list = [
        customer_lost_calculation(total_pax, p)
        for p in percent_list
    ]
    return percent_list, revenue_list

import matplotlib.pyplot as plt

def customer_lost_calculation(percent):
    total_lost = total_pax * (100 - percent) // 100
    revenue = total_lost * 259
    return revenue

# เตรียมข้อมูล
percent_list = list(range(10, 71, 1))
revenue_list = [customer_lost_calculation(p) for p in percent_list]

# สร้างกราฟ
plt.figure()
plt.plot(percent_list, revenue_list)

# 🔥 เพิ่มเส้นแนวนอน (รายได้เดิม)
plt.axhline(y=total_same_price)

# ตั้งชื่อแกน
plt.xlabel("Customer Loss (%)")
plt.ylabel("Revenue")
plt.title("Revenue vs Customer Loss (%)")

plt.show()