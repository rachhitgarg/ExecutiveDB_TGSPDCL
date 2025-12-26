"""
TGSPDCL AI Voice Agent - Executive Dashboard
============================================
Real-time monitoring dashboard for management and executives.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
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
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
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
        color: #E2E8F0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-label-tv {
        font-size: 20px;
        color: #E2E8F0 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    .metric-delta-positive {
        color: #10B981;
        font-size: 14px;
        font-weight: 500;
    }
    
    .metric-delta-negative {
        color: #EF4444;
        font-size: 14px;
        font-weight: 500;
    }
    
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #FFFFFF !important;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #F59E0B;
    }
    
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 12px 24px;
        color: #E2E8F0 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #F59E0B;
        color: #0F172A !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    p, span, div {
        color: #F1F5F9;
    }
    
    .stSelectbox label, .stDateInput label, .stCheckbox label, .stRadio label {
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA GENERATORS
# =============================================================================

def get_live_metrics():
    base_calls = 4500 + random.randint(-200, 200)
    hour = datetime.now().hour
    multiplier = 1.0 + random.uniform(0.1, 0.3) if 9 <= hour <= 18 else 0.4 + random.uniform(0.1, 0.2)
    
    return {
        'active_calls': int(random.randint(80, 180) * multiplier),
        'calls_today': int(base_calls * multiplier),
        'calls_queue': random.randint(5, 35),
        'capacity_utilization': random.uniform(45, 85),
    }

def get_language_distribution():
    telugu_pct = random.uniform(52, 62)
    hindi_pct = random.uniform(22, 30)
    english_pct = 100 - telugu_pct - hindi_pct
    return pd.DataFrame({
        'Language': ['Telugu', 'Hindi', 'English'],
        'Percentage': [telugu_pct, hindi_pct, english_pct],
        'Calls': [int(4500 * telugu_pct / 100), int(4500 * hindi_pct / 100), int(4500 * english_pct / 100)]
    })

def get_top_intents():
    intents = [
        ('Bill Inquiry', random.randint(800, 1200)),
        ('Outage Status', random.randint(600, 900)),
        ('Payment Confirmation', random.randint(400, 600)),
        ('Complaint Status', random.randint(300, 500)),
        ('New Connection', random.randint(200, 400)),
    ]
    return pd.DataFrame(intents, columns=['Intent', 'Count'])

def get_performance_kpis():
    return {
        'containment_rate': random.uniform(68, 78),
        'fcr_rate': random.uniform(65, 75),
        'avg_handle_time': random.uniform(4.5, 7.5),
        'calls_today': random.randint(4000, 5500),
        'calls_yesterday': random.randint(4000, 5500),
        'containment_yesterday': random.uniform(65, 75),
        'fcr_yesterday': random.uniform(62, 72),
        'aht_yesterday': random.uniform(5.0, 8.0)
    }

def get_hourly_call_volume():
    hours = list(range(24))
    current_hour = datetime.now().hour
    volumes = []
    for h in hours:
        if h <= current_hour:
            base = 150 if 9 <= h <= 18 else 50
            volumes.append(base + random.randint(-30, 50))
        else:
            volumes.append(0)
    return pd.DataFrame({'Hour': [f'{h:02d}:00' for h in hours], 'Calls': volumes})

def get_daily_trends(days=7):
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days-1, -1, -1)]
    data = []
    for date in dates:
        total = random.randint(5500, 7500)
        contained = int(total * random.uniform(0.68, 0.78))
        data.append({
            'Date': date, 'Total Calls': total, 'AI Resolved': contained,
            'Escalated': total - contained, 'Containment Rate': (contained / total) * 100
        })
    return pd.DataFrame(data)

def get_resolution_breakdown():
    return pd.DataFrame({
        'Category': ['AI Resolved', 'Human Escalation', 'Abandoned', 'Transferred'],
        'Count': [random.randint(3000, 4000), random.randint(800, 1200), random.randint(100, 200), random.randint(50, 150)]
    })

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_metric_card(label, value, delta=None, suffix="", is_inverse=False):
    delta_html = ""
    if delta is not None:
        delta_class = "metric-delta-positive" if (delta >= 0 and not is_inverse) or (delta < 0 and is_inverse) else "metric-delta-negative"
        delta_sign = "+" if delta >= 0 else ""
        delta_html = f'<div class="{delta_class}">{delta_sign}{delta:.1f}{suffix} vs yesterday</div>'
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_metric_card_tv(label, value, suffix="", color="#F59E0B"):
    st.markdown(f"""
        <div class="metric-card-tv">
            <div class="metric-label-tv">{label}</div>
            <div class="metric-value-tv" style="color: {color};">{value}{suffix}</div>
        </div>
    """, unsafe_allow_html=True)

def render_progress_bar(value, max_value=100, color="#F59E0B"):
    percentage = min((value / max_value) * 100, 100)
    st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%; background: {color};"></div>
        </div>
    """, unsafe_allow_html=True)

