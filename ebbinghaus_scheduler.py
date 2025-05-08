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
        return False, '사용자 이름이 이미 존재합니다.'
    new_user = pd.DataFrame([[username, hashed_password]], columns=['Username', 'Password'])
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    df_users.to_csv(USER_FILE, index=False)
    return True, '사용자 등록 성공!'

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
    st.title("꿈을 꾸는 문어🐙")
    option = st.selectbox("옵션 선택", ["로그인", "회원가입"])
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    if option == "회원가입":
        new_password = st.text_input("비밀번호 생성", type="password")
        if st.button("회원가입"):
            success, message = register_user(username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

    if option == "로그인":
        if username == 'admin' and password == 'adminpass':
            st.success("관리자 로그인 성공!")
            return username
        elif authenticate(username, password):
            st.success("사용자 로그인 성공!")
            return username
        else:
            st.error("잘못된 사용자 이름 또는 비밀번호입니다.")
            return None

# 로그인 실행
current_user = login()

# 사용자별 데이터 파일 경로 설정
if current_user:
    data_path = os.path.join(DATA_DIR, f"{current_user}_review_schedule.csv")

    if current_user == 'admin':
        st.title('관리자 대시보드')
        st.header('모든 사용자 데이터')
        all_files = os.listdir(DATA_DIR)
        for file in all_files:
            if file.endswith('_review_schedule.csv'):
                st.subheader(file)
                user_df = pd.read_csv(os.path.join(DATA_DIR, file))
                st.dataframe(user_df)
    else:
        try:
            df = pd.read_csv(data_path)
            # 컬럼명이 영어로 되어 있을 경우 한글로 변환
            if 'Content' in df.columns:
                df.rename(columns={'Content': '내용', 'Date': '날짜', 'Review 1': '복습 1', 'Review 2': '복습 2', 'Review 3': '복습 3', 'Review 4': '복습 4', 'Completed': '완료 여부'}, inplace=True)
                df.to_csv(data_path, index=False)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['날짜', '내용', '복습 1', '복습 2', '복습 3', '복습 4', '완료 여부'])

        st.title(f'평생기억 하자피🐙 {current_user}!')

        # 학습 내용 입력
        st.header("오늘 학습 내용을 입력하세요")
        today = datetime.now().strftime('%Y-%m-%d')
        content = st.text_input('오늘 무엇을 배웠나요><?')

        if st.button('일정에 추가') and content:
            review_1 = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            review_2 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            review_3 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            review_4 = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
            new_row = {'날짜': today, '내용': content, '복습 1': review_1, '복습 2': review_2, '복습 3': review_3, '복습 4': review_4, '완료 여부': False}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(data_path, index=False)
            st.success('학습 내용이 추가되었습니다!')

        # 복습 일정 표시 및 수정 기능
        st.header('복습 일정')
        if not df.empty:
            selected_row = st.selectbox('수정할 행을 선택하세요:', df.index)
            if selected_row is not None:
                with st.expander(f'행 수정 {selected_row}'):
                    selected_content = df.loc[selected_row, '내용']
                    updated_content = st.text_input('내용 수정', value=selected_content)
                    completed = st.checkbox('완료 여부', value=df.loc[selected_row, '완료 여부'])
                    if st.button('수정'):
                        df.loc[selected_row, '내용'] = updated_content
                        df.loc[selected_row, '완료 여부'] = completed
                        df.to_csv(data_path, index=False)
                        st.success('성공적으로 수정되었습니다!')
        st.dataframe(df)
