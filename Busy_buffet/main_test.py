import streamlit as st
import pandas as pd
from reducetime import load_combine_duration
import numpy as np
import matplotlib.pyplot as plt

# run: py -m streamlit run main_test.py

# ข้อมูล
file = '2026 Data Test1 Final - Busy Buffet Dataset.xlsx'
sheets = {
    'fri': '133',
    'sat': '143',
    'sun': '153',
    'tues': '173',
    'wed': '183'
}

# Sidebar
menu = st.sidebar.radio(
    "Select",
    ["ควรที่ลดเวลาในการกินอาหารของลุกค้าไหม", "ควรที่จะให้ลูกค้า In house skip ได้ไหม",
     'ควรที่จะเพิ่มราคาเป็น 259 ทุกวันไหม',"ลูกค้า ไม่ happy เมื่อ ต้องรอนาน",'ร้านยุ่งทุกวันจริงไหม','queue_table',
     'Priority_balancing']
)

# -------------------------------
# Overview (Weekday)
# -------------------------------
from reducetime import load_combine_duration
if menu == "ควรที่ลดเวลาในการกินอาหารของลุกค้าไหม":
    week_day = ['fri','tues','wed']

    week_day_duration = load_combine_duration(file, sheets, week_day)

    df_plot = week_day_duration[
        (week_day_duration['duration_hr'] >= 0) &
        (week_day_duration['duration_hr'] <= 5)
    ].copy()

    bins = [0,1,2,3,4,5]
    labels = ['0-1h','1-2h','2-3h','3-4h','4-5h']

    df_plot['duration_bin'] = pd.cut(
        df_plot['duration_hr'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    count_data = df_plot['duration_bin'].value_counts().sort_index()
    count_data = count_data.reindex(labels, fill_value=0)

    st.title("Weekday Customer Duration (0–5 Hours)")
    st.bar_chart(count_data)

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
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    
    week_end= ['sat','sun']

    week_end_duration = load_combine_duration(file, sheets, week_end)

    df_plot = week_end_duration[
        (week_end_duration['duration_hr'] >= 0) &
        (week_end_duration['duration_hr'] <= 5)
    ].copy()

    bins = [0,1,2,3,4,5]
    labels = ['0-1h','1-2h','2-3h','3-4h','4-5h']

    df_plot['duration_bin'] = pd.cut(
        df_plot['duration_hr'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    count_data = df_plot['duration_bin'].value_counts().sort_index()
    count_data = count_data.reindex(labels, fill_value=0)

    st.title("Weekday Customer Duration (0–5 Hours)")
    st.bar_chart(count_data)

    #สร้าง card แสดง avg_meal_duration_time ใน normal day
    # โหลดข้อมูล
    week_end_duration = load_combine_duration(file, sheets, week_day)
    # คำนวณค่าเฉลี่ย duration
    weekend_avg = week_end_duration['duration'].mean()  # timedelta
    # แปลงเป็นชั่วโมง + นาที
    total_seconds = weekend_avg.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    # ฟอร์แมตเป็น string
    avg_str = f"{hours}h {minutes}m"
    # แสดง card
    st.title("Customer Meal Duration week end")
    st.metric(label="Average Weekend Duration", value=avg_str)
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------


# -------------------------------
# ควรที่จะให้ลูกค้า In house skip ได้ไหม
# -------------------------------
elif menu == "ควรที่จะให้ลูกค้า In house skip ได้ไหม":
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



# -------------------------------
# ควรที่จะให้ลูกค้า In house skip ได้ไหม
# -------------------------------
elif menu == "ควรที่จะเพิ่มราคาเป็น 259 ทุกวันไหม":
    import matplotlib.pyplot as plt
    from increase_price import customer_lost_calculation , total_same_price

    percent_list = list(range(10, 71, 1))
    revenue_list = [customer_lost_calculation(p) for p in percent_list]

    # สร้าง figure
    fig, ax = plt.subplots()

    ax.plot(percent_list, revenue_list)

    # เส้นรายได้เดิม
    ax.axhline(y=total_same_price, linestyle='--', color='red')

    # ตั้งค่า
    ax.set_xlabel("Customer Loss (%)")
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue vs Customer Loss (%)")

    # แสดงใน streamlit
    st.pyplot(fig)

# -------------------------------
# ลูกค้า ไม่ happy เมื่อ ต้องรอนาน
# -------------------------------

elif menu == "ลูกค้า ไม่ happy เมื่อ ต้องรอนาน":

    import matplotlib.pyplot as plt
    #ลูกค้า Inhouse ออกจากคิวคิดเป็นเท่าไร่
    from waitng_in_queue import In_queue_In_house ,walk_away_In_house ,walk_away_duration_In_house,walk_away_duration_walk_in
    from waitng_in_queue import walk_away_walk_in,In_queue_walk_in

    print(len(In_queue_In_house))
    print(len(walk_away_In_house))

    served = len(In_queue_In_house) - len(walk_away_In_house)
    walk_away = len(walk_away_In_house)

    # เตรียมข้อมูล
    sizes = [served, walk_away]
    labels = ['Served', 'Walk-away']
    colors = ['#4CAF50', '#FF5722']  # สีเขียวและแดง  
    explode = (0.05, 0.05)  # แยกชิ้นส่วนเล็กน้อย

    # สร้าง Donut Chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, explode=explode, wedgeprops={'width':0.3})

    # วงกลมตรงกลางเป็น donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')  # ทำให้เป็นวงกลม
    plt.title("In-house Customer Status")

    # แสดงใน Streamlit
    st.pyplot(fig)
# -------------------------------


# สร้างกราฟ Walk-away In house Customers by Waiting Duration
    walk_away_duration_In_house['duration_min'] = walk_away_duration_In_house['duration'].dt.total_seconds() / 60

    # กำหนด bin ขึ้นทุก 5 นาที (ปรับได้)
    bin_size = 5
    max_duration = int(walk_away_duration_In_house['duration_min'].max()) + bin_size
    bins = np.arange(0, max_duration + bin_size, bin_size)

    # จัดกลุ่ม duration
    walk_away_duration_In_house['duration_bin'] = pd.cut(
    walk_away_duration_In_house['duration_min'], bins=bins, right=False
    )

    # นับจำนวนคนในแต่ละ bin
    count_per_bin = walk_away_duration_In_house.groupby('duration_bin').size()

    # วาด Bar Chart
    fig, ax = plt.subplots(figsize=(10,6))
    count_per_bin.plot(kind='bar', ax=ax, color='#FF5722')

    ax.set_xlabel('Waiting Duration (min)')
    ax.set_ylabel('Number of Walk-away Customers')
    ax.set_title('Walk-away In house Customers by Waiting Duration')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # แสดงใน Streamlit
    st.pyplot(fig)



#--------------------------------------------------------------------
#ฝั่งลูกค้า walk in
#--------------------------------------------------------------------

    served = len(In_queue_walk_in) - len(walk_away_walk_in)
    walk_away = len(walk_away_walk_in)

    # เตรียมข้อมูล
    sizes = [served, walk_away]
    labels = ['Served', 'Walk-away']
    colors = ['#4CAF50', '#FF5722']  # สีเขียวและแดง  
    explode = (0.05, 0.05)  # แยกชิ้นส่วนเล็กน้อย

    # สร้าง Donut Chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, explode=explode, wedgeprops={'width':0.3})

    # วงกลมตรงกลางเป็น donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')  # ทำให้เป็นวงกลม
    plt.title("Walk in Customer Status")

    # แสดงใน Streamlit
    st.pyplot(fig)
# -------------------------------


# สร้างกราฟ Walk-away Walk in  Customers by Waiting Duration
    walk_away_duration_walk_in['duration_min'] = walk_away_duration_walk_in['duration'].dt.total_seconds() / 60

    # กำหนด bin ขึ้นทุก 5 นาที (ปรับได้)
    bin_size = 5
    max_duration = int(walk_away_duration_walk_in['duration_min'].max()) + bin_size
    bins = np.arange(0, max_duration + bin_size, bin_size)

    # จัดกลุ่ม duration
    walk_away_duration_walk_in['duration_bin'] = pd.cut(
    walk_away_duration_walk_in['duration_min'], bins=bins, right=False
    )

    # นับจำนวนคนในแต่ละ bin
    count_per_bin = walk_away_duration_walk_in.groupby('duration_bin').size()

    # วาด Bar Chart
    fig, ax = plt.subplots(figsize=(10,6))
    count_per_bin.plot(kind='bar', ax=ax, color='#FF5722')

    ax.set_xlabel('Waiting Duration (min)')
    ax.set_ylabel('Number of Walk-away Customers')
    ax.set_title('Walk-away Walk in Customers by Waiting Duration')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # แสดงใน Streamlit
    st.pyplot(fig)


#--------------------------------------------------------------------
#Busy everday ?
#--------------------------------------------------------------------
    #เตรียมข้อมูล




elif menu == "ร้านยุ่งทุกวันจริงไหม":

    # เตรียมข้อมูล
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
        df['day'] = day
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    # Streamlit sidebar: เลือกวันและประเภทลูกค้า
    days_options = ['fri','sat','sun','tues','wed']
    selected_days = st.sidebar.multiselect("Select days", days_options, default=days_options)

    show_served = st.sidebar.checkbox("Show Served (In-house)", value=True)
    show_walk_away = st.sidebar.checkbox("Show Walk-away", value=True)

    # กรองตามวันที่เลือก
    df_filtered = combined_df[combined_df['day'].isin(selected_days)]

    # รวม pax ต่อวัน
    data = {}
    if show_served:
        served = df_filtered[df_filtered['Guest_type']=='In house'].groupby('day')['pax'].sum()
        data['Served'] = served
    if show_walk_away:
        walk_away = df_filtered[df_filtered['table_no.'].notna()].groupby('day')['pax'].sum()
        data['Walk-away'] = walk_away

    df_counts = pd.DataFrame(data).fillna(0)

    # เรียงวันตามลำดับ
    df_counts = df_counts.reindex(days_options)

    # วาด Stacked Bar Chart
    fig, ax = plt.subplots(figsize=(8,5))
    df_counts.plot(kind='bar', stacked=True, ax=ax, color=['#4CAF50','#FF5722'])

    ax.set_xlabel('Day')
    ax.set_ylabel('Number of People (pax)')
    ax.set_title('Customer Status per Day (by pax)')
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)


#--------------------------------------------------------------------
#queue_table
#--------------------------------------------------------------------

elif menu == "queue_table":

    from queue_table import walk_in_duration_avg, in_house_duration_avg

    # ข้อมูลสำหรับ Bar Chart
    guest_types = ['Walk-in', 'In-house']
    avg_durations = [walk_in_duration_avg, in_house_duration_avg]

    # วาด Bar Chart
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(guest_types, avg_durations, color=['#2196F3','#4CAF50'])
    ax.set_ylabel('Average Waiting Duration (min)')
    ax.set_title('Average Waiting Duration by Guest Type')
    for i, v in enumerate(avg_durations):
        ax.text(i, v + 0.5, f"{v:.1f}", ha='center')  # ใส่ตัวเลขด้านบน bar

    plt.tight_layout()

    # แสดงใน Streamlit
    st.pyplot(fig)

# -------------------------------
# ควรที่จะให้ลูกค้า In house skip ได้ไหม
# -------------------------------
elif menu == "Priority_balancing":
    
    
    from Priority_balancing import df_plot,avg_by_type,fifo_type,fifo_wait,alt_wait,alt_type
    

    # -----------------------------
    # เตรียมข้อมูล
    # -----------------------------
    guest_types = ['In house', 'Walk in']

    fifo_values = [
        avg_by_type(fifo_wait, fifo_type, 'In house'),
        avg_by_type(fifo_wait, fifo_type, 'Walk in')
    ]

    alt_values = [
        avg_by_type(alt_wait, alt_type, 'In house'),
        avg_by_type(alt_wait, alt_type, 'Walk in')
    ]

    # -----------------------------
    # Plot
    # -----------------------------
    x = np.arange(len(guest_types))  # [0, 1]
    width = 0.35

    fig, ax = plt.subplots()

    # FIFO (แท่งซ้าย)
    ax.bar(x - width/2, fifo_values, width, label='FIFO')

    # Alternating (แท่งขวา)
    ax.bar(x + width/2, alt_values, width, label='Alternating')

    # ตั้งค่าแกน
    ax.set_xticks(x)
    ax.set_xticklabels(guest_types)
    ax.set_ylabel("Average Waiting Time (minutes)")
    ax.set_title("FIFO vs Alternating by Guest Type")

    ax.legend()

    # แสดงใน streamlit
    st.pyplot(fig)
