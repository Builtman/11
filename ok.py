import streamlit as st
import pandas as pd

# 초기 데이터프레임 설정
if 'income' not in st.session_state:
    st.session_state.income = pd.DataFrame(columns=['날짜', '장르', '이유', '지출금액'])
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['날짜', '장르', '이유', '지출금액'])

# 사이드바 메뉴 설정
menu = st.sidebar.selectbox('평가', ['추천', '비추', '현황'])

if menu == '영화 일기':
    st.title('추천')
    # 수입 데이터 표시
    if st.session_state.income.empty:
        st.write('진짜 재밌게 본 영화들')
    else:
        st.write(st.session_state.income)

    # 수입 입력 폼
    st.header('추천 영화 추가')
    with st.form('income_form'):
        date = st.date_input('날짜')
        category = st.selectbox('장르', ['월급', '투자', '기타'])
        description = st.text_input('이유')
        amount = st.number_input('지출 금액', min_value=0)
        submitted = st.form_submit_button('추가')

        if submitted:
            new_income = pd.DataFrame({'날짜': [date], '장르': [category], '이유': [description], '지출 금액': [amount]})
            st.session_state.income = pd.concat([st.session_state.income, new_income], ignore_index=True)
            st.success('추천!!')

elif menu == '영화 일기':
    st.title('비추천')
    # 지출 데이터 표시
    if st.session_state.expenses.empty:
        st.write('진짜 재밌없게 본 영화들')
    else:
        st.write(st.session_state.expenses)

    # 지출 입력 폼
    st.header('비추천 영화 추가')
    with st.form('expense_form'):
        date = st.date_input('날짜')
        category = st.selectbox('장르', ['식비', '교통', '쇼핑', '기타'])
        description = st.text_input('이유')
        amount = st.number_input('지출 금액', min_value=0)
        submitted = st.form_submit_button('추가')

        if submitted:
            new_expense = pd.DataFrame({'날짜': [date], '장르': [category], '이유': [description], '지출 금액': [amount]})
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
            st.success('비추!!')

elif menu == '현황':
    st.title('추천,비추천 영화 모음')

    if st.session_state.income.empty and st.session_state.expenses.empty:
        st.write('몰아보기')
    else:
        # 월별 데이터 집계
        income_df = st.session_state.income.copy()
        income_df['날짜'] = pd.to_datetime(income_df['날짜'])
        income_df['월'] = income_df['날짜'].dt.to_period('M').astype(str)
        monthly_income = income_df.groupby('월')['지출 금액'].sum()

        expenses_df = st.session_state.expenses.copy()
        expenses_df['날짜'] = pd.to_datetime(expenses_df['날짜'])
        expenses_df['월'] = expenses_df['날짜'].dt.to_period('M').astype(str)
        monthly_expenses = expenses_df.groupby('월')['지출 금액'].sum()

        # 월별 수입 및 지출 데이터 병합
        monthly_summary = pd.concat([monthly_income, monthly_expenses], axis=1, keys=['지출']).fillna(0)

        # 월별 수입 및 지출 그래프
        st.line_chart(monthly_summary)

# streamlit run ok.py