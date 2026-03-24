import streamlit as st
import pandas as pd

#run web site
#py -m streamlit run main.py

#จัดการข้อมูล
file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'
sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#สร้างกราฟแสดงว่าคนกินอาหารใช้ช่วงเวลาอยู่ที่เท่าไหร่บ้าง ในวันธรรมดา
from reducetime import load_combine_duration
week_day = ['fri','tues','wed']
# โหลดข้อมูล
week_day_duration = load_combine_duration(file, sheets, week_day)
# filter 0–5 ชั่วโมง
df_plot = week_day_duration[(week_day_duration['duration_hr'] >= 0) &
                            (week_day_duration['duration_hr'] <= 5)].copy()

# binning จัดกลุ่มค่าตัวเลข (continuous data)
bins = [0,1,2,3,4,5]
labels = ['0-1h','1-2h','2-3h','3-4h','4-5h']
df_plot['duration_bin'] = pd.cut(df_plot['duration_hr'], bins=bins, labels=labels, include_lowest=True)

count_data = df_plot['duration_bin'].value_counts().sort_index()
count_data = count_data.reindex(labels, fill_value=0)

st.title(" Weekday Customer Duration (0–5 Hours)")
st.bar_chart(count_data)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#สร้าง card แสดง avg_meal_duration_time ใน normal day
# โหลดข้อมูล
week_day_duration = load_combine_duration(file, sheets, week_day)
# คำนวณค่าเฉลี่ย duration
weekday_avg = week_day_duration['duration'].mean()  # timedelta
# แปลงเป็นชั่วโมง + นาที
total_seconds = weekday_avg.total_seconds()
hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
# ฟอร์แมตเป็น string
avg_str = f"{hours}h {minutes}m"
# แสดง card
st.title("Customer Meal Duration")
st.metric(label="Average Weekday Duration", value=avg_str)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#สร้างกราฟแสดงว่าคนกินอาหารใช้ช่วงเวลาอยู่ที่เท่าไหร่บ้าง ในวันหยุด
#สร้างกราฟแสดงว่าคนกินอาหารใช้ช่วงเวลาอยู่ที่เท่าไหร่บ้าง ในวันธรรมดา
week_end = ['sat','sun']
# โหลดข้อมูล
week_end_duration = load_combine_duration(file, sheets, week_end)
# filter 0–5 ชั่วโมง
df_plot_weakend = week_end_duration[(week_end_duration['duration_hr'] >= 0) &
                            (week_end_duration['duration_hr'] <= 5)].copy()

# binning จัดกลุ่มค่าตัวเลข (continuous data)
bins = [0,1,2,3,4,5]
labels = ['0-1h','1-2h','2-3h','3-4h','4-5h']
df_plot_weakend['duration_bin'] = pd.cut(df_plot_weakend['duration_hr'], bins=bins, labels=labels, include_lowest=True)

count_data_weakend = df_plot_weakend['duration_bin'].value_counts().sort_index()
count_data_weakend = count_data_weakend.reindex(labels, fill_value=0)

st.title(" Weekday Customer Duration (0–5 Hours)")
st.bar_chart(count_data)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

# โหลดข้อมูล weekend
week_end = ['sat', 'sun']
week_end_duration = load_combine_duration(file, sheets, week_end)
# คำนวณค่าเฉลี่ย duration ของ weekend
weekend_avg = week_end_duration['duration'].mean()  # timedelta
# แปลงเป็นชั่วโมง + นาที
total_seconds_weekend = weekend_avg.total_seconds()
hours_weekend = int(total_seconds_weekend // 3600)
minutes_weekend = int((total_seconds_weekend % 3600) // 60)
# ฟอร์แมตเป็น string
avg_str_weekend = f"{hours_weekend}h {minutes_weekend}m"
# แสดง card
st.title("Customer Meal Duration")
st.metric(label="Average Weekend Duration", value=avg_str_weekend)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------


from In_house_skip_queue import In_queue_In_house, walk_away_In_house
import matplotlib.pyplot as plt

print(len(In_queue_In_house))
print(len(walk_away_In_house))


# คำนวณค่า
served = len(In_queue_In_house) - len(walk_away_In_house)
walk_away = len(walk_away_In_house)

# กัน error กรณีไม่มี queue
if len(In_queue_In_house) > 0:

    labels = ['Served', 'Walk Away']
    sizes = [served, walk_away]

    # สร้าง figure
    fig, ax = plt.subplots()

    # pie chart
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90
    )

    # ทำให้เป็น donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # ทำให้เป็นวงกลม
    ax.axis('equal')

    # แสดงใน Streamlit
    st.title("Queue Outcome Distribution")
    st.pyplot(fig)

else:
    st.write("No queue data available")


#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#ตอบคำถามว่าควรจะเพิ่มราคาไหม

import matplotlib.pyplot as plt
from increase_price import generate_data , total_pax , total_same_price
# สร้างข้อมูล
percent_list, revenue_list = generate_data(total_pax)
# วาดกราฟด้วย matplotlib
fig, ax = plt.subplots(figsize=(10,6))
# เส้นรายได้ใหม่
ax.plot(percent_list, revenue_list, marker='o', label='New Revenue (259 THB)')
# เส้นรายได้เดิม (total_same_price)
ax.axhline(y=total_same_price, color='red', linestyle='--', label='Current Revenue')
# ชื่อกราฟ
ax.set_title("Revenue vs Customer Retention (%)")
ax.set_xlabel("Customer Retention (%)")
ax.set_ylabel("Revenue (THB)")
# legend + grid
ax.legend()
ax.grid(True)
# แสดงกราฟใน Streamlit
st.pyplot(fig)

#-----------------------------------------------------------------------------------
