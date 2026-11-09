"""
SHWASA - Personal Air-Quality Exposure Tracking System
Data Module (Static & Dummy Data for UI Prototype)

This module isolates all mock/dummy data structures and configuration constants
away from the presentation logic, as per modular design principles.
"""

from datetime import datetime, timedelta
import random

# ==============================================================================
# Overview Cards Specification
# ==============================================================================
OVERVIEW_METRICS = {
    "nearby_pm25": {
        "title": "Nearby PM2.5",
        "value": None,             # Reserved empty value as required
        "display_placeholder": "—", # Stylized placeholder
        "unit": "µg/m³",
        "badge": "Ambient Sensor",
        "status": "Awaiting Data Stream",
        "icon": "wind",
    },
    "exposure_so_far": {
        "title": "Exposure So Far",
        "value": None,             # Reserved empty value as required
        "display_placeholder": "—", # Stylized placeholder
        "unit": "µg·h/m³",
        "badge": "Cumulative Dose",
        "status": "Ready to Compute",
        "icon": "activity",
    },
}

# ==============================================================================
# Today's Activity Blocks
# Requirement: Exactly 5 sample activity blocks with start/end/duration 00:00,
# and Indoor/Outdoor classifications.
# ==============================================================================
ACTIVITY_BLOCKS = [
    {
        "id": "block-1",
        "block_label": "Block 1",
        "name": "Morning Commute",
        "start_time": "00:00",
        "end_time": "00:00",
        "duration": "00:00",
        "classification": "Outdoor",
        "category_icon": "car",
    },
    {
        "id": "block-2",
        "block_label": "Block 2",
        "name": "Office Workspace",
        "start_time": "00:00",
        "end_time": "00:00",
        "duration": "00:00",
        "classification": "Indoor",
        "category_icon": "building",
    },
    {
        "id": "block-3",
        "block_label": "Block 3",
        "name": "Park Walk & Lunch",
        "start_time": "00:00",
        "end_time": "00:00",
        "duration": "00:00",
        "classification": "Outdoor",
        "category_icon": "trees",
    },
    {
        "id": "block-4",
        "block_label": "Block 4",
        "name": "Metro Transit",
        "start_time": "00:00",
        "end_time": "00:00",
        "duration": "00:00",
        "classification": "Indoor",
        "category_icon": "train",
    },
    {
        "id": "block-5",
        "block_label": "Block 5",
        "name": "Home Living Area",
        "start_time": "00:00",
        "end_time": "00:00",
        "duration": "00:00",
        "classification": "Indoor",
        "category_icon": "home",
    },
]

# ==============================================================================
# PM2.5 Forecast Sample Data
# 60-minute window with smooth variations
# ==============================================================================
def get_forecast_data(base_time=None):
    """
    Generates sample PM2.5 forecast timeseries data for the next 60 minutes.
    Returns a dictionary of timestamps and PM2.5 concentration values.
    """
    if base_time is None:
        base_time = datetime.now()
    
    # 5-minute intervals across 60 minutes (13 points total)
    timestamps = []
    pm25_values = []
    
    # Aesthetic smooth curve values (µg/m³) simulating realistic ambient fluctuation
    sample_curve = [28.2, 29.5, 31.0, 33.4, 35.8, 37.2, 36.5, 34.1, 31.8, 30.2, 29.0, 27.8, 26.5]
    
    for i, val in enumerate(sample_curve):
        t = base_time + timedelta(minutes=i * 5)
        timestamps.append(t.strftime("%H:%M"))
        pm25_values.append(val)
        
    return {
        "timestamps": timestamps,
        "pm25": pm25_values,
        "is_demo": True,
        "window_duration": "Next 60 Minutes",
    }

