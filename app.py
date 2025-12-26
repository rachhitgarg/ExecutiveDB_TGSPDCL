"""
TGSPDCL AI Voice Agent - Executive Dashboard
============================================
Real-time monitoring dashboard for management and executives.

Features:
- Live Operations monitoring
- Performance KPIs tracking
- TV Display mode for wall-mounted screens
- Date range filtering (Today, 7 Days, Custom)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dateutil.parser import parse
import random

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="TGSPDCL Executive Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #475569;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card-tv {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 20px;
        padding: 40px;
        border: 2px solid #F59E0B;
        box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.4);
        text-align: center;
    }
    
    .metric-value {
        font-size: 48px;
        font-weight: 700;
        color: #F59E0B;
        line-height: 1.2;
    }
    
    .metric-value-tv {
        font-size: 72px;
        font-weight: 800;
        color: #F59E0B;
        line-height: 1.1;
    }
    
    .metric-label {
        font-size: 14px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-label-tv {
        font-size: 20px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
    
    .metric-delta-positive {
        color: #10B981;
        font-size: 14px;
    }
    
    .metric-delta-negative {
        color: #EF4444;
        font-size: 14px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #F59E0B;
    }
    
    /* Progress bars */
    .progress-container {
        background: #334155;
        border-radius: 8px;
        height: 12px;
        overflow: hidden;
        margin-top: 8px;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E293B;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 12px 24px;
        color: #94A3B8;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #F59E0B;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MOCK DATA GENERATORS
# =============================================================================

def get_live_metrics():
    """Generate live operations metrics."""
    base_calls = 4500 + random.randint(-200, 200)
    hour = datetime.now().hour
    
    # Simulate hourly patterns (higher during business hours)
    if 9 <= hour <= 18:
        multiplier = 1.0 + random.uniform(0.1, 0.3)
    else:
        multiplier = 0.4 + random.uniform(0.1, 0.2)
    
    return {
        'active_calls': int(random.randint(80, 180) * multiplier),
        'calls_today': int(base_calls * multiplier),
        'calls_queue': random.randint(5, 35),
        'capacity_utilization': random.uniform(45, 85),
        'avg_wait_time': random.uniform(8, 45),
        'calls_per_hour': random.randint(200, 450)
    }

def get_language_distribution():
    """Generate language distribution data."""
    telugu_pct = random.uniform(52, 62)
    hindi_pct = random.uniform(22, 30)
    english_pct = 100 - telugu_pct - hindi_pct
    
    return pd.DataFrame({
        'Language': ['Telugu', 'Hindi', 'English'],
        'Percentage': [telugu_pct, hindi_pct, english_pct],
        'Calls': [
            int(4500 * telugu_pct / 100),
            int(4500 * hindi_pct / 100),
            int(4500 * english_pct / 100)
        ]
    })

def get_top_intents():
    """Generate top customer intents."""
    intents = [
        ('Bill Inquiry', random.randint(800, 1200)),
        ('Outage Status', random.randint(600, 900)),
        ('Payment Confirmation', random.randint(400, 600)),
        ('Complaint Status', random.randint(300, 500)),
        ('New Connection', random.randint(200, 400)),
    ]
    return pd.DataFrame(intents, columns=['Intent', 'Count'])

def get_performance_kpis():
    """Generate performance KPI metrics."""
    return {
        'containment_rate': random.uniform(68, 78),
        'containment_target': 70.0,
        'fcr_rate': random.uniform(65, 75),
        'fcr_target': 70.0,
        'avg_handle_time': random.uniform(4.5, 7.5),
        'aht_target': 8.0,
        'calls_today': random.randint(4000, 5500),
        'calls_yesterday': random.randint(4000, 5500),
        'containment_yesterday': random.uniform(65, 75),
        'fcr_yesterday': random.uniform(62, 72),
        'aht_yesterday': random.uniform(5.0, 8.0)
    }

def get_hourly_call_volume(date_range='today'):
    """Generate hourly call volume data."""
    hours = list(range(24))
    
    if date_range == 'today':
        current_hour = datetime.now().hour
        volumes = []
        for h in hours:
            if h <= current_hour:
                base = 150 if 9 <= h <= 18 else 50
                volumes.append(base + random.randint(-30, 50))
            else:
                volumes.append(0)
    else:
        volumes = []
        for h in hours:
            base = 350 if 9 <= h <= 18 else 100
            volumes.append(base + random.randint(-50, 80))
    
    return pd.DataFrame({
        'Hour': [f'{h:02d}:00' for h in hours],
        'Calls': volumes
    })

def get_daily_trends(days=7):
    """Generate daily trend data."""
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days-1, -1, -1)]
    
    data = []
    for date in dates:
        total = random.randint(5500, 7500)
        contained = int(total * random.uniform(0.68, 0.78))
        escalated = total - contained
        
        data.append({
            'Date': date,
            'Total Calls': total,
            'AI Resolved': contained,
            'Escalated': escalated,
            'Containment Rate': (contained / total) * 100
        })
    
    return pd.DataFrame(data)

def get_resolution_breakdown():
    """Generate resolution breakdown data."""
    return pd.DataFrame({
        'Category': ['AI Resolved', 'Human Escalation', 'Abandoned', 'Transferred'],
        'Count': [
            random.randint(3000, 4000),
            random.randint(800, 1200),
            random.randint(100, 200),
            random.randint(50, 150)
        ],
        'Color': ['#10B981', '#3B82F6', '#EF4444', '#F59E0B']
    })

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_metric_card(label, value, delta=None, delta_prefix="", suffix="", is_inverse=False):
    """Render a metric card with optional delta."""
    delta_html = ""
    if delta is not None:
        delta_class = "metric-delta-positive" if (delta >= 0 and not is_inverse) or (delta < 0 and is_inverse) else "metric-delta-negative"
        delta_sign = "+" if delta >= 0 else ""
        delta_html = f'<div class="{delta_class}">{delta_prefix}{delta_sign}{delta:.1f}{suffix} vs yesterday</div>'
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}{suffix}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_metric_card_tv(label, value, suffix="", color="#F59E0B"):
    """Render a large metric card for TV display."""
    st.markdown(f"""
        <div class="metric-card-tv">
            <div class="metric-label-tv">{label}</div>
            <div class="metric-value-tv" style="color: {color};">{value}{suffix}</div>
        </div>
    """, unsafe_allow_html=True)

def render_progress_bar(value, max_value=100, color="#F59E0B"):
    """Render a progress bar."""
    percentage = min((value / max_value) * 100, 100)
    st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%; background: {color};"></div>
        </div>
    """, unsafe_allow_html=True)

