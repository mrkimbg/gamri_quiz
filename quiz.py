import streamlit as st
import pandas as pd
import os
import datetime

# Set the title of the web app
st.title(':clap:정보시스템 감리사 기출풀이:smile:')

# File uploader allows user to upload their own file
uploaded_files = st.sidebar.file_uploader(":tada:기출문제 파일 업로드:file_folder:", type=['xlsx'], accept_multiple_files=True)

if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

if uploaded_files:
    file_list = [uploaded_file.name for uploaded_file in uploaded_files]
    selected_file = st.sidebar.selectbox(":file_folder:파일을 선택:point_right:하세요", file_list)
    for uploaded_file in uploaded_files:
        if uploaded_file.name == selected_file:
            # Remove the file extension from the selected file name
            file_name, file_extension = os.path.splitext(selected_file)
            
            # Set the title with the selected file name
            st.markdown(f"#### \"{file_name}\"을 선택하셨습니다.")

            # Start exam button
            if st.button('**시험 시작**'):
                st.session_state['start_time'] = datetime.datetime.now()
                st.write('시험을 시작했습니다!')

            if st.session_state['start_time'] is not None:
                df = pd.read_excel(uploaded_file)

                # Create a dictionary to store user answers
                user_answers = {}

                for index, row in df.iterrows():
                    # Display each question and choices with markdown for consistency
                    st.markdown(f'**문제 {index + 1}**')
                    st.markdown(row["문제"])

                    options = [None, f'1) {row["보기1"]}', f'2) {row["보기2"]}', f'3) {row["보기3"]}', f'4) {row["보기4"]}']
                    answer = st.radio('보기 선택:', options, key=str(index) + uploaded_file.name)

                    # Save the user's answer (Extract the number only from the answer)
                    if answer is not None:
                        user_answers[index] = int(answer[0])  # The first character of the answer is the number of the choice

                # Submit button
                if st.button('**제출 -** ' + uploaded_file.name):
                    end_time = datetime.datetime.now()
                    time_taken = end_time - st.session_state['start_time']

                    # Convert time taken to minutes and seconds
                    minutes, seconds = divmod(time_taken.total_seconds(), 60)

                    # Get the current date in YYMMDD format
                    current_date = end_time.strftime('%y%m%d')

                    # Compare user answers with correct answers and save the results to the dataframe
                    df['제출'] = df.index.map(user_answers)
                    df['결과'] = df.apply(lambda row: 'O' if row['제출'] == row["답"] else 'X', axis=1)

                    # Calculate the score
                    score = (df['결과'] == 'O').sum()

                    # Show the score and time taken
                    st.write(f'당신의 점수는 {score} / {len(df)} 입니다. 시험에 걸린 시간은 {int(minutes)}분 {int(seconds)}초 입니다.')

                    # Save the dataframe with the results to a new Excel file
                    result_file_name = f'{file_name}_result_{current_date}_{int(minutes)}m_{int(seconds)}s.xlsx'
                    df.to_excel(result_file_name, index=False)
else:
    st.write('기출문제:question: 파일을 :file_folder: 업로드 해주세요.')
