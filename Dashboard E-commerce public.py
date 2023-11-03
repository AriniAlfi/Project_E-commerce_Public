import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#create_daily_orders_df() digunakan untuk menyiapkan daily_orders_df
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
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
    sum_order_items_df = df.groupby("product_category_name").product_id_x.nunique().sort_values(ascending=False).reset_index()
    return sum_order_items_df

#create__byorderstatus_df() digunakan untuk menyiapkan byorderstatus_df.
def create_byorderstatus_df(df):
    byorderstatus_df = df.groupby(by="order_status").order_id.nunique().reset_index()
    byorderstatus_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return byorderstatus_df

#create_bystate_df() digunakan untuk menyiapkan bystate_df.
def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
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

ecommerce2_df = pd.read_csv("ecommerce2.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
ecommerce2_df.sort_values(by="order_approved_at", inplace=True)
ecommerce2_df.reset_index(inplace=True)
 
for column in datetime_columns:
    ecommerce2_df[column] = pd.to_datetime(ecommerce2_df[column])


min_date = ecommerce2_df["order_approved_at"].min()
max_date = ecommerce2_df["order_approved_at"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/AriniAlfi/e-commerce-public/raw/main/logo-ecommerce.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = ecommerce2_df[(ecommerce2_df["order_approved_at"] >= str(start_date)) & 
                        (ecommerce2_df["order_approved_at"] <= str(end_date))]
    
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
 
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25)
 
st.pyplot(fig)

st.subheader("Best & Worst Performing Category Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 20))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="product_id_x", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Category Product", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="product_id_x", y="product_category_name", data=sum_order_items_df.sort_values(by="product_id_x", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category Product", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
plt.suptitle("Best and Worst Performing Category Product", fontsize=50)
plt.show()
st.pyplot(fig)

st.subheader("Customer Demographics")
 
col1, col2 ,col3 = st.columns(3)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3","#90CAF9","#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="order_count", 
        x="order_status",
        data=byorderstatus_df.sort_values(by="order_status", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Number of Customer by Order Status", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3","#90CAF9"]
 
    sns.barplot(
        y="order_count", 
        x="review_score",
        data=byreviews_df.sort_values(by="review_score", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Number of Customer by Order Reviews", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)
 
with col3:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9"]
    sns.barplot(
        x="customer_count", 
        y="customer_state",
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