def create_gauge_chart(value, title, target=None, max_val=100):
    """Create a gauge chart for KPIs."""
    color = "#10B981" if value >= (target or 70) else "#F59E0B" if value >= (target or 70) * 0.9 else "#EF4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={'suffix': '%', 'font': {'size': 36, 'color': '#F1F5F9'}},
        delta={'reference': target, 'relative': False, 'position': 'bottom'} if target else None,
        title={'text': title, 'font': {'size': 16, 'color': '#94A3B8'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': '#475569'},
            'bar': {'color': color},
            'bgcolor': '#1E293B',
            'borderwidth': 2,
            'bordercolor': '#475569',
            'steps': [
                {'range': [0, target * 0.9] if target else [0, 60], 'color': '#374151'},
                {'range': [target * 0.9, target] if target else [60, 80], 'color': '#374151'},
                {'range': [target, max_val] if target else [80, 100], 'color': '#1F2937'}
            ],
            'threshold': {
                'line': {'color': '#F59E0B', 'width': 3},
                'thickness': 0.8,
                'value': target
            } if target else None
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#F1F5F9'}
    )
    
    return fig

def create_donut_chart(df, names_col, values_col, title=""):
    """Create a donut chart for distribution data."""
    colors = {'Telugu': '#F59E0B', 'Hindi': '#3B82F6', 'English': '#10B981'}
    color_list = [colors.get(name, '#94A3B8') for name in df[names_col]]
    
    fig = go.Figure(data=[go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=0.6,
        marker_colors=color_list,
        textinfo='label+percent',
        textposition='outside',
        textfont={'color': '#F1F5F9', 'size': 12}
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#F1F5F9'), x=0.5),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font={'color': '#F1F5F9'}
    )
    
    return fig

def create_bar_chart(df, x_col, y_col, title="", orientation='h'):
    """Create a horizontal bar chart."""
    fig = go.Figure(data=[go.Bar(
        x=df[y_col] if orientation == 'h' else df[x_col],
        y=df[x_col] if orientation == 'h' else df[y_col],
        orientation=orientation,
        marker_color='#F59E0B',
        text=df[y_col],
        textposition='outside',
        textfont={'color': '#F1F5F9'}
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#F1F5F9'), x=0.5),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
        yaxis={'showgrid': False, 'color': '#94A3B8'},
        font={'color': '#F1F5F9'}
    )
    
    return fig

def create_line_chart(df, x_col, y_col, title=""):
    """Create a line chart for trends."""
    fig = go.Figure(data=[go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=8, color='#F59E0B'),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.1)'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#F1F5F9'), x=0.5),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
        yaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
        font={'color': '#F1F5F9'}
    )
    
    return fig

def create_area_chart(df, x_col, y_cols, title=""):
    """Create a stacked area chart."""
    colors = ['#10B981', '#3B82F6', '#EF4444', '#F59E0B']
    
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[col],
            mode='lines',
            name=col,
            stackgroup='one',
            line=dict(color=colors[i % len(colors)]),
            fillcolor=colors[i % len(colors)].replace(')', ', 0.6)').replace('rgb', 'rgba') if 'rgb' in colors[i % len(colors)] else colors[i % len(colors)] + '99'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#F1F5F9'), x=0.5),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
        yaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font={'color': '#F1F5F9'}),
        font={'color': '#F1F5F9'}
    )
    
    return fig

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Telangana_State_Electricity_Regulatory_Commission_logo.png/220px-Telangana_State_Electricity_Regulatory_Commission_logo.png", width=80)
    st.title("TGSPDCL")
    st.caption("AI Voice Agent Dashboard")
    
    st.divider()
    
    # Display mode selection
    display_mode = st.radio(
        "📺 Display Mode",
        ["Desktop", "TV Display"],
        help="TV Display mode shows larger metrics optimized for wall-mounted screens"
    )
    
    st.divider()
    
    # Date filter
    st.subheader("📅 Date Range")
    date_option = st.radio(
        "Select period",
        ["Today", "Last 7 Days", "Custom Range"],
        label_visibility="collapsed"
    )
    
    if date_option == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", datetime.now() - timedelta(days=7))
        with col2:
            end_date = st.date_input("To", datetime.now())
    
    st.divider()
    
    # Auto-refresh
    auto_refresh = st.toggle("🔄 Auto Refresh (30s)", value=True)
    if auto_refresh:
        st.caption("Dashboard refreshes automatically")
    
    # Manual refresh button
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    # Last updated
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.markdown("""
    <h1 style='color: #F1F5F9; margin-bottom: 0;'>
        ⚡ TGSPDCL Voice Agent Dashboard
    </h1>
    <p style='color: #94A3B8; font-size: 16px;'>
        Executive Monitoring Dashboard | Real-time AI Performance Tracking
    </p>
""", unsafe_allow_html=True)

