#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pylotoncycle import PylotonCycle
import os

USERNAME = "gabrielan2016@gmail.com"
PASSWORD = "Nunez1998!"

peloton = PylotonCycle(USERNAME, PASSWORD)

me = peloton.GetMe()
print("Logged in as:", me.get("username"))

workouts = peloton.GetRecentWorkouts(5)

print("Number of workouts:", len(workouts))

for workout in workouts:
    print(workout.keys())
    print(workout)
    print("-" * 50)


# In[2]:


workouts[0].keys()


# In[3]:


workout = workouts[0]

print(workout["title"])
print(workout["instructor_name"])
print(workout["fitness_discipline"])
print(workout["created_at"])
print(workout["ride"])


# In[4]:


workout["ride"].keys()


# In[5]:


workout = workouts[0]

ride_id = workout["ride"]["id"]
print(ride_id)

url = f"https://members.onepeloton.com/classes/yoga?modal=classDetailsModal&classId={ride_id}"
print(url)


# In[6]:


all_workouts = peloton.GetRecentWorkouts(600)


# In[7]:


disciplines = set(
    w["fitness_discipline"]
    for w in all_workouts
)

print(disciplines)


# In[8]:


yoga = [
    w for w in all_workouts
    if w["fitness_discipline"] == "yoga"
]

print(len(yoga))


# In[17]:


import pandas as pd

rows = []

for w in all_workouts:
    if w.get("fitness_discipline") != "yoga":
        continue

    ride = w.get("ride", {})

    rows.append({
        "class_id": ride.get("id"),
        "title": ride.get("title") or w.get("title"),
        "instructor": w.get("instructor_name"),
        "duration_min": ride.get("duration", 0) // 60,
        "original_air_date": pd.to_datetime(
            ride.get("original_air_time"), unit="s", errors="coerce"
        ).date(),
        "description": ride.get("description"),
        "thumbnail_title": ride.get("thumbnail_title"),
        "difficulty": ride.get("difficulty_rating_avg"),
        "taken_date": pd.to_datetime(w.get("created_at"), unit="s").date(),
        "peloton_url": f"https://members.onepeloton.com/classes/yoga?modal=classDetailsModal&classId={ride.get('id')}",
        "image_url": ride.get("image_url"),
    })
    

df = pd.DataFrame(rows)

summary = (
    df.groupby(
        ["class_id", "title", "instructor", "duration_min", "original_air_date", 
        "description", "peloton_url", "image_url"],
        dropna=False
    )
    .agg(
        times_taken=("taken_date", "count"),
        last_taken=("taken_date", "max"),
        dates_taken=("taken_date", lambda x: ", ".join(str(d) for d in sorted(x)))
    )
    .reset_index()
    .sort_values(["times_taken", "last_taken"], ascending=[False, False])
)

summary["search_text"] = (
    summary["title"].fillna("").astype(str) + " " +
    summary["instructor"].fillna("").astype(str) + " " +
    summary["description"].fillna("").astype(str) + " " +
    summary["duration_min"].fillna("").astype(str) + " " +
    summary["original_air_date"].fillna("").astype(str)
)


# In[18]:


summary.to_csv("peloton_yoga_lookup.csv", index=False)


# In[19]:


summary.sort_values("times_taken", ascending=False).head(20)


# In[20]:


ride_id = workout["ride"]["id"]

url = f"https://members.onepeloton.com/classes/yoga?modal=classDetailsModal&classId={ride_id}"

print(url)


# In[ ]:





# In[ ]:




