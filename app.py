import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")
st.title("Retail Sales Analytics Dashboard")
st.caption("Portfolio project | Python • Pandas • Matplotlib • Streamlit")
st.info("The included dataset is synthetic sample data created for learning; it is not real company performance.")

@st.cache_data
def load_data():
    return pd.read_csv("retail_sales.csv", parse_dates=["date"])

df = load_data()
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df.region.unique()), default=sorted(df.region.unique()))
categories = st.sidebar.multiselect("Category", sorted(df.category.unique()), default=sorted(df.category.unique()))
dates = st.sidebar.date_input("Date range", value=(df.date.min().date(), df.date.max().date()))
data = df[df.region.isin(regions) & df.category.isin(categories)].copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    data = data[(data.date >= pd.to_datetime(dates[0])) & (data.date <= pd.to_datetime(dates[1]))]
if data.empty:
    st.warning("No data matches these filters.")
    st.stop()

revenue, profit, units = data.revenue_inr.sum(), data.profit_inr.sum(), data.units_sold.sum()
margin = profit / revenue * 100 if revenue else 0
a,b,c,d = st.columns(4)
a.metric("Revenue", f"₹{revenue:,.0f}")
b.metric("Profit", f"₹{profit:,.0f}")
c.metric("Units sold", f"{units:,}")
d.metric("Profit margin", f"{margin:.1f}%")

st.subheader("Monthly revenue")
monthly = data.assign(month=data.date.dt.to_period("M").astype(str)).groupby("month").revenue_inr.sum()
fig, ax = plt.subplots()
monthly.plot(marker="o", ax=ax)
ax.set_ylabel("Revenue (₹)"); ax.set_xlabel("Month"); fig.tight_layout()
st.pyplot(fig); plt.close(fig)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by category")
    fig, ax = plt.subplots()
    data.groupby("category").revenue_inr.sum().sort_values(ascending=False).plot(kind="bar", ax=ax)
    ax.set_ylabel("Revenue (₹)"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
with right:
    st.subheader("Profit by region")
    fig, ax = plt.subplots()
    data.groupby("region").profit_inr.sum().sort_values(ascending=False).plot(kind="bar", ax=ax)
    ax.set_ylabel("Profit (₹)"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)

st.subheader("Product performance")
summary = data.groupby("product", as_index=False).agg(units_sold=("units_sold","sum"), revenue_inr=("revenue_inr","sum"), profit_inr=("profit_inr","sum")).sort_values("revenue_inr", ascending=False)
st.dataframe(summary, use_container_width=True, hide_index=True)
st.subheader("Filtered records")
st.dataframe(data, use_container_width=True, hide_index=True)
st.download_button("Download filtered CSV", data.to_csv(index=False).encode(), "filtered_retail_sales.csv", "text/csv")