# =============================================================================
# TV DISPLAY MODE
# =============================================================================

if display_mode == "TV Display":
    st.markdown("---")
    
    # Get metrics
    live_metrics = get_live_metrics()
    kpis = get_performance_kpis()
    
    # Top row - 3 large metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card_tv("Active Calls", live_metrics['active_calls'], color="#3B82F6")
    
    with col2:
        render_metric_card_tv("Calls Today", f"{live_metrics['calls_today']:,}", color="#F59E0B")
    
    with col3:
        render_metric_card_tv("Queue", live_metrics['calls_queue'], color="#EF4444" if live_metrics['calls_queue'] > 20 else "#10B981")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom row - 3 KPI metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        color = "#10B981" if kpis['containment_rate'] >= 70 else "#F59E0B"
        render_metric_card_tv("Containment Rate", f"{kpis['containment_rate']:.1f}", suffix="%", color=color)
    
    with col5:
        color = "#10B981" if kpis['fcr_rate'] >= 70 else "#F59E0B"
        render_metric_card_tv("First Call Resolution", f"{kpis['fcr_rate']:.1f}", suffix="%", color=color)
    
    with col6:
        color = "#10B981" if kpis['avg_handle_time'] <= 8 else "#F59E0B"
        render_metric_card_tv("Avg Handle Time", f"{kpis['avg_handle_time']:.1f}", suffix=" min", color=color)
    
    # Add progress bars under each KPI
    st.markdown("<br>", unsafe_allow_html=True)
    
    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown(f"<p style='text-align:center;color:#94A3B8;'>Target: 70%</p>", unsafe_allow_html=True)
        render_progress_bar(kpis['containment_rate'], 100, "#10B981" if kpis['containment_rate'] >= 70 else "#F59E0B")
    
    with col8:
        st.markdown(f"<p style='text-align:center;color:#94A3B8;'>Target: 70%</p>", unsafe_allow_html=True)
        render_progress_bar(kpis['fcr_rate'], 100, "#10B981" if kpis['fcr_rate'] >= 70 else "#F59E0B")
    
    with col9:
        st.markdown(f"<p style='text-align:center;color:#94A3B8;'>Target: ≤8 min</p>", unsafe_allow_html=True)
        render_progress_bar(8 - kpis['avg_handle_time'] + 8, 16, "#10B981" if kpis['avg_handle_time'] <= 8 else "#F59E0B")

