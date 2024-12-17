import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="dark")


def create_brand_prices(df):
    brand_prices_df = df.groupby("Brand")["AskPrice"].mean().reset_index()
    return brand_prices_df


def create_monthly_posts(df):
    return df.resample(rule="D", on="PostedDate").agg({"PostedDate": "value_counts"})


def create_transmission_posts(df):
    return df.groupby("Transmission")["Transmission"].value_counts()


used_car_df = pd.read_csv(
    "https://raw.githubusercontent.com/zildjianvitoo/gdsc-ml-submission/refs/heads/main/assignment-ml/cleaned_dataset.csv?token=GHSAT0AAAAAACUIPAL2GNWKVWFSZ5CND6PEZ3B3MOA"
)

used_car_df["PostedDate"] = pd.to_datetime(used_car_df["PostedDate"])

used_car_df.sort_values(by="PostedDate", inplace=True)
used_car_df.reset_index(inplace=True)


min_date = used_car_df["PostedDate"].min()
max_date = used_car_df["PostedDate"].max()


with st.sidebar:
    st.image(
        "https://cdn1-production-images-kly.akamaized.net/5aMuPPCC_kUtbMuEa6GOANa37g8=/640x360/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/1299773/original/093401300_1469608828-porsche-exclusive-black-911-gt3-rs-for-sale-at-277000_16.jpg"
    )

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = used_car_df[
    (used_car_df["PostedDate"] >= str(start_date))
    & (used_car_df["PostedDate"] <= str(end_date))
]

monthly_posts_df = create_monthly_posts(main_df)
pricing_brand_df = create_brand_prices(main_df)
transmission_posts_df = create_transmission_posts(main_df)

st.header("Post penjualan mobil")
st.subheader("Post bulanan")
(col1,) = st.columns(1)

with col1:
    total_posts = main_df.PostedDate.value_counts().values.sum()
    st.metric("Total post bulanan", value=total_posts)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    main_df["PostedDate"].value_counts().index,
    main_df["PostedDate"].value_counts().values,
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(
    axis="y",
)
ax.tick_params(
    axis="x",
)

st.pyplot(fig)

## Section 2
st.subheader("Brand mobil yang memiliki rata rata harga penjualan tertinggi")
fig, ax = plt.subplots(figsize=(35, 15))


mean_price_by_brand = used_car_df.groupby("Brand")["AskPrice"].mean().reset_index()
top_10_mean_price_by_brand = mean_price_by_brand.nlargest(10, columns="AskPrice")

max_price_brand = top_10_mean_price_by_brand["AskPrice"].idxmax()
colors = [
    "#D3D3D3" if i != max_price_brand else "#90CAF9"
    for i in top_10_mean_price_by_brand.index
]


sns.barplot(
    x="Brand",
    y="AskPrice",
    data=top_10_mean_price_by_brand,
    palette=colors,
)
ax.set_ylabel(None)
ax.set_xlabel("Brand", fontsize=30)
ax.set_title(
    "Brand dengan rata rata harga penjualan tertinggi", loc="center", fontsize=50
)
ax.tick_params(axis="y", labelsize=35)
ax.tick_params(axis="x", labelsize=30)
st.pyplot(fig)

## Section 3
st.subheader("Transmission Automatic vs Transmission Manual")
fig, ax = plt.subplots()
labels = ["Automatic", "Manual"]
ax.pie(
    data=transmission_posts_df,
    autopct="%1.2f%%",
    labels=labels,
    x=transmission_posts_df.values,
    colors=["#D3D3D3", "#90CAF9"],
)
st.pyplot(fig)
