import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

def generate_data():
    park_num = np.random.randint(0, 4, 100)
    data = pd.DataFrame({
        "day": np.random.randint(0, 100, 100),
        "q": np.random.randint(0, 100, 100),
        "lat": [PARK[i][0] for i in park_num],
        "lon": [PARK[i][1] for i in park_num],
    })
    return data

PARK = [(36.571793, 139.885830), (36.511552, 139.860848), (36.492484, 139.920624), (36.587084, 139.879134)]

if __name__ == '__main__':

    # Overview
    st.title("Garbage Distribution in Tochigi")
    
    # Load data
    data= generate_data()
    
    # Set widget
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": PARK[0][0],
            "longitude": PARK[0][1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    ))

    # Plot by Altair
    st.altair_chart(alt.Chart(data)
        .mark_bar().encode(
            x=alt.X("day:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("q:Q"),
            tooltip=['day', 'q']
        ), use_container_width=True)

    if st.checkbox("Show raw data", False):
        st.write(data)