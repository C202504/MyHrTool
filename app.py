import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

# ==========================================
# 版本標記 (Version Stamp)
# 更新時間：2026-04-24 16:15
# ==========================================

# 1. 歷年調薪基準大數據 (1999-2025)
HISTORY_SALARY_DATA = {
    1999: {"基層人員": 1100, "基層主管": 1500, "二級主管": 1700, "一級主管": 2300},
    2000: {"基層人員": 2100, "基層主管": 2800, "二級主管": 3300, "一級主管": 4500},
    2001: {"基層人員": 560, "基層主管": 0, "二級主管": 0, "一級主管": 0},
    2002: {"基層人員": 790, "基層主管": 1050, "二級主管": 1350, "一級主管": 1900},
    2003: {"基層人員": 1300, "基層主管": 1700, "二級主管": 2200, "一級主管": 3000},
    2004: {"基層人員": 1500, "基層主管": 1900, "二級主管": 2200, "一級主管": 2900},
    2005: {"基層人員": 1250, "基層主管": 1500, "二級主管": 1800, "一級主管": 2300},
    2006: {"基層人員": 1075, "基層主管": 1350, "二級主管": 1600, "一級主管": 2000},
    2007: {"基層人員": 1140, "基層主管": 1360, "二級主管": 1600, "一級主管": 2000},
    2008: {"基層人員": 1165, "基層主管": 1385, "二級主管": 1670, "一級主管": 2150},
    2009: {"基層人員": 0, "基層主管": 0, "二級主管": 0, "一級主管": 0},
    2010: {"基層人員": 1385, "基層主管": 1635, "二級主管": 1960, "一級主管": 2500},
    2011: {"基層人員": 1660, "基層主管": 1960, "二級主管": 2340, "一級主管": 3050},
    2012: {"基層人員": 940, "基層主管": 1140, "二級主管": 1360, "一級主管": 1780},
    2013: {"基層人員": 1200, "基層主管": 1430, "二級主管": 1700, "一級主管": 2200},
    2014: {"基層人員": 1320, "基層主管": 1570, "二級主管": 1900, "一級主管": 2400},
    2015: {"基層人員": 1120, "基層主管": 1450, "二級主管": 1900, "一級主管": 2600},
    2016: {"基層人員": 1770, "基層主管": 2120, "二級主管": 2570, "一級主管": 3250},
    2017: {"基層人員": 2000, "基層主管": 2410, "二級主管": 2920, "一級主管": 3680},
    2018: {"基層人員": 2100, "基層主管": 2550, "二級主管": 3100, "一級主管": 3880},
    2019: {"基層人員": 1800, "基層主管": 2180, "二級主管": 2640, "一級主管": 3330},
    2020: {"基層人員": 550, "基層主管": 810, "二級主管": 900, "一級主管": 1000},
    2021: {"基層人員": 2100, "基層主管": 2690, "二級主管": 3060, "一級主管": 3810},
    2022: {"基層人員": 2490, "基層主管": 3190, "二級主管": 3650, "一級主管": 4550},
    2023: {"基層人員": 1410, "基層主管": 1880, "二級主管": 2030, "一級主管": 2580},
    2024: {"基層人員": 1740, "基層主管": 2250, "二級主管": 2470, "一級主管": 3100},
    2025: {"基層人員": 1190, "基層主管": 1560, "二級主管": 1610, "一級主管": 2040},
}

FIRST_YEAR_H1_DATA = {
    1999: 900, 2000: 1700, 2001: 380, 2002: 560, 2003: 950,
    2004: 1200, 2005: 1000, 2006: 850, 2007: 900, 2008: 950,
    2009: 0, 2010: 1100, 2011: 1350, 2012: 750, 2013: 960,
    2014: 1060, 2015: 900, 2016: 1400, 2017: 1600, 2018: 1700,
    2019: 1440, 2020: 0, 2021: 1650
}

st.set_page_config(page_title="特簽人員核薪試算系統", page_icon="📝", layout="wide")

st.markdown("""<style>.notranslate { translate: no !important; } @media print { .stButton, .stDownloadButton, footer, header { display: none !important; } .stMain { padding: 0 !important; } }</style>""", unsafe_allow_html=True)

st.title("📝 特簽人員任用核薪試算系統 ")

with st.container():
    st.info("""📢 **重要注意事項**：
1. 版本-26.04.24.11。
2. 目前尚無人民幣功能。
3. 此為相關作業人員使用，請勿轉傳。
4. 新進起薪：請自行針對個案狀況進行修改。
5. 調薪基準：歷年1999-2025； 上半年到職1999-2021。""")

