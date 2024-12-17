import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 제목
st.title("다양한 데이터 시각화 페이지")

# **1단계: 데이터 업로드**
st.header("1. 데이터 업로드")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

# 데이터 업로드 확인
if uploaded_file:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # **2단계: 시각화 형태 선택**
    st.header("2. 시각화 형태 선택")
    chart_type = st.selectbox("시각화 형태를 선택하세요", 
                              ["막대그래프", "산점도", "히스토그램", "선 그래프", "상관관계 히트맵"])

    # **3단계: 시각화 출력**
    st.header("3. 시각화 결과")
    if chart_type == "막대그래프":
        x_axis = st.selectbox("X축 선택", df.columns)
        y_axis = st.selectbox("Y축 선택", df.columns)
        
        fig, ax = plt.subplots()
        sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax)
        st.pyplot(fig)

    elif chart_type == "산점도":
        x_axis = st.selectbox("X축 선택", df.columns)
        y_axis = st.selectbox("Y축 선택", df.columns)
        hue1=st.selectbox("hue", df.columns)
        fig, ax = plt.subplots()
        sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax,hue=hue1)
        st.pyplot(fig)

    elif chart_type == "히스토그램":
        column = st.selectbox("히스토그램을 그릴 열을 선택하세요", df.columns)
        fig, ax = plt.subplots()
        sns.histplot(df[column], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    elif chart_type == "선 그래프":
        x_axis = st.selectbox("X축 선택", df.columns)
        y_axis = st.selectbox("Y축 선택", df.columns)
        fig, ax = plt.subplots()
        sns.lineplot(x=x_axis, y=y_axis, data=df, ax=ax)
        st.pyplot(fig)

    elif chart_type == "상관관계 히트맵":
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # **4단계: 데이터 분석 요약**
    st.header("4. 데이터 분석 요약")
    st.write("간단한 데이터 통계 요약:")
    st.write(df.describe())
