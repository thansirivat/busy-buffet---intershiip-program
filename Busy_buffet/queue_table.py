import pandas as pd
import numpy as np

file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'
sheets = {'fri': '133', 'sat': '143', 'sun': '153', 'tues': '173', 'wed': '183'}

# รวมทุก sheet
dfs = []
for day, sheet_name in sheets.items():
    df = pd.read_excel(file, sheet_name=sheet_name)
    df['day'] = day
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# แปลงคอลัมน์เวลาเป็น datetime
combined_df['queue_start'] = pd.to_datetime(combined_df['queue_start'], format='%H:%M:%S', errors='coerce')
combined_df['queue_end'] = pd.to_datetime(combined_df['queue_end'], format='%H:%M:%S', errors='coerce')


def meal_duration_avg(df, guest_type=None):
    """
    คืนค่า average waiting duration (นาที)
    ถ้า guest_type มีค่า จะกรองเฉพาะ In-house หรือ Walk-in
    """
    if guest_type:
        df = df[df['Guest_type'] == guest_type]
    
    # คำนวณ duration เป็นนาที
    duration = (df['queue_end'] - df['queue_start']).dt.total_seconds() / 60
    
    return duration.mean()


# คำนวณค่าเฉลี่ย
walk_in_duration_avg = meal_duration_avg(combined_df, 'Walk in')
in_house_duration_avg = meal_duration_avg(combined_df, 'In house')

print("Average Walk-in duration (min):", walk_in_duration_avg)
print("Average In-house duration (min):", in_house_duration_avg)