st.divider()

# --- 基本資料 ---
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("姓名 *", placeholder="請輸入姓名")
        school = st.text_input("畢業學校 *")
        major = st.text_input("畢業科系 *")
    with c2:
        edu = st.selectbox("學歷 *", ["請選擇學歷", "私專", "學士", "碩士", "博士"], index=0)
        target_pos = st.selectbox("擬擔任職位 *", ["基層人員", "基層主管", "二級主管", "一級主管"], index=1)
        arrival_date = st.date_input("預定到職日 *", value=date.today())
    with c3:
        currency = st.radio("選擇幣別", ["台幣 (TWD)", "人民幣 (RMB)"], horizontal=True)
        symbol = "NT$" if "台幣" in currency else "¥"
        base_salary_origin = st.number_input(f"新進起薪 (A) *", value=30000, step=100)
        discount_rate = st.slider("調薪核給折數 (%)", 0, 100, 90, 5)

st.divider()

# --- 專業經歷 ---
if 'exp_list' not in st.session_state: st.session_state.exp_list = []
if st.button("➕ 新增一筆經歷"): st.session_state.exp_list.append({"label": "", "start": None, "end": None})

total_days = 0
global_error = False
today_dt = date.today()

for idx, exp in enumerate(st.session_state.exp_list):
    with st.container(border=True):
        col_name, col_start, col_end, col_del = st.columns([3, 3, 3, 1])
        with col_name: st.session_state.exp_list[idx]["label"] = st.text_input(f"經歷 {idx+1}", value=exp["label"], key=f"lab_{idx}")
        with col_start: st.session_state.exp_list[idx]["start"] = st.date_input("起始日", value=exp["start"], min_value=date(1911,1,1), key=f"s_{idx}")
        with col_end: st.session_state.exp_list[idx]["end"] = st.date_input("迄止日", value=exp["end"], min_value=date(1911,1,1), max_value=today_dt, key=f"e_{idx}")
        if st.session_state.exp_list[idx]["start"] and st.session_state.exp_list[idx]["end"]:
            if st.session_state.exp_list[idx]["end"] < st.session_state.exp_list[idx]["start"]:
                st.error("迄止日不可早於起始日"); global_error = True
            else: total_days += (st.session_state.exp_list[idx]["end"] - st.session_state.exp_list[idx]["start"]).days + 1
        with col_del: 
            st.write("##")
            if st.button("🗑️", key=f"del_{idx}"): st.session_state.exp_list.pop(idx); st.rerun()

if total_days > 0 and not global_error:
    base_d = date(2000, 1, 1)
    diff = relativedelta(base_d + relativedelta(days=total_days), base_d)
    calc_years = diff.years 
    entry_back = arrival_date - relativedelta(years=diff.years, months=diff.months, days=diff.days)
    with st.container(border=True):
        cr1, cr2 = st.columns(2)
        with cr1: st.metric("認定總工作年資", f"{diff.years} 年 {diff.months} 月 {diff.days} 天")
        with cr2: st.date_input("系統回算入職日", value=entry_back, disabled=True)
else:
    calc_years, entry_back = 0, None

