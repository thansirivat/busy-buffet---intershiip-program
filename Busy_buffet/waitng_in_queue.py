import pandas as pd

file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'
sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}
#รวมทุก sheet
dfs = []
for day, sheet_name in sheets.items():
    df = pd.read_excel(file, sheet_name=sheet_name)
    
    # เพิ่ม column บอกวัน (สำคัญมาก)
    df['day'] = day
    
    dfs.append(df)
# รวมทั้งหมด
combined_df = pd.concat(dfs, ignore_index=True)

print(combined_df.head())
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

# หาว่าคนไม่ทนรอและออกจากคิวไปกี่คน
walk_away_In_house = combined_df[
    (combined_df['Guest_type'] == 'In house') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].isna())
]

#หาลูกค้าที่ Inhouse อยู่ใน Queue
In_queue_In_house = combined_df[
    (combined_df['Guest_type'] == 'In house') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].notna())
]

print("In queue:", len(In_queue_In_house))
print("Walk away:", len(walk_away_In_house))

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#walk in รอนานจนออกคิว เท่าไหร่

walk_away_walk_in = combined_df[
    (combined_df['Guest_type'] == 'Walk in') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].isna())
]

#หาลูกค้าที่ walkin อยู่ใน Queue
In_queue_walk_in = combined_df[
    (combined_df['Guest_type'] == 'Walk in') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].notna())
]

print("In queue:", len(In_queue_walk_in))
print("Walk away:", len(walk_away_walk_in))

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

walk_away_duration_In_house = combined_df[
    (combined_df['Guest_type'] == 'In house') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].notna())
]

walk_away_duration_walk_in = combined_df[
    (combined_df['Guest_type'] == 'Walk in') &
    (combined_df['queue_start'].notna()) &
    (combined_df['table_no.'].notna())
]



def load_combine_duration(df):
    """
    คำนวณ duration จาก meal_end - meal_start สำหรับ DataFrame ที่มี column 'meal_start' และ 'meal_end'
    คืนค่า DataFrame พร้อมคอลัมน์ 'duration', 'duration_min', 'duration_hr'
    """
    # แปลงเวลาเป็น timedelta
    df['meal_start'] = pd.to_timedelta(df['meal_start'].astype(str), errors='coerce')
    df['meal_end'] = pd.to_timedelta(df['meal_end'].astype(str), errors='coerce')
    
    # คำนวณ duration
    df['duration'] = df['meal_end'] - df['meal_start']
    

    
    return df

# ใช้งานกับ walk_away_duration_In_house
walk_away_duration_In_house = load_combine_duration(walk_away_duration_In_house)
walk_away_duration_walk_in = load_combine_duration(walk_away_duration_walk_in)

# ดูผลลัพธ์
#print(walk_away_duration_In_house[['meal_start','meal_end','duration']].head())

print(walk_away_duration_walk_in[['meal_start','meal_end','duration']].head())