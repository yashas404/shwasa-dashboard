# SHWASA – Personal Air-Quality Exposure Tracking System
## Frontend UI Prototype

This repository contains the first UI prototype for **SHWASA**, designed with a modern, calming environmental aesthetic using deep forest green, teal, off-white, and subtle grey tones.

---

### Key Features & Prototype Highlights

1. **Brand Header & Dynamic Greeting**:
   - Prominent **SHWASA** branding with an air-flow / breathing motif.
   - Dynamic greeting that adapts automatically to local time:
     - *Good Morning!* (< 12:00)
     - *Good Afternoon!* (12:00 – 16:59)
     - *Good Evening!* (17:00+)

2. **Today's Overview**:
   - **Nearby PM2.5 Card**: Reserved prominent area for ambient numerical value (`µg/m³`), displaying formatted placeholder `—` awaiting sensor stream.
   - **Exposure So Far Card**: Reserved prominent area for cumulative exposure numerical value (`µg·h/m³`), displaying formatted placeholder `—`.

3. **Today's Activity**:
   - Right-aligned **Edit Timeline** button (visible, non-functional).
   - 5 sample activity blocks with start time (`00:00`), end time (`00:00`), duration (`00:00`), and Indoor/Outdoor classification badges.
   - **Internal Vertical Scrollbar**: Exactly 3 blocks are visible initially; the remaining 2 blocks are revealed by scrolling inside the activity card without scrolling the overall dashboard.

4. **PM2.5 Forecast**:
   - Smooth spline line chart using **Plotly**.
   - Displays sample simulated forecast for the next 60 minutes with subtle gridlines and custom tooltips.
   - Marked clearly as sample/demo data.

5. **Generate Today's Summary**:
   - Prominent hero call-to-action button at the bottom (visible, non-functional).

---

### Running the Application Locally

#### Prerequisites
- Python 3.10+
- Streamlit & Plotly (see `requirements.txt`)

#### Quick Launch (Windows)
Double-click `run_dashboard.bat` or run:

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Launch Streamlit
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

