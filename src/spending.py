import pandas as pd
import numpy as np
import random
import json
from datetime import timedelta
import os

# --- Constants ---
TIME_RANGES = {
    'Transport_morning': (6, 9),
    'Transport_evening': (16, 19),
    'Food_lunch': (11, 14),
    'Food_dinner': (19, 21),
    'Drink_lunch': (11, 14),
    'Drink_evening': (18, 22),
    'Entertainment': (17, 23),
    'Shopping': (10, 18),
    'Default': (10, 22)
}

# --- Utilities ---

def load_profiles(filename='profiles.json'):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r') as file:
        profiles = json.load(file)
    return profiles

def generate_days_map(start_date):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_map = {}

    for idx, day in enumerate(weekdays):
        current_date = start_date + pd.Timedelta(days=idx)
        days_map[day] = current_date

    return days_map

def create_spending_entry(day, days_map, category, time_window, amount_range, spend_id):
    random_hour = np.random.randint(time_window[0], time_window[1])
    random_minute = np.random.randint(0, 60)
    random_second = np.random.randint(0, 60)

    timestamp = days_map[day] + timedelta(
        hours=random_hour,
        minutes=random_minute,
        seconds=random_second
    )

    amount = round(np.random.uniform(amount_range[0], amount_range[1]), 2)

    return {
        'SpendID': spend_id,
        'Amount': amount,
        'Category': category,
        'Timestamp': timestamp
    }

# --- Mandatory Spendings ---

def force_mandatory_spendings(day, days_map, amount_ranges, spend_id):
    mandatory = []
    
    if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        mandatory.append(('Transport', TIME_RANGES['Transport_morning']))
        mandatory.append(('Food', TIME_RANGES['Food_lunch']))
        mandatory.append(('Transport', TIME_RANGES['Transport_evening']))

    if day == 'Friday':
        mandatory.append(('Drink', TIME_RANGES['Drink_evening']))

    entries = []
    for category, time_window in mandatory:
        entry = create_spending_entry(
            day, days_map,
            category=category,
            time_window=time_window,
            amount_range=amount_ranges[category],
            spend_id=spend_id
        )
        entries.append(entry)
        spend_id += 1

    return entries, spend_id

# --- Random Spendings ---

def generate_random_spendings(day, days_map, amount_ranges, categories, spend_id, count):
    entries = []

    for _ in range(count):
        category = random.choice(categories)

        if category == 'Transport':
            time_window = TIME_RANGES['Transport_morning']
        elif category == 'Food':
            time_window = random.choice([TIME_RANGES['Food_lunch'], TIME_RANGES['Food_dinner']])
        elif category == 'Drink':
            time_window = random.choice([TIME_RANGES['Drink_lunch'], TIME_RANGES['Drink_evening']])
        else:
            time_window = TIME_RANGES.get(category, TIME_RANGES['Default'])

        entry = create_spending_entry(
            day, days_map,
            category=category,
            time_window=time_window,
            amount_range=amount_ranges[category],
            spend_id=spend_id
        )
        entries.append(entry)
        spend_id += 1

    return entries, spend_id

# --- Main Generator ---

def generate_spending_events(start_date, profile='normal', categories=None):
    profiles = load_profiles()

    if profile not in profiles:
        raise ValueError(f"Profile '{profile}' not found in profiles.json!")

    spending_plan = profiles[profile]['spending_per_day']
    amount_ranges = profiles[profile]['amount_ranges']

    if categories is None:
        categories = list(amount_ranges.keys())

    days_map = generate_days_map(start_date)
    spending_entries = []
    spend_id = 1

    for day, total_spendings in spending_plan.items():
        mandatory_entries, spend_id = force_mandatory_spendings(day, days_map, amount_ranges, spend_id)
        spending_entries.extend(mandatory_entries)

        remaining = total_spendings - len(mandatory_entries)
        if remaining > 0:
            random_entries, spend_id = generate_random_spendings(
                day, days_map, amount_ranges, categories, spend_id, remaining
            )
            spending_entries.extend(random_entries)

    return spending_entries