def create_gauge_chart(value, title, target=None, max_val=100):
    color = "#10B981" if value >= (target or 70) else "#F59E0B" if value >= (target or 70) * 0.9 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=value,
        number={'suffix': '%', 'font': {'size': 36, 'color': '#FFFFFF'}},
        delta={'reference': target, 'relative': False, 'position': 'bottom'} if target else None,
        title={'text': title, 'font': {'size': 16, 'color': '#E2E8F0'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': '#475569', 'tickfont': {'color': '#E2E8F0'}},
            'bar': {'color': color}, 'bgcolor': '#1E293B', 'borderwidth': 2, 'bordercolor': '#475569',
            'steps': [
                {'range': [0, target * 0.9] if target else [0, 60], 'color': '#374151'},
                {'range': [target * 0.9, target] if target else [60, 80], 'color': '#374151'},
                {'range': [target, max_val] if target else [80, 100], 'color': '#1F2937'}
            ],
            'threshold': {'line': {'color': '#F59E0B', 'width': 3}, 'thickness': 0.8, 'value': target} if target else None
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#FFFFFF'})
    return fig

def create_donut_chart(df, names_col, values_col):
    colors = {'Telugu': '#F59E0B', 'Hindi': '#3B82F6', 'English': '#10B981', 'AI Resolved': '#10B981', 'Human Escalation': '#3B82F6', 'Abandoned': '#EF4444', 'Transferred': '#F59E0B'}
    color_list = [colors.get(name, '#94A3B8') for name in df[names_col]]
    fig = go.Figure(data=[go.Pie(labels=df[names_col], values=df[values_col], hole=0.6, marker_colors=color_list, textinfo='label+percent', textposition='outside', textfont={'color': '#FFFFFF', 'size': 12})])
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, font={'color': '#FFFFFF'})
    return fig

def create_bar_chart(df, x_col, y_col):
    fig = go.Figure(data=[go.Bar(x=df[y_col], y=df[x_col], orientation='h', marker_color='#F59E0B', text=df[y_col], textposition='outside', textfont={'color': '#FFFFFF'})])
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, yaxis={'showgrid': False, 'tickfont': {'color': '#E2E8F0'}}, font={'color': '#FFFFFF'})
    return fig

def create_line_chart(df, x_col, y_col, title=""):
    fig = go.Figure(data=[go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers', line=dict(color='#F59E0B', width=3), marker=dict(size=8, color='#F59E0B'), fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.1)')])
    fig.update_layout(title=dict(text=title, font=dict(size=16, color='#FFFFFF'), x=0.5), height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, yaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, font={'color': '#FFFFFF'})
    return fig

def create_area_chart(df, x_col, y_cols):
    colors = ['#10B981', '#3B82F6']
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(x=df[x_col], y=df[col], mode='lines', name=col, stackgroup='one', line=dict(color=colors[i]), fillcolor=colors[i] + '99'))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, yaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font={'color': '#FFFFFF'}), font={'color': '#FFFFFF'})
    return fig

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Telangana_State_Electricity_Regulatory_Commission_logo.png/220px-Telangana_State_Electricity_Regulatory_Commission_logo.png", width=80)
    st.title("TGSPDCL")
    st.caption("AI Voice Agent Dashboard")
    st.divider()
    
    display_mode = st.radio("📺 Display Mode", ["Desktop", "TV Display"], help="TV Display mode shows larger metrics")
    st.divider()
    
    st.subheader("📅 Date Range")
    date_option = st.radio("Select period", ["Today", "Last 7 Days", "Custom Range"], label_visibility="collapsed")
    if date_option == "Custom Range":
        scol1, scol2 = st.columns(2)
        with scol1:
            start_date = st.date_input("From", datetime.now() - timedelta(days=7))
        with scol2:
            end_date = st.date_input("To", datetime.now())
    st.divider()
    
    auto_refresh = st.toggle("🔄 Auto Refresh (30s)", value=True)
    if auto_refresh:
        st.caption("Dashboard refreshes automatically")
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()
    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# =============================================================================
# MAIN CONTENT
# =============================================================================

st.markdown("""
    <h1 style='color: #FFFFFF; margin-bottom: 0;'>⚡ TGSPDCL Voice Agent Dashboard</h1>
    <p style='color: #E2E8F0; font-size: 16px;'>Executive Monitoring Dashboard | Real-time AI Performance Tracking</p>
""", unsafe_allow_html=True)

