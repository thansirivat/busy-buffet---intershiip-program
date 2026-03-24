import numpy as np
import pandas as pd

file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'

sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}

#ทำการหาเวลาในการกิน ตั้งแต่ start meal ถึง end meal
def load_combine_duration(file, sheets, selected_days):
    dfs = []
    
    for day in selected_days:
        df = pd.read_excel(file, sheet_name=sheets[day])
        
        # แปลงเวลา
        df['meal_start'] = pd.to_timedelta(df['meal_start'].astype(str))
        df['meal_end'] = pd.to_timedelta(df['meal_end'].astype(str))
        
        dfs.append(df)
    
    # รวม DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # คำนวณ duration
    combined_df['duration'] = combined_df['meal_end'] - combined_df['meal_start']
    
        # แปลงเป็นชั่วโมง
    combined_df['duration_hr'] = combined_df['duration'].dt.total_seconds() / 3600
    
    # (optional) นาที
    combined_df['duration_min'] = combined_df['duration'].dt.total_seconds() / 60
    
    return combined_df

#สร้างข้อมูล duration ของลูกคา week day และเวลาในการกินเฉลี่ย
week_day = ['fri', 'tues', 'wed']
week_day_duration = load_combine_duration(file, sheets, week_day)
weekday_avg = week_day_duration['duration'].mean()

print(weekday_avg)

#สร้างข้อมูล duration ของลูกคา week end และเวลาในการกินเฉลี่ย
week_end = ['sat','sun']
week_end_duration = load_combine_duration(file,sheets,week_end)
weekend_avg = week_end_duration['duration'].mean()

print(weekend_avg)