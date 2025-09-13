import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("MBTI 유형별 국가별 비율 Top 10")

file_path = "countriesMBTI_16types.csv"

# 기본 파일 읽기 시도
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.success(f"기본 데이터 파일 `{file_path}` 를 불러왔습니다.")
else:
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("업로드한 파일을 불러왔습니다.")
    else:
        st.warning("CSV 파일을 업로드하거나 기본 데이터 파일을 폴더에 두세요.")
        st.stop()

# MBTI 컬럼 탐지
mbti_types = ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP',
              'ESTP','ESFP','ENFP','ENTP','ESTJ','ESFJ','ENFJ','ENTJ']
mbti_cols = [c for c in df.columns if c in mbti_types]

# 결측치 0으로 채우고 정수화
df[mbti_cols] = df[mbti_cols].fillna(0).astype(int)

# 총합 및 비율 계산
df['total'] = df[mbti_cols].sum(axis=1)
for col in mbti_cols:
    df[col + "_ratio"] = df[col] / df['total']

# MBTI 선택
selected_mbti = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

ratio_col = selected_mbti + "_ratio"

# Top 10 국가 추출
top10 = df[['Country', ratio_col]].sort_values(by=ratio_col, ascending=False).head(10)

st.write(f"### {selected_mbti} 비율 Top 10 국가")
st.dataframe(top10)

# Altair 그래프
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(ratio_col, title="비율", axis=alt.Axis(format='%')),
        y=alt.Y('Country', sort='-x', title="국가"),
        tooltip=['Country', alt.Tooltip(ratio_col, format=".2%")]
    )
    .properties(width=600, height=400)
)

st.altair_chart(chart, use_container_width=True)