# =============================================================================
# TV DISPLAY MODE
# =============================================================================

if display_mode == "TV Display":
    st.markdown("---")
    live_metrics = get_live_metrics()
    kpis = get_performance_kpis()
    
    tvcol1, tvcol2, tvcol3 = st.columns(3)
    with tvcol1:
        render_metric_card_tv("Active Calls", live_metrics['active_calls'], color="#3B82F6")
    with tvcol2:
        render_metric_card_tv("Calls Today", f"{live_metrics['calls_today']:,}", color="#F59E0B")
    with tvcol3:
        render_metric_card_tv("Queue", live_metrics['calls_queue'], color="#EF4444" if live_metrics['calls_queue'] > 20 else "#10B981")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tvcol4, tvcol5, tvcol6 = st.columns(3)
    with tvcol4:
        color = "#10B981" if kpis['containment_rate'] >= 70 else "#F59E0B"
        render_metric_card_tv("Containment Rate", f"{kpis['containment_rate']:.1f}", suffix="%", color=color)
    with tvcol5:
        color = "#10B981" if kpis['fcr_rate'] >= 70 else "#F59E0B"
        render_metric_card_tv("First Call Resolution", f"{kpis['fcr_rate']:.1f}", suffix="%", color=color)
    with tvcol6:
        color = "#10B981" if kpis['avg_handle_time'] <= 8 else "#F59E0B"
        render_metric_card_tv("Avg Handle Time", f"{kpis['avg_handle_time']:.1f}", suffix=" min", color=color)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tvcol7, tvcol8, tvcol9 = st.columns(3)
    with tvcol7:
        st.markdown("<p style='text-align:center;color:#E2E8F0;'>Target: 70%</p>", unsafe_allow_html=True)
        render_progress_bar(kpis['containment_rate'], 100, "#10B981" if kpis['containment_rate'] >= 70 else "#F59E0B")
    with tvcol8:
        st.markdown("<p style='text-align:center;color:#E2E8F0;'>Target: 70%</p>", unsafe_allow_html=True)
        render_progress_bar(kpis['fcr_rate'], 100, "#10B981" if kpis['fcr_rate'] >= 70 else "#F59E0B")
    with tvcol9:
        st.markdown("<p style='text-align:center;color:#E2E8F0;'>Target: ≤8 min</p>", unsafe_allow_html=True)
        render_progress_bar(8 - kpis['avg_handle_time'] + 8, 16, "#10B981" if kpis['avg_handle_time'] <= 8 else "#F59E0B")

# =============================================================================
# DESKTOP MODE
# =============================================================================