# =============================================================================
# DESKTOP MODE
# =============================================================================

else:
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Live Operations", "📈 Performance KPIs"])
    
    # =========================================================================
    # TAB 1: LIVE OPERATIONS
    # =========================================================================
    with tab1:
        # Get live data
        live_metrics = get_live_metrics()
        language_dist = get_language_distribution()
        top_intents = get_top_intents()
        
        # Top metrics row
        st.markdown('<div class="section-header">📡 Current Status</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_metric_card(
                "Active Calls",
                live_metrics['active_calls'],
                delta=random.randint(-15, 25),
                delta_prefix=""
            )
        
        with col2:
            render_metric_card(
                "Calls Today",
                f"{live_metrics['calls_today']:,}",
                delta=random.randint(-200, 300),
                delta_prefix=""
            )
        
        with col3:
            render_metric_card(
                "Queue Size",
                live_metrics['calls_queue'],
                delta=random.randint(-8, 12),
                delta_prefix="",
                is_inverse=True
            )
        
        with col4:
            render_metric_card(
                "Capacity Used",
                f"{live_metrics['capacity_utilization']:.1f}",
                suffix="%"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts row
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="section-header">🌐 Language Distribution</div>', unsafe_allow_html=True)
            fig = create_donut_chart(language_dist, 'Language', 'Percentage', "")
            st.plotly_chart(fig, use_container_width=True)
            
            # Language stats
            for _, row in language_dist.iterrows():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{row['Language']}**")
                with col_b:
                    st.markdown(f"{row['Percentage']:.1f}%")
        
        with col_right:
            st.markdown('<div class="section-header">🎯 Top Customer Intents</div>', unsafe_allow_html=True)
            fig = create_bar_chart(top_intents, 'Intent', 'Count', "")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hourly volume chart
        st.markdown('<div class="section-header">📈 Hourly Call Volume (Today)</div>', unsafe_allow_html=True)
        hourly_data = get_hourly_call_volume('today')
        fig = create_line_chart(hourly_data, 'Hour', 'Calls', "")
        st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # TAB 2: PERFORMANCE KPIs
    # =========================================================================
    with tab2:
        # Get KPI data
        kpis = get_performance_kpis()
        daily_trends = get_daily_trends(7 if date_option == "Last 7 Days" else 30 if date_option == "Custom Range" else 1)
        resolution_data = get_resolution_breakdown()
        
        # KPI Gauges
        st.markdown('<div class="section-header">🎯 Key Performance Indicators</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = create_gauge_chart(kpis['containment_rate'], "Containment Rate", target=70)
            st.plotly_chart(fig, use_container_width=True)
            
            delta = kpis['containment_rate'] - kpis['containment_yesterday']
            delta_color = "green" if delta >= 0 else "red"
            st.markdown(f"""
                <p style='text-align:center;color:{delta_color};'>
                    {'↑' if delta >= 0 else '↓'} {abs(delta):.1f}% vs yesterday
                </p>
            """, unsafe_allow_html=True)
        
        with col2:
            fig = create_gauge_chart(kpis['fcr_rate'], "First Call Resolution", target=70)
            st.plotly_chart(fig, use_container_width=True)
            
            delta = kpis['fcr_rate'] - kpis['fcr_yesterday']
            delta_color = "green" if delta >= 0 else "red"
            st.markdown(f"""
                <p style='text-align:center;color:{delta_color};'>
                    {'↑' if delta >= 0 else '↓'} {abs(delta):.1f}% vs yesterday
                </p>
            """, unsafe_allow_html=True)
        
        with col3:
            # For AHT, lower is better, so we invert the gauge logic
            aht_score = max(0, 100 - (kpis['avg_handle_time'] / 12) * 100)
            fig = create_gauge_chart(aht_score, f"Avg Handle Time: {kpis['avg_handle_time']:.1f} min", target=66.7)  # 8 min = 66.7%
            st.plotly_chart(fig, use_container_width=True)
            
            delta = kpis['aht_yesterday'] - kpis['avg_handle_time']  # Positive delta is good
            delta_color = "green" if delta >= 0 else "red"
            st.markdown(f"""
                <p style='text-align:center;color:{delta_color};'>
                    {'↓' if delta >= 0 else '↑'} {abs(delta):.1f} min vs yesterday
                </p>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Today vs Yesterday comparison
        st.markdown('<div class="section-header">📊 Today vs Yesterday</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            change = ((kpis['calls_today'] - kpis['calls_yesterday']) / kpis['calls_yesterday']) * 100
            render_metric_card(
                "Total Calls",
                f"{kpis['calls_today']:,}",
                delta=change,
                suffix="%"
            )
        
        with col2:
            ai_resolved = int(kpis['calls_today'] * kpis['containment_rate'] / 100)
            ai_yesterday = int(kpis['calls_yesterday'] * kpis['containment_yesterday'] / 100)
            change = ((ai_resolved - ai_yesterday) / ai_yesterday) * 100 if ai_yesterday > 0 else 0
            render_metric_card(
                "AI Resolved",
                f"{ai_resolved:,}",
                delta=change,
                suffix="%"
            )
        
        with col3:
            escalated = kpis['calls_today'] - int(kpis['calls_today'] * kpis['containment_rate'] / 100)
            esc_yesterday = kpis['calls_yesterday'] - int(kpis['calls_yesterday'] * kpis['containment_yesterday'] / 100)
            change = ((escalated - esc_yesterday) / esc_yesterday) * 100 if esc_yesterday > 0 else 0
            render_metric_card(
                "Escalated",
                f"{escalated:,}",
                delta=change,
                suffix="%",
                is_inverse=True
            )
        
        with col4:
            # Cost savings calculation: ₹50 per AI-resolved call
            savings = ai_resolved * 50
            savings_yesterday = ai_yesterday * 50
            change = ((savings - savings_yesterday) / savings_yesterday) * 100 if savings_yesterday > 0 else 0
            render_metric_card(
                "Cost Savings",
                f"₹{savings:,.0f}",
                delta=change,
                suffix="%"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts row
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="section-header">📈 Call Volume Trend</div>', unsafe_allow_html=True)
            if len(daily_trends) > 1:
                fig = create_line_chart(daily_trends, 'Date', 'Total Calls', "")
                st.plotly_chart(fig, use_container_width=True)
            else:
                hourly_data = get_hourly_call_volume('today')
                fig = create_line_chart(hourly_data, 'Hour', 'Calls', "Today's Hourly Volume")
                st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown('<div class="section-header">🥧 Resolution Breakdown</div>', unsafe_allow_html=True)
            if len(daily_trends) > 1:
                fig = create_area_chart(daily_trends, 'Date', ['AI Resolved', 'Escalated'], "")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = create_donut_chart(resolution_data, 'Category', 'Count', "")
                st.plotly_chart(fig, use_container_width=True)
        
        # Containment rate trend
        if len(daily_trends) > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Containment Rate Trend</div>', unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_trends['Date'],
                y=daily_trends['Containment Rate'],
                mode='lines+markers',
                name='Containment Rate',
                line=dict(color='#F59E0B', width=3),
                marker=dict(size=10)
            ))
            
            # Add target line
            fig.add_hline(y=70, line_dash="dash", line_color="#10B981", 
                         annotation_text="Target: 70%", annotation_position="right")
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8'},
                yaxis={'showgrid': True, 'gridcolor': '#334155', 'color': '#94A3B8', 'range': [50, 100]},
                font={'color': '#F1F5F9'}
            )
            
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# AUTO-REFRESH
# =============================================================================

if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()
