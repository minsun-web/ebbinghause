# 학습 내용 입력
st.header("Enter Today's Learning Content")
today = datetime.now().strftime('%Y-%m-%d')
content = st.text_input('What did you learn today?', key='add_content')

if st.button('Add to Schedule', key='add_button') and content:
    review_1 = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    review_2 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    review_3 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    review_4 = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    new_row = {'Date': today, 'Content': content, 'Review 1': review_1, 'Review 2': review_2, 'Review 3': review_3, 'Review 4': review_4, 'Completed': False}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(data_path, index=False)
    st.success('Learning content added!')

# 복습 일정 표시 및 수정 기능
st.header('Review Schedule')
if len(df) > 0:
    for index, row in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            updated_content = st.text_input(f'Update: {row["Content"]}', value=row["Content"], key=f'content_{index}')
        with col2:
            completed = st.checkbox('Completed', value=row["Completed"], key=f'completed_{index}')

        if st.button('Save Changes', key=f'update_{index}'):
            df.at[index, 'Content'] = updated_content
            df.at[index, 'Completed'] = completed
            df.to_csv(data_path, index=False)
            st.success(f'Updated: {updated_content}')

st.dataframe(df)
