import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sandy Alcantara Performance Analysis",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Google Fonts and baseball theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;600;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
    }
    
    /* Title styling */
    h1 {
        font-family: 'Bebas Neue', cursive;
        font-size: 3.5rem !important;
        color: #0d47a1 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem !important;
        letter-spacing: 2px;
    }
    
    h2 {
        font-family: 'Oswald', sans-serif;
        font-weight: 700 !important;
        color: #1565c0 !important;
        border-bottom: 3px solid #ff6f00;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-family: 'Oswald', sans-serif;
        font-weight: 600 !important;
        color: #1976d2 !important;
    }
    
    /* Subheader styling */
    .subheader {
        font-family: 'Oswald', sans-serif;
        font-weight: 600;
        color: #424242;
    }
    
    /* Body text */
    p, li, div {
        font-family: 'Roboto', sans-serif;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-family: 'Bebas Neue', cursive;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-family: 'Bebas Neue', cursive;
        font-size: 2.5rem !important;
        color: #0d47a1 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Oswald', sans-serif;
        font-weight: 600;
        color: #424242 !important;
    }
    
    /* Buttons and selectboxes */
    .stSelectbox label, .stRadio label {
        font-family: 'Oswald', sans-serif;
        font-weight: 600;
        color: #1565c0 !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Oswald', sans-serif;
        font-weight: 600;
        color: #1565c0;
    }
    
    /* Baseball emoji decorations */
    .baseball-header {
        text-align: center;
        font-size: 1.2rem;
        color: #424242;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and prepare the data from Excel file"""
    # Load all sheets
    df_data = pd.read_excel('Data/sandy_stats_since_21 copy.xlsx', sheet_name='Data')
    df_season = pd.read_excel('Data/sandy_stats_since_21 copy.xlsx', sheet_name='Season Totals')
    df_vars = pd.read_excel('Data/sandy_stats_since_21 copy.xlsx', sheet_name='Variable Descriptions')
    
    # Clean up the data sheet - remove unnamed columns
    # Handle NaN values by filling them with False before applying ~ operator
    unnamed_mask = df_data.columns.str.contains('^Unnamed', na=False)
    df_data = df_data.loc[:, ~unnamed_mask]
    
    # Ensure Date is datetime
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    
    return df_data, df_season, df_vars

# Load data
df_data, df_season, df_vars = load_data()

# Title and Introduction
st.title("⚾ Sandy Alcantara: Performance Analysis Dashboard")

# Add Sandy Alcantara image at the top
st.image("Sandy Picture.jpeg", use_container_width=True)

st.markdown("""
<div class="baseball-header">
    🏟️ ⚾ 🎯 ⚾ 📊 ⚾ 🎯 ⚾ 🏟️
</div>
""", unsafe_allow_html=True)
st.markdown("""
### 🏆 From Cy Young Winner to Recovery: A Deep Dive into Sandy Alcantara's Pitching Journey ⚾

This interactive dashboard analyzes Sandy Alcantara's performance from his **Cy Young Award-winning 2022 season** through his return from **Tommy John surgery in 2025**. Explore his stats, pitch usage, and recovery journey below!
""")

# Sidebar
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='color: white; font-size: 2rem; margin: 0;'>⚾📊⚾</h1>
</div>
""", unsafe_allow_html=True)
st.sidebar.header("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Select a section:",
    ["Overview", "Performance Regression", "Pitch Usage Analysis", "Detailed Statistics", "Analysis & Recommendations"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: white; font-size: 0.9rem;'>
    <p>⚾ Baseball Analytics ⚾</p>
    <p>MGMT 504 Project</p>
</div>
""", unsafe_allow_html=True)

# Baseball-themed color scheme
colors = {
    '2021': '#1565c0',  # Blue
    '2022': '#2e7d32',  # Green for Cy Young year (baseball field green)
    '2023': '#f57c00',  # Orange
    '2025': '#c62828'   # Red for worst year
}

