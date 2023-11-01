import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#create_daily_orders_df() digunakan untuk menyiapkan daily_orders_df
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='Order_approved_date').agg({
        "order_id": "nunique",
        "revenue": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    
    return daily_orders_df

#create_sum_order_items_df() bertanggung jawab untuk menyiapkan sum_orders__category_ items_df.
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

#create__byorderstatus_df() digunakan untuk menyiapkan byorderstatus_df.
def create_byorderstatus_df(df):
    byorderstatus_df = df.groupby(by="Order_status").Customer_id.nunique().reset_index()
    byorderstatus_df.rename(columns={
        "Customer_id": "customer_count"
    }, inplace=True)
    
    return byorderstatus_df

#create_bystate_df() digunakan untuk menyiapkan bystate_df.
def create_bystate_df(df):
    bystate_df = df.groupby(by="Customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

#create_byreviews_df() digunakan untuk menyiapkan byreviews_df.
def create_byreviews_df(df):
    byreviews_df = df.groupby(by="review_score").order_id.nunique().reset_index()
    byreviews_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return byreviews_df

all1_df = pd.read_csv("all1_data.csv")

datetime_columns = ["order_approved_date", "order_delivered_customer_date"]
all1_df.sort_values(by="order_approved_date", inplace=True)
all1_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all1_df[column] = pd.to_datetime(all1_df[column])


min_date = all1_df["order_approved_date"].min()
max_date = all1_df["order_approved_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/AriniAlfi/logo-e-commerce-public/blob/8bb9dabf896e2b6aad16fb636df0c83876bcf16a/README.md")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all1_df[(all1_df["order_approved_date"] >= str(start_date)) & 
                (all1_df["order_approved_date"] <= str(end_date))]
    
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
byorderstatus_df = create_byorderstatus_df(main_df)
bystate_df = create_bystate_df(main_df)
byreviews_df = create_byreviews_df(main_df)


st.header('E-commerce Public Dashboard :sparkles:')

st.subheader('Daily Orders')

 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_date"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Best & Worst Performing Category Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="product_id", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Category Product", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="product_id", y="product_category_name", data=sum_order_items_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category Product", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
plt.suptitle("Best and Worst Performing Category Product", fontsize=20)
plt.show()
st.pyplot(fig)

st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="customer_count", 
        x="order_status",
        data=bystate_df.sort_values(by="order_status", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Order Status", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="order_count", 
        x="order_review",
        data=byorderstatus_df.sort_values(by="order_review", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Order Reviews", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
 
st.caption('Copyright (c) Dicoding 2023')