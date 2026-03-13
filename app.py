
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="生产订单数据看板", layout="wide")

st.title("📊 生产 / 订单数据看板（Demo）")
st.markdown("**数据来源：SAP 导出 Excel（示例数据）**")

# 读取数据
df = pd.read_excel("sap_order_demo.xlsx", engine="openpyxl")

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# =============================
# KPI 区域
# =============================
st.subheader("📌 关键指标")

col1, col2, col3, col4 = st.columns(4)

col1.metric("订单总数", df["OrderNo"].nunique())
col2.metric("总数量", int(df["Quantity"].sum()))
col3.metric("物料数", df["Material"].nunique())
col4.metric("工序数", df["Process"].nunique())

# =============================
# 趋势分析
# =============================
st.subheader("📈 订单数量趋势")

daily_qty = df.groupby("OrderDate")["Quantity"].sum().reset_index()
fig_trend = px.line(
    daily_qty,
    x="OrderDate",
    y="Quantity",
    title="按日期统计订单数量"
)
st.plotly_chart(fig_trend, use_container_width=True)

# =============================
# 分布分析
# =============================
st.subheader("📊 产品 / 工序分布")

col5, col6 = st.columns(2)

mat_dist = df.groupby("Material")["Quantity"].sum().reset_index()
fig_mat = px.pie(mat_dist, names="Material", values="Quantity", title="物料占比")
col5.plotly_chart(fig_mat, use_container_width=True)

proc_dist = df.groupby("Process")["Quantity"].sum().reset_index()
fig_proc = px.bar(proc_dist, x="Process", y="Quantity", title="工序数量分布")
col6.plotly_chart(fig_proc, use_container_width=True)

# =============================
# 异常提示
# =============================
st.subheader("⚠️ 异常订单提示")

threshold = 1000
abnormal_df = df[df["Quantity"] > threshold]

if abnormal_df.empty:
    st.success("未发现异常订单")
else:
    st.warning(f"发现 {len(abnormal_df)} 条异常订单（数量 > {threshold}）")
    st.dataframe(abnormal_df)

st.markdown("---")
st.caption("IT 数据看板 Demo | 可扩展至真实 SAP 数据")