# ========== OVERVIEW PAGE ==========
if page == "Overview":
    st.header("📈 Season Overview ⚾")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Custom metric display with big numbers and descriptions
    with col1:
        era_2021 = df_season[df_season['Year'] == 2021]['ERA'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #1565c0;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #0d47a1; line-height: 1;'>{era_2021:.2f}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2021 ERA</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Earned Run Average</div>
        </div>
        """, unsafe_allow_html=True)
        w_2021 = df_season[df_season['Year'] == 2021]['W'].values[0]
        l_2021 = df_season[df_season['Year'] == 2021]['L'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #1565c0; margin-top: 1rem;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #0d47a1; line-height: 1;'>{w_2021}-{l_2021}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2021 Record</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Wins - Losses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        era_2022 = df_season[df_season['Year'] == 2022]['ERA'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); border-radius: 10px; border: 3px solid #2e7d32;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #1b5e20; line-height: 1;'>{era_2022:.2f}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>🏆 2022 ERA</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Cy Young Award Winner</div>
        </div>
        """, unsafe_allow_html=True)
        w_2022 = df_season[df_season['Year'] == 2022]['W'].values[0]
        l_2022 = df_season[df_season['Year'] == 2022]['L'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); border-radius: 10px; border: 3px solid #2e7d32; margin-top: 1rem;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #1b5e20; line-height: 1;'>{w_2022}-{l_2022}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>⭐ 2022 Record</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Wins - Losses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        era_2023 = df_season[df_season['Year'] == 2023]['ERA'].values[0]
        era_change_2023 = era_2023 - era_2022
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #f57c00;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #e65100; line-height: 1;'>{era_2023:.2f}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2023 ERA</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>+{era_change_2023:.2f} from 2022</div>
        </div>
        """, unsafe_allow_html=True)
        w_2023 = df_season[df_season['Year'] == 2023]['W'].values[0]
        l_2023 = df_season[df_season['Year'] == 2023]['L'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #f57c00; margin-top: 1rem;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #e65100; line-height: 1;'>{w_2023}-{l_2023}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2023 Record</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Wins - Losses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        era_2025 = df_season[df_season['Year'] == 2025]['ERA'].values[0]
        era_change_2025 = era_2025 - era_2022
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #c62828;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #b71c1c; line-height: 1;'>{era_2025:.2f}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2025 ERA</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>+{era_change_2025:.2f} from 2022</div>
        </div>
        """, unsafe_allow_html=True)
        w_2025 = df_season[df_season['Year'] == 2025]['W'].values[0]
        l_2025 = df_season[df_season['Year'] == 2025]['L'].values[0]
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%); border-radius: 10px; border: 2px solid #c62828; margin-top: 1rem;'>
            <div style='font-family: "Bebas Neue", cursive; font-size: 4rem; color: #b71c1c; line-height: 1;'>{w_2025}-{l_2025}</div>
            <div style='font-family: "Oswald", sans-serif; font-size: 1.2rem; color: #424242; margin-top: 0.5rem; font-weight: 600;'>2025 Record</div>
            <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; margin-top: 0.3rem;'>Wins - Losses</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key metrics comparison
    st.subheader("⚾ Key Performance Metrics by Season")
    
    metrics_to_show = ['ERA', 'FIP', 'SO', 'BB', 'HR', 'IP', 'BAbip']
    metric_names = {
        'ERA': 'ERA (Earned Run Average)',
        'FIP': 'FIP (Fielding Independent Pitching)',
        'SO': 'Strikeouts',
        'BB': 'Walks',
        'HR': 'Home Runs',
        'IP': 'Innings Pitched',
        'BAbip': 'Batting Average on Balls in Play'
    }
    
    selected_metric = st.selectbox("Select a metric to compare:", list(metric_names.keys()), 
                                   format_func=lambda x: metric_names[x])
    
    # Convert Year to int and prepare data
    years_int = df_season['Year'].astype(int).tolist()
    metric_values = df_season[selected_metric].tolist()
    max_val = max(metric_values)
    
    # Determine text format - whole numbers for HR, SO, BB, etc., decimals for others
    whole_number_metrics = ['HR', 'SO', 'BB', 'H', 'IP']
    if selected_metric in whole_number_metrics:
        text_format = [f"{int(val)}" for val in metric_values]
        text_template = '%{text}'
    elif selected_metric == 'BAbip':
        # BAbip should have 3 decimal places
        text_format = [f"{val:.3f}" for val in metric_values]
        text_template = '%{text:.3f}'
    else:
        text_format = [f"{val:.2f}" for val in metric_values]
        text_template = '%{text:.2f}'
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=years_int,
            y=metric_values,
            marker_color=[colors[str(y)] for y in years_int],
            text=text_format,
            textposition='outside',
            hovertemplate=f'{metric_names[selected_metric]}: %{{y}}<extra></extra>'
        )
    )
    
    # Always add padding to prevent numbers from being cut off
    fig.update_layout(
        title=f"⚾ {metric_names[selected_metric]} by Season",
        xaxis_title="Season",
        yaxis_title=metric_names[selected_metric],
        showlegend=False, 
        height=450,
        yaxis=dict(range=[0, max_val * 1.15]),  # Add 15% padding for text visibility
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=2021, dtick=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.subheader("📊 Complete Season Statistics")
    display_cols = ['Year', 'W', 'L', 'IP', 'ERA', 'FIP', 'SO', 'BB', 'HR', 'BAbip']
    st.dataframe(df_season[display_cols].style.format({
        'IP': '{:.1f}',
        'ERA': '{:.2f}',
        'FIP': '{:.2f}',
        'BAbip': '{:.3f}'
    }), use_container_width=True)

# ========== PERFORMANCE REGRESSION PAGE ==========
elif page == "Performance Regression":
    st.header("📉 Performance Regression Analysis ⚾")
    st.markdown("""
    This section shows how Sandy's performance has changed from his peak 2022 season through his return in 2025.
    """)
    
    # ERA and FIP trend
    st.subheader("⚾ ERA and FIP Over Time")
    
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    fig.add_trace(
        go.Scatter(
            x=df_season['Year'],
            y=df_season['ERA'],
            mode='lines+markers',
            name='ERA',
            line=dict(color='#d62728', width=3),
            marker=dict(size=12, symbol='circle')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_season['Year'],
            y=df_season['FIP'],
            mode='lines+markers',
            name='FIP',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=12, symbol='square')
        )
    )
    
    fig.update_layout(
        title="⚾ ERA and FIP Trend (Lower is Better)",
        xaxis_title="Season",
        yaxis_title="Runs Per 9 Innings",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add annotation for Cy Young year
    fig.add_annotation(
        x=2022, y=df_season[df_season['Year'] == 2022]['ERA'].values[0],
        text="🏆 Cy Young Award",
        showarrow=True,
        arrowhead=2,
        arrowcolor="green",
        bgcolor="rgba(255,255,255,0.8)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **What this shows:** 
    - ERA (Earned Run Average) measures runs allowed per 9 innings
    - FIP (Fielding Independent Pitching) measures what ERA should be based on strikeouts, walks, and home runs
    - Both metrics show a significant decline from 2022 to 2025
    """)
    
    st.markdown("---")
    
    # Game-by-game ERA progression
    st.subheader("📈 Game-by-Game ERA Progression")
    
    # Calculate cumulative ERA for each season
    fig = go.Figure()
    
    for year in [2021, 2022, 2023, 2025]:
        year_data = df_data[df_data['Year'] == year].sort_values('Date')
        year_data = year_data[year_data['ERA'].notna()]
        
        # Filter out January dates (offseason) - MLB season typically starts in late March/early April
        year_data = year_data[year_data['Date'].dt.month >= 3]  # Only March onwards
        
        fig.add_trace(
            go.Scatter(
                x=year_data['Date'],
                y=year_data['ERA'],
                mode='lines',
                name=f'{year}',
                line=dict(color=colors[str(year)], width=2),
                hovertemplate='Date: %{x}<br>ERA: %{y:.2f}<extra></extra>'
            )
        )
    
    fig.update_layout(
        title="⚾ ERA Throughout Each Season (Game-by-Game)",
        xaxis_title="Date",
        yaxis_title="ERA",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Strikeout and Walk rates
    st.subheader("🎯 Strikeout and Walk Trends")
    
    # Calculate rates per 9 innings
    df_season['K/9'] = (df_season['SO'] / df_season['IP']) * 9
    df_season['BB/9'] = (df_season['BB'] / df_season['IP']) * 9
    df_season['K/BB'] = df_season['SO'] / df_season['BB']
    
    col1, col2 = st.columns(2)
    
    with col1:
        years_int = df_season['Year'].astype(int).tolist()
        k9_vals = df_season['K/9'].tolist()
        bb9_vals = df_season['BB/9'].tolist()
        max_val = max(max(k9_vals), max(bb9_vals))
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name='Strikeouts per 9',
                x=years_int,
                y=k9_vals,
                marker_color='#2e7d32',
                text=[f"{val:.1f}" for val in k9_vals],
                textposition='outside'
            )
        )
        fig.add_trace(
            go.Bar(
                name='Walks per 9',
                x=years_int,
                y=bb9_vals,
                marker_color='#c62828',
                text=[f"{val:.1f}" for val in bb9_vals],
                textposition='outside'
            )
        )
        fig.update_layout(
            title="⚾ Strikeouts and Walks per 9 Innings",
            xaxis_title="Season",
            yaxis_title="Per 9 Innings",
            height=450, 
            barmode='group',
            showlegend=True,
            font=dict(family="Roboto, sans-serif", size=12),
            title_font=dict(family="Oswald, sans-serif", size=18, color="#1565c0"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', tick0=2021, dtick=1),
            yaxis=dict(range=[0, max_val * 1.15])  # Add padding
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        years_int = df_season['Year'].astype(int).tolist()
        kbb_vals = df_season['K/BB'].tolist()
        max_kbb = max(kbb_vals)
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=years_int,
                y=kbb_vals,
                mode='lines+markers',
                name='K/BB',
                line=dict(color='#1565c0', width=3),
                marker=dict(size=12, color='#1565c0'),
                text=[f"{val:.2f}" for val in kbb_vals],
                textposition='top center'
            )
        )
        fig.update_layout(
            title="⚾ Strikeout-to-Walk Ratio (Higher is Better)",
            xaxis_title="Season",
            yaxis_title="Strikeout-to-Walk Ratio",
            height=450,
            font=dict(family="Roboto, sans-serif", size=12),
            title_font=dict(family="Oswald, sans-serif", size=18, color="#1565c0"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', tick0=2021, dtick=1),
            yaxis=dict(range=[0, max_kbb * 1.15]),  # Add padding for text
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Key Insights:**
    - Strikeout rate (K/9) has decreased from 8.1 in 2022 to 7.3 in 2025
    - Walk rate (BB/9) has increased from 2.0 in 2022 to 2.9 in 2025
    - The strikeout-to-walk ratio has declined significantly, indicating less control and dominance
    """)

# ========== PITCH USAGE ANALYSIS PAGE ==========
elif page == "Pitch Usage Analysis":
    st.header("🎯 Pitch Type Usage Analysis ⚾")
    st.markdown("""
    This section examines how Sandy's pitch mix has changed over time, which is crucial for understanding his performance.
    """)
    
    # Pitch type percentages
    pitch_types = ['Four-seam %', 'Sinker %', 'Slider %', 'Curve %', 'Changeup %']
    pitch_names = {
        'Four-seam %': 'Four-Seam Fastball',
        'Sinker %': 'Sinker',
        'Slider %': 'Slider',
        'Curve %': 'Curveball',
        'Changeup %': 'Changeup'
    }
    
    st.subheader("⚾ Pitch Type Usage by Season")
    
    # Create a grouped bar chart instead of stacked area for better clarity
    fig = go.Figure()
    
    # Prepare data for grouped bars
    years = df_season['Year'].astype(int).tolist()  # Convert to int to remove .5
    
    for pitch in pitch_types:
        fig.add_trace(
            go.Bar(
                name=pitch_names[pitch],
                x=years,
                y=df_season[pitch] * 100,
                hovertemplate=f'{pitch_names[pitch]}: %{{y:.1f}}%<extra></extra>',
                text=[f"{val:.1f}%" for val in df_season[pitch] * 100],
                textposition='outside',
                textangle=0
            )
        )
    
    # Calculate max value for padding
    max_pitch_pct = max([df_season[pitch].max() * 100 for pitch in pitch_types])
    
    fig.update_layout(
        title="⚾ Pitch Type Distribution by Season (Grouped Bars)",
        xaxis_title="Season",
        yaxis_title="Usage Percentage (%)",
        height=500,
        barmode='group',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=2021, dtick=1),  # Show only whole years
        yaxis=dict(range=[0, max_pitch_pct * 1.1])  # Add padding for text visibility
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **What this shows:** This chart displays how often Sandy used each pitch type in each season. 
    Each bar group represents one season, and the different colored bars show the percentage usage 
    of each pitch type. The percentages add up to 100% for each season.
    """)
    
    st.markdown("---")
    
    # Individual pitch trends
    st.subheader("🎯 Individual Pitch Type Trends")
    
    selected_pitch = st.selectbox(
        "Select a pitch type to analyze:",
        pitch_types,
        format_func=lambda x: pitch_names[x]
    )
    
    # Fix: Convert Year to int and create proper bar chart
    years_int = df_season['Year'].astype(int).tolist()
    pitch_values = df_season[selected_pitch].tolist()
    
    fig = go.Figure()
    pitch_values_100 = [val * 100 for val in pitch_values]
    max_pitch_val = max(pitch_values_100)
    
    fig.add_trace(
        go.Bar(
            x=years_int,
            y=pitch_values_100,
            marker_color=[colors[str(y)] for y in years_int],
            text=[f"{val:.1f}%" for val in pitch_values_100],
            textposition='outside',
            hovertemplate=f'{pitch_names[selected_pitch]}: %{{y:.1f}}%<extra></extra>'
        )
    )
    
    fig.update_layout(
        title=f"⚾ {pitch_names[selected_pitch]} Usage by Season",
        xaxis_title="Season",
        yaxis_title=f"{pitch_names[selected_pitch]} Usage (%)",
        showlegend=False, 
        height=450,
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=2021, dtick=1),
        yaxis=dict(range=[0, max_pitch_val * 1.15])  # Add padding for text - FIXED: use yaxis in update_layout
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate changes
    pitch_2022 = df_season[df_season['Year'] == 2022][selected_pitch].values[0]
    pitch_2025 = df_season[df_season['Year'] == 2025][selected_pitch].values[0]
    change = (pitch_2025 - pitch_2022) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("2022 Usage", f"{pitch_2022*100:.1f}%")
    with col2:
        st.metric("2025 Usage", f"{pitch_2025*100:.1f}%")
    with col3:
        st.metric("Change", f"{change:+.1f}%", delta=f"{change:+.1f} percentage points")
    
    st.markdown("---")
    
    # Pitch comparison table
    st.subheader("📊 Complete Pitch Usage Comparison")
    
    pitch_display = df_season[['Year'] + pitch_types].copy()
    for pitch in pitch_types:
        pitch_display[pitch] = pitch_display[pitch] * 100
    
    pitch_display.columns = ['Year'] + [pitch_names[p] for p in pitch_types]
    st.dataframe(
        pitch_display.style.format({pitch_names[p]: '{:.1f}%' for p in pitch_types}),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Key observations
    st.subheader("🔍 Key Observations on Pitch Usage")
    
    observations = {
        'Four-seam %': {
            'trend': 'Decreasing',
            'change': f"{(df_season[df_season['Year'] == 2025]['Four-seam %'].values[0] - df_season[df_season['Year'] == 2022]['Four-seam %'].values[0]) * 100:.1f}%",
            'impact': 'Less reliance on four-seam fastball may indicate velocity concerns or confidence issues'
        },
        'Sinker %': {
            'trend': 'Decreasing',
            'change': f"{(df_season[df_season['Year'] == 2025]['Sinker %'].values[0] - df_season[df_season['Year'] == 2022]['Sinker %'].values[0]) * 100:.1f}%",
            'impact': 'Sinker was a key pitch in 2022; reduced usage may be affecting ground ball rates'
        },
        'Slider %': {
            'trend': 'Decreasing',
            'change': f"{(df_season[df_season['Year'] == 2025]['Slider %'].values[0] - df_season[df_season['Year'] == 2022]['Slider %'].values[0]) * 100:.1f}%",
            'impact': 'Less slider usage reduces strikeout potential and weak contact generation'
        },
        'Curve %': {
            'trend': 'Increasing',
            'change': f"{(df_season[df_season['Year'] == 2025]['Curve %'].values[0] - df_season[df_season['Year'] == 2022]['Curve %'].values[0]) * 100:.1f}%",
            'impact': 'Dramatic increase in curveball usage (from 0.3% to 18.0%) suggests trying to compensate for other pitches'
        },
        'Changeup %': {
            'trend': 'Decreasing',
            'change': f"{(df_season[df_season['Year'] == 2025]['Changeup %'].values[0] - df_season[df_season['Year'] == 2022]['Changeup %'].values[0]) * 100:.1f}%",
            'impact': 'Changeup was a dominant pitch in 2022; reduced effectiveness may indicate arm strength issues'
        }
    }
    
    for pitch, info in observations.items():
        with st.expander(f"{pitch_names[pitch]} - {info['trend']} by {info['change']} percentage points"):
            st.write(f"**Impact:** {info['impact']}")

# ========== DETAILED STATISTICS PAGE ==========
elif page == "Detailed Statistics":
    st.header("📊 Detailed Statistical Analysis ⚾")
    
    # Select metric to analyze
    st.subheader("Select Metrics to Compare")
    
    # Full names mapping for display
    metric_full_names = {
        'ERA': 'Earned Run Average',
        'FIP': 'Fielding Independent Pitching',
        'SO': 'Strikeouts',
        'BB': 'Walks',
        'HR': 'Home Runs',
        'H': 'Hits',
        'IP': 'Innings Pitched',
        'BAbip': 'Batting Average on Balls in Play',
        'GmSc': 'Game Score',
        'WPA': 'Win Probability Added',
        'RE24': 'Run Expectancy 24',
        'Pit': 'Total Pitches',
        'Str': 'Strikes',
        'StL': 'Strikes Looking',
        'StS': 'Swinging Strikes',
        'GB': 'Ground Balls',
        'FB': 'Fly Balls',
        'LD': 'Line Drives',
        'PU': 'Pop-ups'
    }
    
    metric_options = {
        'Pitching Stats': ['ERA', 'FIP', 'SO', 'BB', 'HR', 'H', 'IP'],
        'Advanced Stats': ['BAbip', 'GmSc', 'WPA', 'RE24'],
        'Pitch Count Stats': ['Pit', 'Str', 'StL', 'StS'],
        'Batted Ball Stats': ['GB', 'FB', 'LD', 'PU']
    }
    
    category = st.selectbox("Select category:", list(metric_options.keys()))
    selected_metrics = st.multiselect("Select metrics to display:", metric_options[category], 
                                      default=metric_options[category][:3])
    
    if selected_metrics:
        # Use full names for subplot titles
        subplot_titles = [metric_full_names.get(m, m) for m in selected_metrics]
        
        fig = make_subplots(
            rows=len(selected_metrics),
            cols=1,
            subplot_titles=subplot_titles,
            vertical_spacing=0.1
        )
        
        for i, metric in enumerate(selected_metrics, 1):
            years_int = df_season['Year'].astype(int).tolist()
            metric_vals = df_season[metric].tolist()
            max_metric_val = max(metric_vals)
            
            # Format text based on metric type
            if metric in ['ERA', 'FIP', 'BAbip']:
                text_format = [f"{val:.2f}" for val in metric_vals]
            elif metric in ['Pit', 'Str', 'GmSc', 'GB', 'LD', 'FB', 'PU', 'StL', 'HR', 'SO', 'BB', 'H']:
                text_format = [f"{int(val)}" for val in metric_vals]
            else:
                text_format = [f"{val:.1f}" for val in metric_vals]
            
            fig.add_trace(
                go.Bar(
                    x=years_int,
                    y=metric_vals,
                    name=metric,
                    marker_color=[colors[str(y)] for y in years_int],
                    showlegend=False,
                    text=text_format,
                    textposition='outside'
                ),
                row=i, col=1
            )
            fig.update_xaxes(title_text="Season", row=i, col=1, tickmode='linear', tick0=2021, dtick=1)
            fig.update_yaxes(
                title_text=metric_full_names.get(metric, metric), 
                row=i, col=1,
                range=[0, max_metric_val * 1.15]  # Add padding to prevent text cutoff
            )
        
        fig.update_layout(
            title=f"⚾ {category} Comparison Across Seasons",
            height=300 * len(selected_metrics),
            showlegend=False,
            font=dict(family="Roboto, sans-serif", size=12),
            title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Game Score analysis
    st.subheader("⭐ Game Score Analysis")
    st.markdown("""
    Game Score is a metric that evaluates the quality of a pitching start (higher is better, typically 50+ is good, 70+ is excellent).
    """)
    
    # Calculate average game score by year
    avg_gmsc = df_data.groupby('Year')['GmSc'].mean().reset_index()
    avg_gmsc.columns = ['Year', 'Average Game Score']
    
    # Convert Year to int and fix chart
    avg_gmsc['Year'] = avg_gmsc['Year'].astype(int)
    max_score = avg_gmsc['Average Game Score'].max()
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=avg_gmsc['Year'],
            y=avg_gmsc['Average Game Score'],
            marker_color=[colors[str(y)] for y in avg_gmsc['Year']],
            text=[f"{val:.1f}" for val in avg_gmsc['Average Game Score']],
            textposition='outside',
            hovertemplate='Year: %{x}<br>Average Game Score: %{y:.1f}<extra></extra>'
        )
    )
    
    fig.update_traces()
    fig.update_layout(
        title="⚾ Average Game Score by Season",
        xaxis_title="Season",
        yaxis_title="Average Game Score",
        showlegend=False, 
        height=450,
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=2021, dtick=1),
        yaxis=dict(range=[0, max_score * 1.15])  # Add padding for text visibility
    )
    fig.add_hline(y=50, line_dash="dash", line_color="gray", 
                  annotation_text="Good Start Threshold (50)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='font-family: "Roboto", sans-serif; font-size: 0.9rem; color: #757575; font-style: italic; padding: 0.5rem 0;'>
        <strong>Footnote:</strong> The "Good Start Threshold" of 50 is based on Bill James' Game Score metric. 
        Game Score evaluates pitching performance on a scale where 50 represents an average quality start. 
        Scores above 50 indicate above-average starts, with 70+ being excellent and 90+ being exceptional. 
        The threshold of 50 is widely used in baseball analytics as a benchmark for determining whether a 
        pitcher had a "quality start" or better.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Batted ball profile
    st.subheader("⚾ Batted Ball Profile")
    st.markdown("""
    This shows the types of contact batters are making against Sandy's pitches.
    """)
    
    batted_ball_types = ['GB', 'FB', 'LD', 'PU']
    bb_names = {
        'GB': 'Ground Balls',
        'FB': 'Fly Balls',
        'LD': 'Line Drives',
        'PU': 'Pop-ups'
    }
    
    # Calculate percentages
    df_season['Total_BB'] = df_season[['GB', 'FB', 'LD', 'PU']].sum(axis=1)
    for bb in batted_ball_types:
        df_season[f'{bb}_pct'] = (df_season[bb] / df_season['Total_BB']) * 100
    
    fig = go.Figure()
    
    years_int = df_season['Year'].astype(int).tolist()
    
    for bb in batted_ball_types:
        fig.add_trace(
            go.Bar(
                name=bb_names[bb],
                x=years_int,
                y=df_season[f'{bb}_pct'],
                hovertemplate=f'{bb_names[bb]}: %{{y:.1f}}%<extra></extra>'
            )
        )
    
    fig.update_layout(
        title="⚾ Batted Ball Type Distribution by Season",
        xaxis_title="Season",
        yaxis_title="Percentage (%)",
        barmode='stack',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Roboto, sans-serif", size=12),
        title_font=dict(family="Oswald, sans-serif", size=20, color="#1565c0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=2021, dtick=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **What this shows:**
    - **Ground Balls (GB)**: Generally good for pitchers, lead to double plays and fewer extra-base hits
    - **Fly Balls (FB)**: Can be dangerous, especially in hitter-friendly parks
    - **Line Drives (LD)**: Usually result in hits, want to minimize these
    - **Pop-ups (PU)**: Almost always outs, very beneficial
    """)

