# TGSPDCL AI Voice Agent - Executive Dashboard

## Overview

This dashboard provides real-time monitoring of the TGSPDCL AI Voice Agent system for management and executives. It offers a clear view of operational performance, customer service metrics, and AI effectiveness.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/tgspdcl-executive-dashboard.git
cd tgspdcl-executive-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select this repository
5. Set `app.py` as the main file
6. Click "Deploy"

---

## 📊 Features

### Display Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **Desktop** | Full-featured view with tabs and detailed charts | Day-to-day monitoring |
| **TV Display** | Large metrics optimized for wall-mounted screens | Control room, lobby display |

### Tab 1: Live Operations

| Component | Description | Update Frequency |
|-----------|-------------|------------------|
| Active Calls | Current concurrent calls being handled | Real-time |
| Calls Today | Total calls processed since midnight | Real-time |
| Queue Size | Customers waiting to connect | Real-time |
| Capacity Utilization | Percentage of system capacity in use | Real-time |
| Language Distribution | Donut chart showing Telugu/Hindi/English split | 5 minutes |
| Top Customer Intents | Horizontal bar chart of top 5 call reasons | 5 minutes |
| Hourly Call Volume | Line chart showing call pattern throughout the day | 5 minutes |

### Tab 2: Performance KPIs

| Component | Description | Target |
|-----------|-------------|--------|
| Containment Rate | Percentage of calls fully resolved by AI | ≥70% |
| First Call Resolution (FCR) | Percentage of issues resolved in single interaction | ≥70% |
| Average Handle Time (AHT) | Mean duration per call | ≤8 minutes |
| Today vs Yesterday | Comparative metrics showing improvement/decline | - |
| Call Volume Trend | Line chart of daily call volumes | - |
| Resolution Breakdown | Area chart showing AI vs Human resolution split | - |
| Containment Rate Trend | Line chart with target threshold line | - |

---

## 📐 Formulas & Calculations

### 1. Containment Rate

```
Containment Rate = (Calls Fully Resolved by AI / Total Calls) × 100
```

**Definition**: A call is "contained" when the AI agent successfully addresses the customer's query without any human intervention.

**Example**:
- Total Calls Today: 5,000
- AI Resolved (no human touch): 3,500
- Containment Rate = (3,500 / 5,000) × 100 = **70%**

### 2. First Call Resolution (FCR)

```
FCR = (Issues Resolved in Single Call / Total Issues Raised) × 100
```

**Definition**: Measures whether the customer's issue was completely resolved during the first interaction, with no need for callbacks or follow-ups.

**Example**:
- Total Issues: 4,000
- Resolved in First Call: 2,800
- FCR = (2,800 / 4,000) × 100 = **70%**

### 3. Average Handle Time (AHT)

```
AHT = Total Handling Time / Number of Calls Handled
```

**Components**:
- Talk Time (customer speaking + AI responding)
- Hold Time (if any)
- After-Call Work (ticket creation, system updates)

**Example**:
- Total Handling Time: 30,000 minutes
- Calls Handled: 5,000
- AHT = 30,000 / 5,000 = **6 minutes**

### 4. Capacity Utilization

```
Capacity Utilization = (Active Concurrent Calls / Maximum Capacity) × 100
```

**System Capacity**: 300 concurrent calls (as per requirements)

**Example**:
- Active Calls: 180
- Max Capacity: 300
- Utilization = (180 / 300) × 100 = **60%**

### 5. Cost Savings

```
Daily Cost Savings = AI Resolved Calls × Cost Per Human-Handled Call
```

**Assumptions**:
- Cost per human-handled call: ₹50 (includes agent salary, infrastructure, supervision)
- Each AI-resolved call saves ₹50

**Example**:
- AI Resolved Today: 3,500 calls
- Cost Savings = 3,500 × ₹50 = **₹1,75,000/day**

---

## 🗃️ Data Sources

### Production Integration

