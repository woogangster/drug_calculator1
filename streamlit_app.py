# -*- coding: utf-8 -*-
"""
약물 용량 계산기 - Streamlit 웹앱
로컬 실행: streamlit run streamlit_app.py
배포: streamlit.io (Streamlit Community Cloud) - README_배포가이드.md 참고
필요 패키지: streamlit, pandas
"""
import streamlit as st
import pandas as pd
from drug_data import get_drug_names, calculate, DISCLAIMER, DRUGS

st.set_page_config(page_title="약물 용량 계산기", page_icon="💊", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #FFFFFF; }
h1, h2, h3 { color: #1F4E78; }
div.stButton > button {
    background-color: #1F4E78; color: white; border-radius: 10px;
    height: 3em; width: 100%; font-weight: bold; border: none;
}
div.stButton > button:hover { background-color: #163A5C; color: white; }
.result-box {
    background-color: #F5F9FC; border-radius: 14px; padding: 20px;
    border: 1px solid #DCE6F0; color: #1F2D3A; line-height: 1.8; margin-top: 12px;
}
.warning-box {
    background-color: #FFF3E0; border-radius: 10px; padding: 14px;
    border-left: 5px solid #E0A100; margin-top: 10px; color: #7A4E00;
}
.small-note { color: #9AA7B2; font-size: 0.82em; margin-top: 24px; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 💊 약물 용량 계산기")
st.markdown("<p style='color:#5B7A9C;'>소아·노인 맞춤 용량 참고 프로그램 (교육용)</p>", unsafe_allow_html=True)

with st.form("dose_form"):
    drug_name = st.selectbox("약물 선택", get_drug_names())

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("나이 (세)", min_value=0, max_value=120, step=1, value=30)
    with col2:
        weight = st.number_input("체중 (kg)", min_value=0.0, max_value=200.0, step=0.5, value=60.0)

    sex = st.radio("성별", ["남성", "여성"], horizontal=True)

    creatinine = st.number_input(
        "혈청 크레아티닌 (mg/dL) — 선택 입력", min_value=0.0, max_value=15.0, step=0.1, value=0.0
    )
    st.caption("※ 신장기능에 이상이 있다면 크레아티닌 입력을 권장합니다. "
               "신장으로 배설되는 약물은 입력 시 더 정확한 조정값을 제공합니다.")

    submitted = st.form_submit_button("용량 계산하기")

if submitted:
    creat_value = creatinine if creatinine > 0 else None
    sex_code = "F" if sex == "여성" else "M"
    result = calculate(drug_name, int(age), float(weight), creat_value, sex_code)

    lines_html = "<br><br>".join(result["lines"])
    st.markdown(f"<div class='result-box'>{lines_html}</div>", unsafe_allow_html=True)

    for w in result["warnings"]:
        st.markdown(f"<div class='warning-box'>{w}</div>", unsafe_allow_html=True)

st.markdown(f"<p class='small-note'>{DISCLAIMER}</p>", unsafe_allow_html=True)

with st.expander("📋 전체 약물 목록 보기 (분류 · 좁은 치료역 여부)"):
    df = pd.DataFrame(DRUGS)[["name", "eng", "category", "use", "narrow_ti"]].copy()
    df.columns = ["약물명", "성분명", "분류", "용도", "좁은 치료역"]
    df["좁은 치료역"] = df["좁은 치료역"].map({True: "예", False: "아니오"})
    st.dataframe(df, use_container_width=True, hide_index=True)
