# 복습 완료 표시 및 수정 기능
def edit_or_update(df, data_path):
    if len(df) > 0:
        st.header('Edit or Update Entries')

        # 수정할 항목 선택
        edit_content = st.selectbox('Select an entry to edit:', df['Content'], key="edit_selectbox")
        new_content = st.text_input('Update Content', value=edit_content, key="edit_text_input")
        update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]), key="edit_checkbox")
        
        if st.button('Update Entry', key="update_button"):
            df.loc[df['Content'] == edit_content, 'Content'] = new_content
            df.loc[df['Content'] == new_content, 'Completed'] = update_status
            df.to_csv(data_path, index=False)
            st.success(f'Updated "{new_content}"!')

        # 복습 완료 표시
        st.header('Mark Review as Completed')
        selected = st.selectbox('Select a row to mark as reviewed:', df['Content'], key="review_selectbox")
        
        if st.button('Mark as Reviewed', key="review_button"):
            df.loc[df['Content'] == selected, 'Completed'] = True
            df.to_csv(data_path, index=False)
            st.success(f'Marked "{selected}" as reviewed!')

# 코드 실행 부분
if len(df) > 0:
    edit_or_update(df, data_path)
