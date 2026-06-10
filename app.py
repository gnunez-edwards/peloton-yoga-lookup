import pandas as pd
import streamlit as st

st.set_page_config(page_title="Peloton Yoga Lookup", layout="wide")

df = pd.read_csv("peloton_yoga_lookup.csv")

'''
df["last_taken"] = pd.to_datetime(df["last_taken"])
df["original_air_date"] = pd.to_datetime(df["original_air_date"], errors="coerce")
'''

if "days_since_taken" not in df.columns:
    df["days_since_taken"] = (
        pd.Timestamp.today().normalize() - df["last_taken"]
    ).dt.days

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

sort_option = st.selectbox(
    "Sort by",
    [
        "Most repeated",
        "Least recently taken",
        "Most recently taken",
        "Newest class",
        "Oldest class",
    ]
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

if sort_option == "Most repeated":
    results = results.sort_values(["times_taken", "last_taken"], ascending=[False, False])

elif sort_option == "Least recently taken":
    results = results.sort_values("last_taken", ascending=True)

elif sort_option == "Most recently taken":
    results = results.sort_values("last_taken", ascending=False)

elif sort_option == "Newest class":
    results = results.sort_values("original_air_date", ascending=False)

elif sort_option == "Oldest class":
    results = results.sort_values("original_air_date", ascending=True)

for _, row in results.iterrows():
    st.subheader(row["title"])

    if pd.notna(row.get("image_url")):
        st.image(row["image_url"], width=250)

    st.write(f"Instructor: {row['instructor']}")
    st.write(f"Duration: {row['duration_min']} min")
    st.write(f"Original Air Date: {row['original_air_date']}")
    st.write(
        f"Taken {row['times_taken']}x • Last taken {row['last_taken']} "
        f"({row['days_since_taken']} days ago)"
    )
    st.write(f"{len(results)} classes found")

    st.link_button("Open in Peloton", row["peloton_url"])

    with st.expander("Dates Taken"):
        st.write(row["dates_taken"])

    st.divider()
