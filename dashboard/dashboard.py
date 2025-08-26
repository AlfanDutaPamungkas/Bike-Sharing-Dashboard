import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./dashboard/bike_merged.csv")

st.title("🚴‍♂️ Dashboard Bike Sharing")

st.markdown("""
Dashboard ini menjawab dua pertanyaan utama:
1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda pada jam sibuk?
2. Bagaimana pola penyewaan sepeda bervariasi sepanjang jam operasional di setiap musim, dan apa perbedaan signifikan antara jam puncak dan jam terendah?
""")

st.header("1. Pengaruh Cuaca terhadap Penyewaan Sepeda di Jam Sibuk")

filter_mode_hours = st.radio(
    "Pilih mode filter jam:",
    ["Single", "Multi"],
    horizontal=True
)

rush_hours_options = list(range(24))
peak_hours = [7, 8, 9, 16, 17, 18, 19]

if filter_mode_hours == "Single":
    selected_hour = st.selectbox(
        "Pilih jam sibuk:",
        options=["All", "Peak Hours"] + rush_hours_options,
        index=0
    )
    if selected_hour == "All":
        rush_data = df
    elif selected_hour == "Peak Hours":
        rush_data = df[df["hr"].isin(peak_hours)]
    else:
        rush_data = df[df["hr"] == selected_hour]
else:
    selected_hours = st.multiselect(
        "Pilih jam sibuk:",
        options=["Peak Hours"] + rush_hours_options,
        default=["Peak Hours"]
    )
    if "Peak Hours" in selected_hours:
        selected = peak_hours + [h for h in selected_hours if isinstance(h, int)]
        rush_data = df[df["hr"].isin(selected)]
    else:
        rush_data = df[df["hr"].isin(selected_hours)]

filter_mode_weather = st.radio(
    "Pilih mode filter cuaca:",
    ["Single", "Multi"],
    horizontal=True
)

weather_options = {
    1: "Cerah / Berawan Ringan",
    2: "Mendung / Berkabut",
    3: "Hujan / Salju Ringan",
    4: "Hujan Deras / Badai"
}

if filter_mode_weather == "Single":
    selected_weather = st.selectbox(
        "Pilih kondisi cuaca:",
        options=["All"] + list(weather_options.keys()),
        format_func=lambda x: "Semua Cuaca" if x == "All" else weather_options[x]
    )
    if selected_weather == "All":
        filtered_weather = rush_data
    else:
        filtered_weather = rush_data[rush_data["weathersit"] == selected_weather]
else:
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

st.header("2. Bagaimana pola penyewaan sepeda bervariasi sepanjang jam operasional di setiap musim?")

filter_mode_season = st.radio(
    "Pilih mode filter musim:",
    ["Single", "Multi"],
    horizontal=True
)

season_options = {
    1: "Semi",
    2: "Panas",
    3: "Gugur",
    4: "Dingin"
}

if filter_mode_season == "Single":
    selected_season = st.selectbox(
        "Pilih musim:",
        options=["All"] + list(season_options.keys()),
        format_func=lambda x: "Semua Musim" if x == "All" else season_options[x]
    )
    if selected_season == "All":
        season_filter = df
        selected_seasons = list(season_options.keys())
    else:
        season_filter = df[df["season"] == selected_season]
        selected_seasons = [selected_season]
else:
    selected_seasons = st.multiselect(
        "Pilih musim:",
        options=list(season_options.keys()),
        format_func=lambda x: season_options[x],
        default=[1, 2, 3, 4]
    )
    season_filter = df[df["season"].isin(selected_seasons)]

season_group = season_filter.groupby(["season", "hr"])["cnt"].mean().reset_index()

season_colors = {
    1: "blue",
    2: "orange",
    3: "green",
    4: "red"
}

fig2, ax2 = plt.subplots()
for s in selected_seasons:
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