# ========== ANALYSIS & RECOMMENDATIONS PAGE ==========
elif page == "Analysis & Recommendations":
    st.header("🔬 Data Analysis & Recommendations ⚾")
    
    st.markdown("""
    ## Executive Summary
    """)
    
    st.markdown("""
    <div style='font-family: "Oswald", sans-serif; font-size: 1.4rem; line-height: 1.8; color: #424242; padding: 1.5rem; background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); border-radius: 10px; border-left: 5px solid #1565c0;'>
        Sandy Alcantara's performance has significantly declined since his <strong>Cy Young Award-winning 2022 season</strong>. 
        After missing the entire 2024 season due to <strong>Tommy John surgery</strong>, his 2025 return has been the worst 
        statistical season of his career. This analysis examines the key factors contributing to this decline 
        and provides actionable recommendations for improvement.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📉 Key Performance Declines")
    
    # Calculate key declines
    stats_2022 = df_season[df_season['Year'] == 2022].iloc[0]
    stats_2025 = df_season[df_season['Year'] == 2025].iloc[0]
    
    declines = {
        'ERA': {
            '2022': stats_2022['ERA'],
            '2025': stats_2025['ERA'],
            'change': stats_2025['ERA'] - stats_2022['ERA'],
            'impact': 'Critical - ERA increased by 135%, meaning Sandy is allowing over 3 more runs per 9 innings'
        },
        'FIP': {
            '2022': stats_2022['FIP'],
            '2025': stats_2025['FIP'],
            'change': stats_2025['FIP'] - stats_2022['FIP'],
            'impact': 'Significant - Fielding-independent metrics also show decline, indicating the problem is with pitching, not defense'
        },
        'Strikeouts per 9': {
            '2022': (stats_2022['SO'] / stats_2022['IP']) * 9,
            '2025': (stats_2025['SO'] / stats_2025['IP']) * 9,
            'change': ((stats_2025['SO'] / stats_2025['IP']) * 9) - ((stats_2022['SO'] / stats_2022['IP']) * 9),
            'impact': 'Moderate - Strikeout rate down 10%, reducing ability to escape jams'
        },
        'Walk Rate': {
            '2022': (stats_2022['BB'] / stats_2022['IP']) * 9,
            '2025': (stats_2025['BB'] / stats_2025['IP']) * 9,
            'change': ((stats_2025['BB'] / stats_2025['IP']) * 9) - ((stats_2022['BB'] / stats_2022['IP']) * 9),
            'impact': 'Critical - Walk rate increased 45%, putting more runners on base and increasing pitch counts'
        },
        'Home Runs': {
            '2022': stats_2022['HR'],
            '2025': stats_2025['HR'],
            'change': stats_2025['HR'] - stats_2022['HR'],
            'impact': 'Significant - More home runs despite fewer innings, indicating reduced command and velocity'
        }
    }
    
    for stat, data in declines.items():
        with st.expander(f"**{stat}**: {data['2022']:.2f} → {data['2025']:.2f} (Change: {data['change']:+.2f})"):
            st.write(f"**Impact:** {data['impact']}")
    
    st.markdown("---")
    
    st.subheader("🎯 Pitch Usage Changes & Impact")
    
    st.markdown("""
    ### Major Pitch Mix Shifts:
    
    1. **Curveball Usage Explosion**: Increased from 0.3% in 2022 to 18.0% in 2025
       - This is a **60x increase** in curveball usage
       - Suggests Sandy is trying to compensate for reduced effectiveness of other pitches
       - May indicate he's lost confidence in his fastball or changeup
    
    2. **Changeup Decline**: Decreased from 27.6% to 23.2%
       - This was Sandy's most effective pitch in 2022
       - Reduced usage may indicate:
         - Loss of arm strength affecting changeup effectiveness
         - Reduced confidence in the pitch
         - Hitters adjusting to the pitch
    
    3. **Fastball Decline**: Both four-seam and sinker usage decreased
       - Four-seam: 25.2% → 21.1%
       - Sinker: 25.0% → 21.9%
       - Combined fastball usage down from 50.2% to 43.0%
       - This is concerning as fastballs are typically a pitcher's foundation
    
    4. **Slider Decline**: 22.0% → 15.8%
       - Reduced strikeout pitch usage correlates with lower strikeout totals
    """)
    
    st.markdown("---")
    
    st.subheader("💡 Root Cause Analysis")
    
    st.markdown("""
    ### Why Has Performance Declined?
    
    **1. Post-Surgery Recovery Challenges**
    - Tommy John surgery requires 12-18 months of recovery
    - Many pitchers take 2+ years to fully regain velocity and command
    - Sandy returned after missing only one full season, which may have been too soon
    
    **2. Velocity & Arm Strength**
    - Reduced fastball usage suggests velocity concerns
    - Lower strikeout rates indicate less "swing-and-miss" stuff
    - Increased walk rate shows command issues, common post-surgery
    
    **3. Pitch Effectiveness**
    - The dramatic shift to curveballs suggests other pitches aren't working
    - Changeup, once dominant, is being used less
    - Hitters may have adjusted to Sandy's pitch patterns
    
    **4. Confidence & Approach**
    - Pitching from behind in counts more often (higher walk rate)
    - Less aggressive approach (fewer strikeouts)
    - Trying to "pitch around" hitters instead of attacking them
    """)
    
    st.markdown("---")
    
    st.subheader("🚀 Recommendations for Improvement")
    
    st.markdown("""
    ### Short-Term (2026 Season)
    
    **1. Rebuild Fastball Command**
    - Focus on regaining velocity and command of both four-seam and sinker
    - Fastballs should be 45-50% of pitch mix (currently 43%)
    - Work with pitching coaches on mechanics and arm slot
    
    **2. Restore Changeup as Primary Weapon**
    - This was Sandy's best pitch in 2022 (27.6% usage, high effectiveness)
    - Gradually increase usage back toward 25-28% range
    - Focus on maintaining arm speed and deception
    
    **3. Reduce Curveball Dependency**
    - Current 18% usage is too high for a pitch that was barely used before
    - Reduce to 5-10% range, use as a "show" pitch or strikeout pitch in specific counts
    - Over-reliance suggests compensating for other pitches
    
    **4. Improve Control**
    - Walk rate must decrease from 2.9 to under 2.5 per 9 innings
    - Focus on first-pitch strikes
    - Attack hitters more aggressively, especially with fastball
    
    **5. Build Arm Strength Gradually**
    - Consider pitch count limits early in season
    - Focus on quality over quantity
    - Monitor velocity and adjust approach accordingly
    
    ### Long-Term (2027+)
    
    **1. Full Recovery Timeline**
    - Most pitchers need 2-3 years post-surgery to fully recover
    - Be patient with velocity and command improvements
    - Focus on health and mechanics over immediate results
    
    **2. Pitch Development**
    - Work on slider effectiveness to restore it as a strikeout pitch
    - Develop a cutter or two-seam variation to add to arsenal
    - Maintain changeup as signature pitch
    
    **3. Mental Approach**
    - Rebuild confidence through success in bullpen sessions
    - Trust the process and don't overthink on the mound
    - Work with sports psychologists if needed
    
    **4. Conditioning & Mechanics**
    - Continue strengthening program for elbow and shoulder
    - Work on maintaining consistent mechanics
    - Focus on flexibility and mobility
    """)
    
    st.markdown("---")
    
    st.subheader("📊 Expected Recovery Timeline")
    
    st.markdown("""
    Based on historical data from pitchers returning from Tommy John surgery:
    
    - **Year 1 (2025)**: Typically the worst year - ✅ **Current Status**
    - **Year 2 (2026)**: Gradual improvement, velocity returns, command improves
    - **Year 3 (2027)**: Near pre-surgery form, full confidence restored
    - **Year 4+ (2028+)**: Potentially better than pre-surgery with refined mechanics
    
    **Key Takeaway**: Sandy's 2025 struggles are **normal** for a pitcher in their first year back. 
    The focus should be on gradual improvement and health, not immediate return to Cy Young form.
    """)
    
    st.markdown("---")
    
    st.subheader("✅ Action Items Summary")
    
    action_items = [
        "✅ Reduce walk rate through improved fastball command",
        "✅ Restore changeup usage to 2022 levels (25-28%)",
        "✅ Decrease curveball dependency (target 5-10%)",
        "✅ Increase fastball usage back to 45-50% of mix",
        "✅ Focus on first-pitch strikes and attacking hitters",
        "✅ Build arm strength gradually with proper rest",
        "✅ Work with coaches on mechanics and pitch sequencing",
        "✅ Be patient - full recovery takes 2-3 years post-surgery"
    ]
    
    for item in action_items:
        st.markdown(f"- {item}")
    
    st.markdown("---")
    
    st.markdown("""
    <div style='font-family: "Oswald", sans-serif; font-size: 1.3rem; color: #1565c0; font-weight: 600; margin-bottom: 1rem;'>
        TLDR/Dashboard Summary:
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    This analysis shows that Sandy's struggles are understandable given his surgery. The key is patience and 
    focusing on the fundamentals: throwing strikes, trusting his best pitches, and gradually rebuilding 
    strength. With proper recovery time and adjustments, there's every reason to believe he can return to 
    being an effective pitcher, even if not immediately at his 2022 Cy Young level.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #1565c0; font-family: "Oswald", sans-serif; padding: 2rem 0;'>
    <p style='font-size: 1.2rem; margin: 0.5rem 0;'>⚾ 📊 ⚾ 📊 ⚾</p>
    <p style='font-size: 1rem; margin: 0.5rem 0;'>Dashboard created for MGMT 504 - Python Data Analysis</p>
    <p style='font-size: 0.9rem; margin: 0.5rem 0; color: #757575;'>Data: Sandy Alcantara MLB Pitching Statistics (2021-2025)</p>
    <p style='font-size: 1.2rem; margin: 0.5rem 0;'>⚾ 📊 ⚾ 📊 ⚾</p>
</div>
""", unsafe_allow_html=True)

