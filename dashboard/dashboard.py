import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./dashboard/bike_merged.csv")

st.title("🚴‍♂️ Dashboard Bike Sharing")

st.markdown("""
Dashboard ini menjawab dua pertanyaan utama:
1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda pada jam sibuk?
2. Pada jam berapa puncak penyewaan terjadi untuk setiap musim, dan bagaimana selisihnya dengan jam terendah?
""")

st.header("1. Pengaruh Cuaca terhadap Penyewaan Sepeda di Jam Sibuk")

rush_hours = st.multiselect(
    "Pilih jam sibuk:",
    options=list(range(24)),
    default=[7, 8, 9, 16, 17, 18, 19]
)

rush_data = df[df["hr"].isin(rush_hours)]

weather_options = {
    1: "Cerah / Berawan Ringan",
    2: "Mendung / Berkabut",
    3: "Hujan / Salju Ringan",
    4: "Hujan Deras / Badai"
}
selected_weather = st.multiselect(
    "Pilih kondisi cuaca:",
    options=list(weather_options.keys()),
    format_func=lambda x: weather_options[x],
    default=[1, 2, 3]
)

filtered_weather = rush_data[rush_data["weathersit"].isin(selected_weather)]

weather_group = filtered_weather.groupby("weathersit")["cnt"].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(x="weathersit", y="cnt", data=weather_group, palette="pastel", ax=ax1)
ax1.set_xlabel("Kondisi Cuaca")
ax1.set_ylabel("Rata-rata Penyewaan di Jam Sibuk")
ax1.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda di Jam Sibuk")
ax1.set_xticklabels([weather_options[w] for w in weather_group["weathersit"]])
st.pyplot(fig1)

st.header("2. Pola Penyewaan Sepeda per Jam untuk Tiap Musim")

season_options = {
    1: "Semi",
    2: "Panas",
    3: "Gugur",
    4: "Dingin"
}
selected_season = st.multiselect(
    "Pilih musim:",
    options=list(season_options.keys()),
    format_func=lambda x: season_options[x],
    default=[1, 2, 3, 4]
)

season_group = df[df["season"].isin(selected_season)]
season_group = season_group.groupby(["season", "hr"])["cnt"].mean().reset_index()

season_colors = {
    1: "blue",    
    2: "orange",  
    3: "green",   
    4: "red"      
}

fig2, ax2 = plt.subplots()
for s in selected_season:
    subset = season_group[season_group["season"] == s]
    ax2.plot(
        subset["hr"], subset["cnt"],
        label=season_options[s],
        color=season_colors[s]
    )

ax2.set_xlabel("Jam")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_title("Pola Penyewaan Sepeda per Jam")
ax2.legend(title="Musim")

st.pyplot(fig2)

st.markdown("""
**Interpretasi cepat**:  
- Cuaca cerah → paling banyak digunakan.  
- Musim gugur → puncak penyewaan tertinggi (terutama sore hari).  
- Musim dingin → penyewaan terendah.  
""")