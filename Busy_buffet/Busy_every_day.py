import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#เตรียมข้อมูล
file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'

sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}

dfs = []
for day, sheet in sheets.items():
    df = pd.read_excel(file, sheet_name=sheet)
    df['day'] = day  # เพิ่มคอลัมน์วัน
    dfs.append(df)

# รวมทุกวันเป็น DataFrame เดียว
combined_df = pd.concat(dfs, ignore_index=True)

# นับจำนวนลูกค้าต่อวัน (ใช้ service_no. เป็นตัวนับ)
count_per_day = combined_df.groupby('day')['service_no.'].count()

# วาด Bar Chart
fig, ax = plt.subplots(figsize=(8,5))
count_per_day.plot(kind='bar', color='#4CAF50', ax=ax)

ax.set_xlabel('Day')
ax.set_ylabel('Number of Customers')
ax.set_title('Number of Customers per Day')
plt.xticks(rotation=0)
plt.tight_layout()

# แสดงใน Streamlit
st.pyplot(fig)