else:
    tab1, tab2 = st.tabs(["📊 Live Operations", "📈 Performance KPIs"])
    
    with tab1:
        live_metrics = get_live_metrics()
        language_dist = get_language_distribution()
        top_intents = get_top_intents()
        
        st.markdown('<div class="section-header">📡 Current Status</div>', unsafe_allow_html=True)
        
        lcol1, lcol2, lcol3 = st.columns(3)
        with lcol1:
            render_metric_card("Active Calls", live_metrics['active_calls'], delta=random.randint(-15, 25))
        with lcol2:
            render_metric_card("Calls Today", f"{live_metrics['calls_today']:,}", delta=random.randint(-5, 8), suffix="%")
        with lcol3:
            render_metric_card("Queue Size", live_metrics['calls_queue'], delta=random.randint(-8, 12), is_inverse=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown('<div class="section-header">🌐 Language Distribution</div>', unsafe_allow_html=True)
            fig = create_donut_chart(language_dist, 'Language', 'Percentage')
            st.plotly_chart(fig, use_container_width=True)
            for _, row in language_dist.iterrows():
                lcola, lcolb = st.columns([3, 1])
                with lcola:
                    st.markdown(f"**{row['Language']}**")
                with lcolb:
                    st.markdown(f"{row['Percentage']:.1f}%")
        
        with right_col:
            st.markdown('<div class="section-header">🎯 Top Customer Intents</div>', unsafe_allow_html=True)
            fig = create_bar_chart(top_intents, 'Intent', 'Count')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📈 Hourly Call Volume (Today)</div>', unsafe_allow_html=True)
        hourly_data = get_hourly_call_volume()
        fig = create_line_chart(hourly_data, 'Hour', 'Calls')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        kpis = get_performance_kpis()
        daily_trends = get_daily_trends(7 if date_option == "Last 7 Days" else 30 if date_option == "Custom Range" else 1)
        resolution_data = get_resolution_breakdown()
        
        st.markdown('<div class="section-header">🎯 Key Performance Indicators</div>', unsafe_allow_html=True)
        
        kcol1, kcol2, kcol3 = st.columns(3)
        with kcol1:
            fig = create_gauge_chart(kpis['containment_rate'], "Containment Rate", target=70)
            st.plotly_chart(fig, use_container_width=True)
            delta = kpis['containment_rate'] - kpis['containment_yesterday']
            st.markdown(f"<p style='text-align:center;color:{'#10B981' if delta >= 0 else '#EF4444'};font-weight:500;'>{'↑' if delta >= 0 else '↓'} {abs(delta):.1f}% vs yesterday</p>", unsafe_allow_html=True)
        
        with kcol2:
            fig = create_gauge_chart(kpis['fcr_rate'], "First Call Resolution", target=70)
            st.plotly_chart(fig, use_container_width=True)
            delta = kpis['fcr_rate'] - kpis['fcr_yesterday']
            st.markdown(f"<p style='text-align:center;color:{'#10B981' if delta >= 0 else '#EF4444'};font-weight:500;'>{'↑' if delta >= 0 else '↓'} {abs(delta):.1f}% vs yesterday</p>", unsafe_allow_html=True)
        
        with kcol3:
            aht_score = max(0, 100 - (kpis['avg_handle_time'] / 12) * 100)
            fig = create_gauge_chart(aht_score, f"Avg Handle Time: {kpis['avg_handle_time']:.1f} min", target=66.7)
            st.plotly_chart(fig, use_container_width=True)
            delta = kpis['aht_yesterday'] - kpis['avg_handle_time']
            st.markdown(f"<p style='text-align:center;color:{'#10B981' if delta >= 0 else '#EF4444'};font-weight:500;'>{'↓' if delta >= 0 else '↑'} {abs(delta):.1f} min vs yesterday</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 Today vs Yesterday</div>', unsafe_allow_html=True)
        
        ccol1, ccol2, ccol3 = st.columns(3)
        with ccol1:
            change = ((kpis['calls_today'] - kpis['calls_yesterday']) / kpis['calls_yesterday']) * 100
            render_metric_card("Total Calls", f"{kpis['calls_today']:,}", delta=change, suffix="%")
        
        with ccol2:
            ai_resolved = int(kpis['calls_today'] * kpis['containment_rate'] / 100)
            ai_yesterday = int(kpis['calls_yesterday'] * kpis['containment_yesterday'] / 100)
            change = ((ai_resolved - ai_yesterday) / ai_yesterday) * 100 if ai_yesterday > 0 else 0
            render_metric_card("AI Resolved", f"{ai_resolved:,}", delta=change, suffix="%")
        
        with ccol3:
            escalated = kpis['calls_today'] - ai_resolved
            esc_yesterday = kpis['calls_yesterday'] - ai_yesterday
            change = ((escalated - esc_yesterday) / esc_yesterday) * 100 if esc_yesterday > 0 else 0
            render_metric_card("Escalated", f"{escalated:,}", delta=change, suffix="%", is_inverse=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        chcol1, chcol2 = st.columns(2)
        with chcol1:
            st.markdown('<div class="section-header">📈 Call Volume Trend</div>', unsafe_allow_html=True)
            if len(daily_trends) > 1:
                fig = create_line_chart(daily_trends, 'Date', 'Total Calls')
            else:
                fig = create_line_chart(get_hourly_call_volume(), 'Hour', 'Calls', "Today's Hourly Volume")
            st.plotly_chart(fig, use_container_width=True)
        
        with chcol2:
            st.markdown('<div class="section-header">🥧 Resolution Breakdown</div>', unsafe_allow_html=True)
            if len(daily_trends) > 1:
                fig = create_area_chart(daily_trends, 'Date', ['AI Resolved', 'Escalated'])
            else:
                fig = create_donut_chart(resolution_data, 'Category', 'Count')
            st.plotly_chart(fig, use_container_width=True)
        
        if len(daily_trends) > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Containment Rate Trend</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_trends['Date'], y=daily_trends['Containment Rate'], mode='lines+markers', name='Containment Rate', line=dict(color='#F59E0B', width=3), marker=dict(size=10)))
            fig.add_hline(y=70, line_dash="dash", line_color="#10B981", annotation_text="Target: 70%", annotation_position="right", annotation=dict(font_color="#10B981"))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'showgrid': True, 'gridcolor': '#334155', 'tickfont': {'color': '#E2E8F0'}}, yaxis={'showgrid': True, 'gridcolor': '#334155', 'range': [50, 100], 'tickfont': {'color': '#E2E8F0'}}, font={'color': '#FFFFFF'})
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# AUTO-REFRESH
# =============================================================================

if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()
