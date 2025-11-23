# Sandy Alcantara Performance Analysis Dashboard

An interactive dashboard analyzing Sandy Alcantara's MLB pitching performance from his Cy Young Award-winning 2022 season through his return from Tommy John surgery in 2025.

## Overview

This project provides a comprehensive analysis of Sandy Alcantara's pitching statistics, showing:
- Performance regression from 2022 to 2025
- Pitch type usage changes over time
- Detailed statistical trends
- Data-driven insights and recommendations

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Option 1: Using VS Code (Recommended)

**Method A: Using VS Code Terminal**
1. Open the project folder in VS Code
2. Open the integrated terminal (`Ctrl+`` ` or `Cmd+`` ` on Mac, or View → Terminal)
3. Run: `streamlit run dashboard.py`
4. The dashboard will open in your default web browser at `http://localhost:8501`
5. You can see the Streamlit server logs in the VS Code terminal

**Method B: Using VS Code Tasks**
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Run Streamlit Dashboard"
4. The dashboard will launch in your browser

**Method C: Using VS Code Debugger**
1. Go to the Run and Debug panel (⇧⌘D or F5)
2. Select "Streamlit Dashboard" from the dropdown
3. Press F5 or click the green play button
4. The dashboard will open in your browser

### Option 2: Using Terminal/Command Line

To launch the interactive dashboard, run:

```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Viewing in VS Code

While Streamlit opens in your browser, you can:
- See all server logs and output in the VS Code integrated terminal
- Edit the `dashboard.py` file and see changes auto-reload (Streamlit has hot-reload enabled)
- Use VS Code's built-in browser preview if you have a browser extension installed

## Dashboard Features

### 1. Overview
- Quick comparison of key metrics across all seasons
- Interactive metric selection
- Complete season statistics table

### 2. Performance Regression
- ERA and FIP trends over time
- Game-by-game ERA progression
- Strikeout and walk rate analysis

### 3. Pitch Usage Analysis
- Pitch type distribution over time
- Individual pitch type trends
- Detailed pitch usage comparisons

### 4. Detailed Statistics
- Customizable metric comparisons
- Game Score analysis
- Batted ball profile visualization

### 5. Analysis & Recommendations
- Comprehensive data analysis
- Root cause identification
- Actionable recommendations for improvement
- Expected recovery timeline

## Data Structure

The project uses an Excel file (`Data/sandy_stats_since_21 copy.xlsx`) with three sheets:
- **Data**: Game-by-game statistics for each start
- **Season Totals**: Aggregated statistics by year
- **Variable Descriptions**: Explanation of each variable

## Key Insights

- Sandy's ERA increased from 2.28 (2022) to 5.36 (2025)
- Walk rate increased by 45% from 2022 to 2025
- Curveball usage increased dramatically (0.3% to 18.0%)
- Changeup usage decreased from 27.6% to 23.2%
- Strikeout rate declined by 10%

## Technologies Used

- **Python**: Main programming language
- **Streamlit**: Interactive web dashboard framework
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file reading

## Project Structure

```
.
├── dashboard.py              # Main dashboard application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── Data/
    └── sandy_stats_since_21 copy.xlsx  # Dataset
```

## Deployment

To deploy this dashboard publicly, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

**Quick Deploy to Streamlit Community Cloud:**
1. Push your code to a GitHub repository
2. Go to https://share.streamlit.io/
3. Sign in with GitHub and deploy your app
4. Share the public URL!

## Notes

- The dashboard is designed to be accessible to non-technical users
- All visualizations are interactive and can be explored in detail
- Analysis focuses on actionable insights and recommendations
- The project demonstrates Python data analysis capabilities for MGMT 504

