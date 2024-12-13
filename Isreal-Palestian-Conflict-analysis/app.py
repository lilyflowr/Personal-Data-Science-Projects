import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

url = "https://raw.githubusercontent.com/lilyflowr/Personal-Data-Science-Projects/main/Isreal-Palestian-Conflict-analysis/fatalities_isr_pse_conflict_2000_to_2023.csv"

try:
    df = pd.read_csv(url, encoding='utf-8')
    df.columns = df.columns.str.strip() 

    # st.write("Columns in the DataFrame:", df.columns)

except pd.errors.ParserError as e:
    st.error("There was an issue reading the CSV file: " + str(e))
    st.stop()  



    
# Function to count fatalities by region
def count_fatalities_by_region(df, date_col='date_of_death', region_col='event_location_region'):
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    fatalities_count = df.groupby(region_col).size().reset_index(name='fatality_count')
    return fatalities_count

# sidebar code
no_event = len(df)
citizenship_counts = df['citizenship'].value_counts()
event_location_region = df['event_location_region'].value_counts()
hostilities_counts = df[df['took_part_in_the_hostilities'] == 'Yes']['citizenship'].value_counts()
no_hostilities_counts = df[df['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts()

st.sidebar.write("No of Event :", no_event)

col1,col2 = st.sidebar.columns(2)
col3,col4 = st.sidebar.columns(2)
with col1:
    st.subheader("citizenship_counts")
    st.write(citizenship_counts)
with col2:
    st.subheader("event_location_region")
    st.write(event_location_region)
with col3:
    st.subheader("hostilities_counts")
    st.write(hostilities_counts)

weapons_counts = df['ammunition'].value_counts()
st.sidebar.write("Weapon counts",weapons_counts)


# Data analysis
st.title("Isreal Palestine Conflict Analysis")
st.write('Dataset Sample',df)

col1,col2 = st.columns(2)
with col1:
    st.subheader("type of injuries")
    type_of_injury= df['type_of_injury'].value_counts()
    st.bar_chart(type_of_injury)
with col2:
    st.subheader("MaleFemaleCount")
    MFcounts = df['gender'].value_counts()
    st.bar_chart(MFcounts,color='#FF0000')

col1, col2 = st.columns(2)
with col1:
    st.subheader("Age Summary")
    age = df['age'].describe()
    st.write(age)
with col2:
    st.subheader("Even Location Region Count")
    eventregion = df['event_location_region'].value_counts()
    st.bar_chart(eventregion)

col1,col2 = st.columns(2)
with col1:
    residencecountbyreg = df.groupby('event_location_region')['place_of_residence'].nunique()
    st.subheader("Residence Percentage by Region")
    fig, ax = plt.subplots()
    ax.pie(residencecountbyreg,labels=residencecountbyreg.index, autopct='%1.1f%%')
    st.pyplot(fig)
with col2:
    injurytype = df['type_of_injury'].value_counts()
    st.subheader("Injury Types")
    fig,ax = plt.subplots()
    ax.pie(injurytype,labels=injurytype.index,autopct='%1.1f%%')
    st.pyplot(fig)

regionavgage = df.groupby('event_location_region')['age'].mean()
st.subheader("Avg Age by region")
st.bar_chart(regionavgage)

col1, col2 = st.columns(2)
with col1:
    IncidentcountbyNat = df.groupby('citizenship').size().reset_index(name='incident_count')
    st.subheader('Incident Count by Nationality')
    st.write(IncidentcountbyNat)
with col2:
    genderInc = df.groupby('gender').size().reset_index(name="incident_count")
    st.subheader('Incident Count by Gender')
    st.write(genderInc)

location_fatalities = count_fatalities_by_region(df)

key_regions = ["Gaza", "West Bank", "Jerusalem", "Haifa", "Tel Aviv"]
filtered_location_fatalities = location_fatalities[location_fatalities['event_location_region'].isin(key_regions)]

region_coordinates = {
"Gaza": {"lat": 31.5, "lon": 34.47},
"West Bank": {"lat": 32.0, "lon": 35.3},
"Jerusalem": {"lat": 31.78, "lon": 35.23},
"Haifa": {"lat": 32.82, "lon": 34.98},
"Tel Aviv": {"lat": 32.08, "lon": 34.78}
}

filtered_location_fatalities["lat"] = filtered_location_fatalities["event_location_region"].map(lambda x: region_coordinates[x]["lat"])
filtered_location_fatalities["lon"] = filtered_location_fatalities["event_location_region"].map(lambda x: region_coordinates[x]["lon"])


st.subheader("Geospatial Mapping of Fatalities")
fig = px.scatter_geo(
    filtered_location_fatalities,
    lat="lat",
    lon="lon",
    size="fatality_count",
    hover_name="event_location_region",
    title="Fatalities by Key Region",
    center={"lat": 31.5, "lon": 35.0},  
)
fig.update_geos(
    visible=True,
    resolution=110,
    showcountries=True,        
)
st.plotly_chart(fig)

# Time-based analysis 
df['date_of_event'] = pd.to_datetime(df['date_of_event'])
df['year'] = df['date_of_event'].dt.year
df['month'] = df['date_of_event'].dt.month_name()
time_events = df.groupby(['year', 'month']).size().reset_index(name='incident_count')
time_events['year_month'] = time_events['month'] + ' ' + time_events['year'].astype(str)
st.subheader('Time-Based Events')
st.line_chart(time_events.set_index('year_month')['incident_count'])