# --- 核薪試算 ---
if all([name.strip() != "", school.strip() != "", total_days > 0, not global_error]):
    st.divider()
    st.header(f"💹 歷年調薪與核定本薪")
    total_adj = 0
    start_year = entry_back.year
    for yr in range(start_year, arrival_date.year + 1):
        idx_yr = yr - start_year
        cy1, cy2, cy3 = st.columns([2, 4, 4])
        with cy1: st.write(f"### {yr} 年")
        with cy2:
            if idx_yr == 0: p = st.selectbox(f"{yr} 職位", ["基層人員"], index=0, key=f"pos_{yr}", disabled=True)
            else: p = st.selectbox(f"{yr} 職位", ["基層人員", "基層主管", "二級主管", "一級主管"], index=["基層人員", "基層主管", "二級主管", "一級主管"].index(target_pos), key=f"pos_{yr}")
        with cy3:
            if idx_yr == 0:
                if entry_back.month < 7:
                    val = FIRST_YEAR_H1_DATA.get(yr, HISTORY_SALARY_DATA.get(yr, {}).get("基層人員", 0))
                    st.caption(f"💡 {entry_back.month}月到職(上半年)")
                else:
                    val = 0
                    st.caption(f"💡 {entry_back.month}月到職(下半年)")
            else:
                val = HISTORY_SALARY_DATA.get(yr, {}).get(p, 0)
            amt = st.number_input(f"{yr} 調薪金額", value=int(val), key=f"amt_{yr}_{p}")
        total_adj += amt

    discounted_adj = round(total_adj * (discount_rate / 100))
    suggested = base_salary_origin + discounted_adj
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        with st.container(border=True):
            st.write(f"基礎起薪(A): {symbol} {base_salary_origin:,}")
            st.write(f"歷年調薪合計(B): {symbol} {total_adj:,}")
            st.write(f"核給折數: {discount_rate}%")
            st.info(f"系統建議本薪: **{symbol} {suggested:,}**")
    with c_s2: final_base = st.number_input(f"最終核給本薪 ({symbol})", value=int(suggested), step=100)

    # --- 年薪試算 ---
    st.divider(); st.header("💰 年薪試算")
    is_lv1 = target_pos == "一級主管"
    p_label = "經營津貼" if is_lv1 else "效率獎金"
    b_label = "主管獎勵金" if target_pos in ["一級主管", "二級主管"] else "節慶獎金"
    
    if target_pos == "一級主管": d_bonus, d_p_base, d_u_pay, d_y_mo = 950000, 1.0, 6000, 3.0
    elif target_pos == "二級主管": d_bonus, d_p_base, d_u_pay, d_y_mo = 390000, 4.0, 3000, 3.0
    elif target_pos == "基層主管": d_bonus, d_p_base, d_u_pay, d_y_mo = 22500, 3.2, 3000, 3.0
    else: d_bonus, d_p_base, d_u_pay, d_y_mo = 22500, 2.7, 3000, 3.0

    with st.container(border=True):
        st.subheader("📌 參數手動輸入")
        i0, i1, i2, i3, i4 = st.columns(5)
        with i0: st.text_input("職等、級", value="8.2")
        with i1: p_base = st.number_input("效獎基數", value=float(d_p_base), step=0.1)
        with i2: p_pay = st.number_input(f"每基數{p_label}", value=int(d_u_pay), step=100)
        with i3: yr_mo = st.number_input("年獎月數", value=float(d_y_mo), step=0.5)
        with i4: fest_val = st.number_input(b_label, value=int(d_bonus), step=1000)
        
        p_bonus_val = int(round(p_pay * p_base, 0))
        mo_total = final_base + p_bonus_val + 2400 + 1430 + 4000
        suggested_yr_total = (mo_total * 12) + final_base + int(round(final_base * yr_mo, 0)) + fest_val

        st.write("📊 **年薪構成明細表**")
        res_df = pd.DataFrame({
            "項目": ["核給本薪", p_label, "伙食津貼", "交通津貼", "作業用品代金", "月薪合計", "勤勉獎金", "年終獎金", b_label, "預估年薪總計(核定)"],
            "金額": [f"{symbol} {final_base:,}", f"{symbol} {p_bonus_val:,}", f"{symbol} 2,400", f"{symbol} 1,430", f"{symbol} 4,000", f"{symbol} {mo_total:,}", f"{symbol} {final_base:,}", f"{symbol} {int(round(final_base*yr_mo,0)):,}", f"{symbol} {fest_val:,}", f"{symbol} {int(round(suggested_yr_total,0)):,}"]
        })
        
        def draw(df):
            h = '<table style="width:100%; border-collapse: collapse; font-family: sans-serif;">'
            h += '<tr style="background-color: #f0f2f6;"><th style="padding:10px; border:1px solid #ddd;">項目</th><th style="padding:10px; border:1px solid #ddd;">金額</th></tr>'
            for _, r in df.iterrows():
                is_target = r["項目"] in ["月薪合計", "預估年薪總計(核定)"]
                style = 'style="background-color: #FFFACD; font-weight: bold;"' if is_target else ""
                h += f'<tr {style}><td style="padding:10px; border:1px solid #ddd;">{r["項目"]}</td><td style="padding:10px; border:1px solid #ddd;">{r["金額"]}</td></tr>'
            h += '</table>'
            return h

        st.markdown(draw(res_df), unsafe_allow_html=True)
        st.write("---")
        final_yr_total = st.number_input(f"預估年薪總計 ({symbol}) - 可手動調整", value=int(round(suggested_yr_total, 0)), step=1000)
        st.success(f"### 👉 最終核薪總覽： {symbol} {final_yr_total:,}")

    # --- 按鈕 ---
    st.divider(); cp1, cp2 = st.columns(2)
    with cp1:
        if st.button("🖨️ 列印/存成 PDF 試算表"): st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 500);</script>", height=0)
    with cp2:
        csv = res_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載數據 CSV", csv, f"核薪試算_{name}.csv", "text/csv")