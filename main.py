# Importing the tools
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Setting Randomness & Sample size
np.random.seed(42)
n_records = 200  # creating data for 200 patients

# arrival_times: When Patients arrive
arrival_times = [
    datetime(2026, 9, 1) + timedelta(minutes=int(x))
    for x in np.random.randint(0, 14400, n_records)
]
# wait_mins: How long they wait
# Decide who gets a long wait (25% chance)
is_long_wait = np.random.random(n_records) < 0.25

# Pick unique wait times for each patient
wait_mins = np.where(
    is_long_wait,
    np.random.randint(220, 480, size=n_records),  # If True, 25% long_wait
    np.random.randint(30, 210, size=n_records),  # If False, 75% short wait
)

# departure_times: When patients leave
departure_times = [
    arr + timedelta(minutes=int(w)) for arr, w in zip(arrival_times, wait_mins)
]

# Assebling the full DataFrame
df_raw = pd.DataFrame(
    {
        "Patient_ID": [f"NHS_{1000 + i}" for i in range(n_records)],
        "Site_Name": np.random.choice(
            ["St Marys Hospital", "Charing Cross Hospital", "Hammersmith Hospital"],
            n_records,
        ),
        "Arrival_Timestamp": arrival_times,
        "Departure_Timestamp": departure_times,
        "Wait_Time_Minutes": wait_mins,
        "Acuity_Level": np.random.choice(
            ["Resus", "Majors", "Minors", "Urgent Treatment Centre"],
            n_records,
            p=[0.05, 0.35, 0.40, 0.20],
        ),
        "Disposition": np.random.choice(
            ["Admitted", "Discharged", "Transferred", "Left before seen"],
            n_records,
            p=[0.30, 0.60, 0.05, 0.05],
        ),
    }
)

# Introduce a few dirty data entries (realistic EPR noise)
df_raw.loc[5, "Wait_Time_Minutes"] = -15  # Impossible negative wait
df_raw.loc[12, "Site_Name"] = "St. Marys Hosp"  # Inconsistent naming

# Saving to disk
df_raw.to_csv("a_and_e_raw.csv", index=False)
print("Synthetic Raw Dataset successfully created: 'a_and_e_raw.csv'")
