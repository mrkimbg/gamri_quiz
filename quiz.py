import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

def check_answers(user_answers, correct_answers):
    results = []
    for ua, ca in zip(user_answers, correct_answers):
        results.append("정답" if ua == ca else "오답")
    return results

st.title(':clap:정보시스템 감리사 기출풀이:smile:')

uploaded_file = st.file_uploader("문제 엑셀 파일을 업로드해주세요.", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    user_answers = []

    for index, row in df.iterrows():
        st.write(f"문제 {index + 1}: {row['문제']}")
        options = ["None"] + [row['보기1'], row['보기2'], row['보기3'], row['보기4']]
        # answer = st.radio(f"문제 {index + 1}의 답 선택:", options)
        answer = st.radio(f"문제 {index + 1}의 답을 선택하세요.", options)

        if answer != "None":
            user_answers.append(options.index(answer))
        else:
            user_answers.append(None)

    if st.button("제출하기"):
        # 사용자 답을 1 기반으로 변환 (즉, 0 -> 1, 1 -> 2, ...)
        df['사용자 답'] = [ua + 1 if ua is not None else "선택하지 않음" for ua in user_answers]
        df['결과'] = check_answers(user_answers, df['답'].tolist())
        
        st.subheader("결과 확인")
        
        total_correct = df['결과'].tolist().count("정답")
        
        for index, row in df.iterrows():
            st.write(f"문제 {index + 1}: {row['문제']}")
            st.write(f"정답: {row['답']}, 사용자 답: {row['사용자 답']}, 결과: {row['결과']}")
        
        st.write(f"총 {len(df)}문제 중 {total_correct}개가 정답입니다.")

        # 현재 월, 일, 시간을 가져온다.
        now = datetime.now()
        current_time = now.strftime("%m%d%H%M")

        # 파일명 생성
        file_name = os.path.splitext(uploaded_file.name)[0] + "_" + current_time + '.xlsx'

        # 엑셀 다운로드
        towrite = io.BytesIO()
        downloaded_file = df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        st.download_button("결과 파일 다운로드", towrite, file_name, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
