# Import python packages
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
from snowflake.snowpark.context import get_active_session

st.set_page_config(layout="centered", initial_sidebar_state="expanded")  ## layout must be e "centered" or "wide"   #"auto" or "expanded" or "collapsed"

# Write directly to the app
st.title("Student Score Card")
st.text("This dashboard represents marks scored by students from class I to VII in the Final Exam")

session = get_active_session()

### Pie Chart

# Execute the SQL query
sql_query = """
SELECT CLASS,
    CASE
        WHEN score BETWEEN 80 AND 90 THEN '80-90 %'
        WHEN score BETWEEN 70 AND 80 THEN '70-80 %'
        WHEN score BETWEEN 60 AND 70 THEN '60-70 %'
        WHEN score < 60 THEN '< 60 %'
        WHEN score > 90 THEN '> 90 %'
    END AS LABEL,
    count(*) as COUNT
FROM STREAMLIT.REPORTING_TABLE.STUDENT_REPORTING_TABLE 
group by class,label
"""
result = session.sql(sql_query).collect()

# Convert the result into a Pandas DataFrame
df_pie_chart = pd.DataFrame(result, columns=['class', 'label', 'count'])
default_selection = [df_pie_chart['class'].iloc[0]]
selected_classes = st.sidebar.multiselect('Select classes', df_pie_chart['class'].unique(), default=default_selection)
df_filtered = df_pie_chart[df_pie_chart['class'].isin(selected_classes)]
df_pie_data = df_filtered.groupby('label')['count'].sum().reset_index()

# Create a pie chart
fig, ax = plt.subplots(figsize=(4, 4)) 
ax.pie(df_pie_data['count'], labels=df_pie_data['label'], autopct='%1.1f%%')

# Display the pie chart
st.pyplot(fig)

# Display bar chart
col1, col2 = st.columns([2, 3])#st.columns(2)

with col1:

    # Pass Vs Failed
    sql_query = """
    SELECT 
        class,
        SUM(CASE WHEN result = 'pass' THEN 1 ELSE 0 END) AS passed_count,
        SUM(CASE WHEN result = 'fail' THEN 1 ELSE 0 END) AS failed_count
    FROM STREAMLIT.REPORTING_TABLE.STUDENT_REPORTING_TABLE  
         
    GROUP BY 
        class;
    """
    result = session.sql(sql_query).collect()
    
    df = pd.DataFrame(result, columns=['class', 'passed_count', 'failed_count'])
    
    # Set the class column as the index
    df.set_index('class', inplace=True)
    
    # Plotting the bar chart using Streamlit's built-in function
    st.text('Passed Vs Failed student in each Class')
    st.bar_chart(df)
 
with col2:

    sql_query = """
    SELECT class, COUNT(score) as count
    FROM STREAMLIT.REPORTING_TABLE.STUDENT_REPORTING_TABLE 
    WHERE score > 70
    GROUP BY class
    """
    result = session.sql(sql_query).collect()
    
    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result)
    
    # Plotting the bar chart using Streamlit's built-in function
    
    st.text('Student Scoring more that 70% in Each Class')
    st.bar_chart(df.set_index(df.columns[0]),)


#chart
fig_warehouse_variance_df=px.bar(df_pie_chart,x="class",y="count",color ='label',orientation='v',title="Percentage Score across all the clases")
st.plotly_chart(fig_warehouse_variance_df, use_container_width=True)






 