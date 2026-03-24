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