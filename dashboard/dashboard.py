import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta


def penjualan_tertinggi_satu_tahun_terakhir(df):
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    recent_orders = df['order_purchase_timestamp'].max()
    one_year_ago = recent_orders - timedelta(days=365)
    recent_orders = df[df['order_purchase_timestamp'] >= one_year_ago]

    top_categories = recent_orders.groupby('product_category_name')['order_id'].count().sort_values(ascending=False)
    return top_categories

def wilayah_pelanggan_tertinggi(df):
    top_states = all_df['customer_state'].value_counts()
    return top_states

def jumlah_foto_product(df):
    photo_sales_grouped = all_df.groupby('product_photos_qty')['order_id'].count()
    return photo_sales_grouped

def metode_pembayaran(df):
    payment_counts = all_df['payment_type'].value_counts()
    return payment_counts

def prepare_rfm_data(df):
    all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

    rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique", 
        "price": "sum" 
    })

    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    recent_date = all_df["order_purchase_timestamp"].max().date()
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].fillna(pd.Timestamp(recent_date))
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    rfm_df.head().reset_index(drop=True)
    
    return rfm_df

all_df = pd.read_csv('https://raw.githubusercontent.com/asgarindoo/E-commerce_Analysis/refs/heads/main/dashboard/all_data.csv')
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"], errors='coerce')
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("logo.png")
    st.title("Retail Shop")
    st.write("Dashboard analitik penjualan online")

    start_date = st.date_input('Tanggal Mulai', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('Tanggal Akhir', min_value=min_date, max_value=max_date, value=max_date)
    
    if start_date > end_date:
        st.error("Tanggal Mulai tidak boleh lebih besar dari Tanggal Akhir")
    else:
        main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                         (all_df["order_purchase_timestamp"].dt.date <= end_date)]

st.header('📊 Ecommerce Dashboard')
st.subheader('Penjualan Tertinggi dalam 1 Tahun Terakhir')

top_categories = penjualan_tertinggi_satu_tahun_terakhir(main_df)
top_10 = top_categories.head(10)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#79C"] + ["#D3D3D3"] * (len(top_10) - 1)
sns.barplot(x=top_10.values, y=top_10.index, palette=colors, ax=ax, hue=top_10.index, legend=False)
ax.set_ylabel(None)
ax.set_xlabel(None)
st.pyplot(fig)

st.subheader('Wilayah Pelanggan dengan Jumlah Pelanggan Tertinggi')

top_states = wilayah_pelanggan_tertinggi(main_df)
top_five_states = top_states.head(5)

fig, ax = plt.subplots(figsize=(10, 5))
colors = colors[:len(top_five_states)] 
sns.barplot(x=top_five_states.index, y=top_five_states.values, palette=colors, ax=ax, hue=top_five_states.index, legend=False)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

st.subheader('Jumlah Foto Dalam Suatu Product')

photo_sales_grouped = jumlah_foto_product(main_df)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#79C"] + ["#D3D3D3"] * (len(photo_sales_grouped) - 1)
sns.barplot(x=photo_sales_grouped.index, y=photo_sales_grouped.values, palette=colors, ax=ax, hue=photo_sales_grouped.index, legend=False)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

st.subheader('Metode Pembayaran yang Sering Digunakan')
payment_counts =  metode_pembayaran(main_df)
fig, ax = plt.subplots(figsize=(10, 5)) 
ax.pie(
    payment_counts, 
    labels=payment_counts.index, 
    autopct='%1.1f%%', 
    colors=sns.color_palette("pastel"), 
    wedgeprops={'edgecolor': 'white', 'linewidth': 1},
    textprops={'fontsize': 8}
)
st.pyplot(fig)

st.subheader('Pelanggan Terbaik Berdasarkan Parameter RFM (Customer ID)')

rfm_df = prepare_rfm_data(main_df)

top_customers_recency = rfm_df.sort_values("recency", ascending=False).head(10)
top_customers_frequency = rfm_df.sort_values("frequency", ascending=False).head(10)
top_customers_monetary = rfm_df.sort_values("monetary", ascending=False).head(10)

colors = ["#79C"] * 10  

#Grafik Recency
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_customers_recency.index, 
    y="recency",
    data=top_customers_recency, 
    hue=top_customers_recency.index, palette=colors, 
    ax=ax, 
    legend=False
    )
ax.set_ylabel("Recency (Days)", fontsize=14, labelpad=20)
ax.set_xlabel("Customer ID", fontsize=14, labelpad=20)
ax.set_title("By Recency (days)", fontsize=16, pad=20)
st.pyplot(fig)

#Grafik Frequency
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_customers_frequency.index, 
    y=top_customers_frequency["frequency"], 
    palette=colors, 
    ax=ax,
    hue=top_customers_frequency.index,
    legend=False
)
ax.set_ylabel("Frequency", fontsize=14, labelpad=20)
ax.set_xlabel("Customer ID", fontsize=14, labelpad=20)
ax.set_title("By Frequency", fontsize=16, pad=20)
st.pyplot(fig)

#Grafik Monetary
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_customers_monetary.index, 
    y=top_customers_monetary["monetary"], 
    palette=colors, 
    ax=ax,
    hue=top_customers_monetary.index,
    legend=False
)
ax.set_ylabel("Monetary (Revenue)", fontsize=14, labelpad=20)
ax.set_xlabel("Customer ID", fontsize=14, labelpad=20)
ax.set_title("By Monetary", fontsize=16, pad=20)
st.pyplot(fig)