| Metric | Data Source | Query/API |
|--------|-------------|-----------|
| Active Calls | Redis Session Store | `KEYS session:*` count |
| Calls Today | PostgreSQL | `SELECT COUNT(*) FROM call_sessions WHERE date = TODAY` |
| Queue Size | Redis | `LLEN call_queue` |
| Language Distribution | PostgreSQL | `SELECT language, COUNT(*) FROM call_sessions GROUP BY language` |
| Top Intents | PostgreSQL | `SELECT intent, COUNT(*) FROM intent_analytics GROUP BY intent ORDER BY count DESC LIMIT 5` |
| Containment Rate | PostgreSQL | `SELECT (SUM(CASE WHEN escalated = false THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) FROM call_sessions` |
| FCR | PostgreSQL | `SELECT (SUM(CASE WHEN fcr = true THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) FROM call_sessions` |
| AHT | PostgreSQL | `SELECT AVG(duration_seconds) / 60 FROM call_sessions` |

### Current Implementation

The dashboard currently uses **mock data generators** for demonstration. To connect to production:

1. Replace functions in the `get_*` methods with actual database queries
2. Configure database connection strings via Streamlit secrets
3. Add Redis connection for real-time metrics

Example production connection:

```python
import redis
import psycopg2

# Redis for real-time metrics
redis_client = redis.Redis(host='redis.internal', port=6379, db=0)

# PostgreSQL for historical data
conn = psycopg2.connect(st.secrets["postgres"]["connection_string"])

def get_active_calls():
    return len(redis_client.keys('session:*'))
```

---

## 🎨 Design Rationale

### Color Scheme

| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Amber) | `#F59E0B` | Highlights, accents, primary actions |
| Background | `#0F172A` | Main background (dark mode) |
| Card Background | `#1E293B` | Cards, panels |
| Success | `#10B981` | Positive metrics, targets met |
| Warning | `#F59E0B` | Approaching thresholds |
| Danger | `#EF4444` | Below targets, alerts |
| Text Primary | `#F1F5F9` | Main text |
| Text Secondary | `#94A3B8` | Labels, captions |

### Language Colors

| Language | Color | Rationale |
|----------|-------|-----------|
| Telugu | `#F59E0B` (Amber) | Primary language, highest visibility |
| Hindi | `#3B82F6` (Blue) | Secondary language |
| English | `#10B981` (Green) | Tertiary language |

### TV Display Mode

**Design Decisions**:
- **Large fonts (72px)**: Visible from 15+ feet away
- **High contrast**: Bright text on dark background
- **6 metrics maximum**: Reduces cognitive load
- **Progress bars**: Quick visual comparison against targets
- **Auto-refresh**: 30-second interval for real-time updates

---

## 🔧 Configuration

### Streamlit Secrets

For production deployment, create `.streamlit/secrets.toml`:

```toml
[postgres]
connection_string = "postgresql://user:pass@host:5432/tgspdcl"

[redis]
host = "redis.internal"
port = 6379
password = "your_redis_password"

[settings]
refresh_interval = 30
```

### Environment Variables

```bash
export TGSPDCL_DB_HOST=localhost
export TGSPDCL_DB_PORT=5432
export TGSPDCL_REDIS_HOST=localhost
```

---

## 📁 File Structure

```
executive-dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🔄 Update Frequency

| Metric Type | Refresh Rate | Rationale |
|-------------|--------------|-----------|
| Real-time (Active calls, Queue) | 30 seconds | Immediate operational awareness |
| Aggregated (Today's totals) | 5 minutes | Balance between freshness and load |
| Historical (Trends, Charts) | 15 minutes | Less volatile data |

---

## 📱 Responsive Design

The dashboard is optimized for:

| Device | Resolution | Layout |
|--------|------------|--------|
| Desktop | 1920×1080+ | Full features, all charts visible |
| Laptop | 1366×768 | Scrollable, all features accessible |
| Tablet | 1024×768 | Stacked columns, touch-friendly |
| TV Display | 1920×1080+ | Large metrics only, minimal UI |

---

## 🛡️ Security Considerations

1. **No PII Displayed**: Dashboard shows aggregated metrics only
2. **Read-Only Access**: No data modification capabilities
3. **Authentication**: Integrate with Streamlit authentication for production
4. **Rate Limiting**: Mock data prevents database overload in development

---

## 📈 Future Enhancements

- [ ] SSO/LDAP authentication integration
- [ ] Real-time WebSocket connections
- [ ] PDF report generation
- [ ] Email alerts for threshold breaches
- [ ] Mobile-responsive design improvements
- [ ] Dark/Light theme toggle

---

## 📞 Support

For issues or feature requests, contact the TGSPDCL IT team.

---

## 📄 License

This project is developed for TGSPDCL. All rights reserved.
