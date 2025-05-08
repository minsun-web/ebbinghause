import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import hashlib

# 사용자 데이터 디렉토리 설정
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

# 유저 정보를 저장할 파일 경로
USER_FILE = os.path.join(DATA_DIR, 'users.csv')

# 초기 사용자 파일 생성
if not os.path.exists(USER_FILE):
    df_users = pd.DataFrame(columns=['Username', 'Password'])
    df_users.to_csv(USER_FILE, index=False)

# 사용자 등록 함수
def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    df_users = pd.read_csv(USER_FILE)
    if username in df_users['Username'].values:
        return False, 'Username already exists'
    new_user = pd.DataFrame([[username, hashed_password]], columns=['Username', 'Password'])
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    df_users.to_csv(USER_FILE, index=False)
    return True, 'User registered successfully'

# 사용자 인증 함수
def authenticate(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    df_users = pd.read_csv(USER_FILE)
    if username in df_users['Username'].values:
        stored_password = df_users[df_users['Username'] == username]['Password'].values[0]
        if stored_password == hashed_password:
            return True
    return False

# 로그인 함수
def login():
    st.title("Login")
    option = st.selectbox("Select an option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Register":
        new_password = st.text_input("Create Password", type="password")
        if st.button("Register"):
            success, message = register_user(username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

    if option == "Login":
        if username == 'admin' and password == 'adminpass':
            st.success("Admin login successful!")
            return username
        elif authenticate(username, password):
            st.success("User login successful!")
            return username
        else:
            st.error("Invalid username or password")
            return None

# 로그인 실행
current_user = login()

# 사용자별 데이터 파일 경로 설정
if current_user:
    data_path = os.path.join(DATA_DIR, f"{current_user}_review_schedule.csv")

    if current_user == 'admin':
        st.title('Admin Dashboard')
        st.header('All Users Data')
        all_files = os.listdir(DATA_DIR)
        for file in all_files:
            if file.endswith('_review_schedule.csv'):
                st.subheader(file)
                user_df = pd.read_csv(os.path.join(DATA_DIR, file))
                st.dataframe(user_df)
    else:
        try:
            df = pd.read_csv(data_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Date', 'Content', 'Review 1', 'Review 2', 'Review 3', 'Review 4', 'Completed'])

        st.title(f'Welcome, {current_user}!')

        # 학습 내용 입력
        st.header("Enter Today's Learning Content")
        today = datetime.now().strftime('%Y-%m-%d')
        content = st.text_input('What did you learn today?')

        if st.button('Add to Schedule') and content:
            review_1 = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            review_2 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            review_3 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            review_4 = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
            new_row = {'Date': today, 'Content': content, 'Review 1': review_1, 'Review 2': review_2, 'Review 3': review_3, 'Review 4': review_4, 'Completed': False}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(data_path, index=False)
            st.success('Learning content added!')

        # 복습 일정 표시
        st.header('Review Schedule')
        st.dataframe(df)

        # 복습 완료 표시 및 수정 기능
        if len(df) > 0:
            st.header('Edit or Update Entries')
            # 수정할 항목 선택
            edit_content = st.selectbox('Select an entry to edit:', df['Content'])
            new_content = st.text_input('Update Content', value=edit_content)
            update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]))
            if st.button('Update Entry'):
                df.loc[df['Content'] == edit_content, 'Content'] = new_content
                df.loc[df['Content'] == new_content, 'Completed'] = update_status
                df.to_csv(data_path, index=False)
                st.success(f'Updated "{new_content}"!')

            # 복습 완료 표시
            selected = st.selectbox('Select a row to mark as reviewed:', df['Content'])
            if st.button('Mark as Reviewed'):
                df.loc[df['Content'] == selected, 'Completed'] = True
                df.to_csv(data_path, index=False)
                st.success(f'Marked "{selected}" as reviewed!')
        if len(df) > 0:
                    # 수정할 항목 선택
            edit_content = st.selectbox('Select an entry to edit:', df['Content'])
            new_content = st.text_input('Update Content', value=edit_content)
            update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]))
            if st.button('Update Entry'):
                df.loc[df['Content'] == edit_content, 'Content'] = new_content
                df.loc[df['Content'] == new_content, 'Completed'] = update_status
                df.to_csv(data_path, index=False)
                st.success(f'Updated "{new_content}"!')
        if len(df) > 0:
            # 수정할 항목 선택
            edit_content = st.selectbox('Select an entry to edit:', df['Content'])
            new_content = st.text_input('Update Content', value=edit_content)
            update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]))
            if st.button('Update Entry'):
                df.loc[df['Content'] == edit_content, 'Content'] = new_content
                df.loc[df['Content'] == new_content, 'Completed'] = update_status
                df.to_csv(data_path, index=False)
                st.success(f'Updated "{new_content}"!')
    # 수정할 항목 선택
    edit_content = st.selectbox('Select an entry to edit:', df['Content'])
    new_content = st.text_input('Update Content', value=edit_content)
    update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]))
    if st.button('Update Entry'):
        df.loc[df['Content'] == edit_content, 'Content'] = new_content
        df.loc[df['Content'] == new_content, 'Completed'] = update_status
        df.to_csv(data_path, index=False)
        st.success(f'Updated "{new_content}"!')
    edit_content = st.selectbox('Select an entry to edit:', df['Content'])
    new_content = st.text_input('Update Content', value=edit_content)
    update_status = st.checkbox('Mark as Completed', value=bool(df.loc[df['Content'] == edit_content, 'Completed'].values[0]))
    if st.button('Update Entry'):
        df.loc[df['Content'] == edit_content, 'Content'] = new_content
        df.loc[df['Content'] == new_content, 'Completed'] = update_status
        df.to_csv(data_path, index=False)
        st.success(f'Updated "{new_content}"!')
    # 수정할 항목 선택
    edit_content = st.selectbox('Select an entry to edit:', df['Content'])
    new_content = st.text_input('Update Content', value=edit_content)
    update_status = st.checkbox('Mark as Completed', value=df.loc[df['Content'] == edit_content, 'Completed'].values[0])
    if st.button('Update Entry'):
        df.loc[df['Content'] == edit_content, 'Content'] = new_content
        df.loc[df['Content'] == new_content, 'Completed'] = update_status
        df.to_csv(data_path, index=False)
        st.success(f'Updated "{new_content}"!')
            selected = st.selectbox('Select a row to mark as reviewed:', df['Content'])
            if st.button('Mark as Reviewed'):
                df.loc[df['Content'] == selected, 'Completed'] = True
                df.to_csv(data_path, index=False)
                st.success(f'Marked "{selected}" as reviewed!')

