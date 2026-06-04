import pandas as pd
import streamlit as st

st.set_page_config(page_title="Peloton Yoga Lookup", layout="wide")

df = pd.read_csv("peloton_yoga_lookup.csv")

st.title("Peloton Yoga Lookup")

search_cols = [
    "title",
    "instructor",
    "duration_min",
    "original_air_date",
    "description"
]

search = st.text_input(
    "Search by title, instructor, duration, air date, or description"
)

if search:
    mask = df["search_text"].str.contains(
        search,
        case=False,
        na=False
    )

    results = df[mask].sort_values(
        ["times_taken", "last_taken"],
        ascending=[False, False]
    )
else:
    results = df.sort_values(
        ["times_taken", "last_taken"],
        ascending=[False, False]
    )

results = df[mask]

for _, row in results.iterrows():
    st.subheader(row["title"])

    st.write(f"Instructor: {row['instructor']}")
    st.write(f"Taken: {row['times_taken']}x")
    st.write(f"Last Taken: {row['last_taken']}")
    st.write(f"Duration: {row['duration_min']} min")
    st.write(f"Original Air Date: {row['original_air_date']}")
    
    if pd.notna(row.get("image_url")):
        st.image(row["image_url"], width=250)

    st.link_button("Open in Peloton", row["peloton_url"])

    with st.expander("Dates Taken"):
        st.write(row["dates_taken"])

    st.divider()
    