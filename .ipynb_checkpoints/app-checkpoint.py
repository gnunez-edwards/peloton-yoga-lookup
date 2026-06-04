import pandas as pd
import streamlit as st

st.set_page_config(page_title="Peloton Yoga Lookup", layout="wide")

df = pd.read_csv("peloton_yoga_lookup.csv")

df["last_taken"] = pd.to_datetime(df["last_taken"])
df["original_air_date"] = pd.to_datetime(df["original_air_date"], errors="coerce")

df["last_taken_display"] = df["last_taken"].dt.strftime("%m/%d/%Y")
df["original_air_date_display"] = df["original_air_date"].dt.strftime("%m/%d/%Y")

if "days_since_taken" not in df.columns:
    df["days_since_taken"] = (
        pd.Timestamp.today().normalize() - df["last_taken"]
    ).dt.days

st.title("Peloton Yoga Lookup")

search = st.text_input(
    "Search by title, instructor, duration, air date, or description"
)

duration_filter = st.multiselect(
    "Duration",
    sorted(df["duration_min"].dropna().unique())
)

instructor_filter = st.multiselect(
    "Instructor",
    sorted(df["instructor"].dropna().unique())
)

results = df.copy()

if search:
    mask = results["search_text"].str.contains(
        search,
        case=False,
        na=False
    )
    results = results[mask]

if duration_filter:
    results = results[results["duration_min"].isin(duration_filter)]

if instructor_filter:
    results = results[results["instructor"].isin(instructor_filter)]

results = results.sort_values(
    ["times_taken", "last_taken"],
    ascending=[False, False]
)

st.subheader("Rediscover")

min_days = st.slider(
    "Only show classes I have not taken in at least this many days",
    min_value=0,
    max_value=365,
    value=60
)

rediscover = results[results["days_since_taken"] >= min_days]

if st.button("Pick a class for me"):
    if rediscover.empty:
        st.warning("No classes match that rediscovery filter.")
    else:
        pick = rediscover.sample(1).iloc[0]

        st.success("Today's rediscovered class")

        if pd.notna(pick.get("image_url")):
            st.image(pick["image_url"], width=250)

        st.write(f"{pick['title']}")
        st.write(f"Instructor: {pick['instructor']}")
        st.write(f"Duration: {pick['duration_min']} min")
        st.write(f"Taken {pick['times_taken']}x")
        st.write(
            f"Last taken {pick['last_taken_display']} "
            f"({pick['days_since_taken']} days ago)"
        )

        st.link_button("Open this class", pick["peloton_url"])

st.divider()

for _, row in results.iterrows():
    st.subheader(row["title"])

    if pd.notna(row.get("image_url")):
        st.image(row["image_url"], width=250)

    st.write(f"Instructor: {row['instructor']}")
    st.write(f"Duration: {row['duration_min']} min")
    st.write(f"Original Air Date: {row['original_air_date_display']}")
    st.write(
        f"Taken {row['times_taken']}x • Last taken {row['last_taken_display']} "
        f"({row['days_since_taken']} days ago)"
    )

    st.link_button("Open in Peloton", row["peloton_url"])

    with st.expander("Dates Taken"):
        st.write(row["dates_taken"])

    st.divider()