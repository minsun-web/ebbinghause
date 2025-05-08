import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize DataFrame or load existing data
try:
    df = pd.read_csv('review_schedule.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'Content', 'Review 1', 'Review 2', 'Review 3', 'Review 4', 'Completed'])

st.title('Ebbinghaus Review Scheduler')

# User input for today's learning content
st.header("Enter Today's Learning Content")
today = datetime.now().strftime('%Y-%m-%d')
content = st.text_input('What did you learn today?')

if st.button('Add to Schedule') and content:
    # Calculate review dates based on Ebbinghaus schedule
    review_1 = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    review_2 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    review_3 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    review_4 = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    new_row = {
        'Date': today, 
        'Content': content, 
        'Review 1': review_1, 
        'Review 2': review_2, 
        'Review 3': review_3, 
        'Review 4': review_4, 
        'Completed': False
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('review_schedule.csv', index=False)
    st.success('Learning content added!')

# Display the review schedule
st.header('Review Schedule')
st.dataframe(df)

# Mark as reviewed
st.header('Mark Review as Completed')
if len(df) > 0:
    selected = st.selectbox('Select a row to mark as reviewed:', df['Content'])
    if st.button('Mark as Reviewed'):
        df.loc[df['Content'] == selected, 'Completed'] = True
        df.to_csv('review_schedule.csv', index=False)
        st.success(f'Marked "{selected}" as reviewed!')

