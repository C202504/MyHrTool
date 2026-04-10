import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

st.set_page_config(page_title="特簽人員年資計算與表單系統", page_icon="📝", layout="wide")

st.title("📝 特簽人員年資計算與表單系統")
st.write("輸入各段經歷說明與日期，系統將自動彙整成表單並計算總年資。")

# 初始化經歷清單，將預設值設為 None
if 'exp_list' not in st.session_state:
    st.session_state.exp_list = [{"label": "", "start": None, "end": None}]

# --- 功能按鈕 ---
col_btn, _ = st.columns([1, 4])
with col_btn:
    if st.button("➕ 新增一筆經歷"):
        st.session_state.exp_list.append({"label": "", "start": None, "end": None})

st.divider()

# --- 經歷輸入區 ---
data_for_table = []
total_all_days = 0

for idx, exp in enumerate(st.session_state.exp_list):
    c1, c2, c3, c4 = st.columns([3, 3, 3, 1])
    
    with c1:
        st.session_state.exp_list[idx]["label"] = st.text_input(
            f"經歷 {idx+1} 說明", value=exp["label"], key=f"label_{idx}", placeholder="例如：XX公司"
        )
    with c2:
        # 將 value 設為 exp["start"]，預設會是 None
        st.session_state.exp_list[idx]["start"] = st.date_input(
            "起始日期", value=exp["start"], min_value=date(1911, 1, 1), max_value=date(2050, 12, 31), key=f"s_{idx}"
        )
    with c3:
        # 將 value 設為 exp["end"]，預設會是 None
        st.session_state.exp_list[idx]["end"] = st.date_input(
            "迄止日期", value=exp["end"], min_value=date(1911, 1, 1), max_value=date(2050, 12, 31), key=f"e_{idx}"
        )
    with c4:
        st.write("##")
        if st.button("🗑️", key=f"del_{idx}"):
            st.session_state.exp_list.pop(idx)
            st.rerun()

    # 計算邏輯：只有當兩個日期都填寫了，才進行計算
    s = st.session_state.exp_list[idx]["start"]
    e = st.session_state.exp_list[idx]["end"]
    label = st.session_state.exp_list[idx]["label"]
    
    if s is not None and e is not None:
        if s <= e:
            duration = (e - s).days + 1
            total_all_days += duration
            d_diff = relativedelta(e + relativedelta(days=1), s)
            duration_text = f"{d_diff.years}年{d_diff.months}月{d_diff.days}天"
            
            data_for_table.append({
                "經歷說明": label if label else f"經歷 {idx+1}",
                "起始日期": s.strftime("%Y-%m-%d"),
                "迄止日期": e.strftime("%Y-%m-%d"),
                "年資(小計)": duration_text,
                "總天數": duration
            })
        else:
            st.error(f"⚠️ 經歷 {idx+1} 的日期順序有誤")

st.divider()

# --- 總結果顯示 ---
if data_for_table:
    # (這部分維持不變，與之前相同)
    st.header("📋 經歷年資彙整表單")
    df = pd.DataFrame(data_for_table)
    st.table(df)

    base = date(2000, 1, 1)
    target = base + relativedelta(days=total_all_days)
    final_diff = relativedelta(target, base)

    st.subheader("📊 總計年資摘要")
    res1, res2, res3 = st.columns(3)
    res1.metric("累計年數", f"{final_diff.years} 年")
    res2.metric("累計月數", f"{final_diff.months} 月")
    res3.metric("累計天數", f"{final_diff.days} 天")
    
    st.success(f"🎊 所有經歷總計為：**{final_diff.years} 年 {final_diff.months} 月 {final_diff.days} 天**")
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="📥 下載經歷表單 (CSV)", data=csv, file_name=f"年資表單_{date.today()}.csv", mime="text/csv")
else:
    # 如果還沒填完日期，顯示提示
    st.info("💡 請填寫上方的「起始日期」與「迄止日期」以進行計算。")