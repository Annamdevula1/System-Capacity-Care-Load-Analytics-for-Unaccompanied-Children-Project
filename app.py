import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="UAC Care Load Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F4F7FB; color: #172033; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #101D35; }
[data-testid="stSidebar"] * { color: #F4F7FB !important; }
[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E5EAF2; padding: 18px 18px;
    border-radius: 14px; box-shadow: 0 3px 12px rgba(20,35,60,.04);
}
[data-testid="stMetricLabel"] { color: #64748B !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #14213D !important; font-family: 'Manrope', sans-serif; }
h1, h2, h3 { font-family: 'Manrope', sans-serif; color: #14213D; }
.hero {
    background: linear-gradient(120deg, #14213D 0%, #1D4772 100%);
    border-radius: 18px; padding: 26px 30px; color: white; margin-bottom: 22px;
}
.hero h1 { color: white; font-size: 2rem; margin: 0 0 6px 0; }
.hero p { color: #D9E7F6; margin: 0; font-size: 1rem; }
.section-note { color: #64748B; font-size: .9rem; }
div[data-testid="stTabs"] button { font-weight: 700; }
.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------- Dataset schema ----------
DATE = "Date"
CBP_INTAKE = "Children apprehended and placed in CBP custody"
CBP_LOAD = "Children in CBP custody"
TRANSFER = "Children transferred out of CBP custody"
HHS_LOAD = "Children in HHS Care"
DISCHARGE = "Children discharged from HHS Care"

REQUIRED = [DATE, CBP_INTAKE, CBP_LOAD, TRANSFER, HHS_LOAD, DISCHARGE]

def clean_numeric(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )

def prepare_data(raw):
    data = raw.copy()
    missing_cols = [c for c in REQUIRED if c not in data.columns]
    if missing_cols:
        raise ValueError("Missing required columns: " + ", ".join(missing_cols))

    data[DATE] = pd.to_datetime(data[DATE], errors="coerce")
    for col in REQUIRED[1:]:
        data[col] = clean_numeric(data[col])

    data = data.dropna(subset=[DATE]).sort_values(DATE)
    data["Total System Load"] = data[CBP_LOAD] + data[HHS_LOAD]
    data["Net Daily Intake"] = data[TRANSFER] - data[DISCHARGE]
    data["Care Load Growth Rate (%)"] = data["Total System Load"].pct_change() * 100
    data["7-Day Average"] = data["Total System Load"].rolling(7, min_periods=1).mean()
    data["14-Day Average"] = data["Total System Load"].rolling(14, min_periods=1).mean()
    data["7-Day Net Intake"] = data["Net Daily Intake"].rolling(7, min_periods=1).sum()
    return data

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <h1>UAC Healthcare Capacity &amp; Care Load Analytics</h1>
  <p>Operational visibility across CBP custody, HHS care, transfers and sponsor discharges</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## UAC Analytics")
    st.caption("Data-driven operational monitoring")
    st.markdown("---")
    st.markdown("### Dashboard controls")

# ---------- Automatic CSV Loading ----------
try:
    raw_df = pd.read_csv("UAC_Final_Cleaned_Data.csv")

    raw_df.columns = (
        raw_df.columns
        .str.strip()
        .str.replace("*", "", regex=False)
    )

    df = prepare_data(raw_df)

except Exception as e:
    st.error(f"Could not read this dataset: {e}")
    st.stop()

if df.empty:
    st.error("No usable rows were found. Check the Date column and the CSV file.")
    st.stop()

min_date = df[DATE].min().date()
max_date = df[DATE].max().date()

with st.sidebar:
    selected_dates = st.date_input(
        "Reporting date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    granularity = st.selectbox("Time granularity", ["Daily", "Weekly", "Monthly"])
    show_rolling = st.toggle("Show rolling averages", value=True)
    selected_metrics = st.multiselect(
        "Load metrics",
        ["CBP Custody", "HHS Care", "Total System Load"],
        default=["CBP Custody", "HHS Care", "Total System Load"]
    )

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df[DATE].dt.date >= start_date) &
    (df[DATE].dt.date <= end_date)
].copy()

if filtered.empty:
    st.warning("No records are available for the selected date range.")
    st.stop()

# ---------- KPI calculations ----------
latest = filtered.iloc[-1]
avg_load = filtered["Total System Load"].mean()
peak_load = filtered["Total System Load"].max()
net_total = filtered["Net Daily Intake"].sum()
volatility = filtered["Total System Load"].diff().std()
discharges_total = filtered[DISCHARGE].sum()
transfers_total = filtered[TRANSFER].sum()
discharge_offset = (discharges_total / transfers_total * 100) if transfers_total else np.nan

st.subheader("System load overview")
st.markdown(f"<div class='section-note'>Selected period: {start_date:%d %b %Y} — {end_date:%d %b %Y} · {len(filtered):,} recorded days</div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
# Care Load Growth Rate KPI
growth_rate = latest["Care Load Growth Rate (%)"]

st.metric(
    "Care Load Growth Rate",
    f"{growth_rate:.2f}%" if pd.notna(growth_rate) else "N/A"
)
k1.metric("Current recorded system load", f"{latest['Total System Load']:,.0f}")
k2.metric("Average system load", f"{avg_load:,.0f}")
k3.metric("Peak system load", f"{peak_load:,.0f}")
k4.metric("Net intake pressure", f"{net_total:,.0f}")

k5, k6, k7, k8 = st.columns(4)
k5.metric("CBP custody · latest", f"{latest[CBP_LOAD]:,.0f}")
k6.metric("HHS care · latest", f"{latest[HHS_LOAD]:,.0f}")
k7.metric("Care-load volatility", f"{volatility:,.1f}" if pd.notna(volatility) else "N/A")
k8.metric("Discharge offset ratio", f"{discharge_offset:.1f}%" if pd.notna(discharge_offset) else "N/A")

# ---------- Time aggregation ----------
def aggregate(frame, gran):
    temp = frame.set_index(DATE)
    if gran == "Weekly":
        return temp.resample("W").agg({
            CBP_LOAD: "mean", HHS_LOAD: "mean",
            "Total System Load": "mean", "Net Daily Intake": "sum",
            "7-Day Average": "mean", "14-Day Average": "mean",
            "7-Day Net Intake": "mean"
        }).dropna(how="all").reset_index()
    if gran == "Monthly":
        return temp.resample("MS").agg({
            CBP_LOAD: "mean", HHS_LOAD: "mean",
            "Total System Load": "mean", "Net Daily Intake": "sum",
            "7-Day Average": "mean", "14-Day Average": "mean",
            "7-Day Net Intake": "mean"
        }).dropna(how="all").reset_index()
    return frame.copy()

plot_df = aggregate(filtered, granularity)
x_title = "Date"

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "System overview",
    "CBP & HHS comparison",
    "Intake & backlog",
    "Data quality",
    "Growth & Forecast"
])
with tab1:
    st.markdown("### Total system care load")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plot_df[DATE], y=plot_df["Total System Load"],
        mode="lines", name="Total system load",
        line=dict(width=3, color="#2463A6")
    ))
    if show_rolling:
        fig.add_trace(go.Scatter(
            x=plot_df[DATE], y=plot_df["7-Day Average"],
            mode="lines", name="7-day average",
            line=dict(width=2, color="#E59A36", dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=plot_df[DATE], y=plot_df["14-Day Average"],
            mode="lines", name="14-day average",
            line=dict(width=2, color="#299D8F", dash="dot")
        ))
    fig.update_layout(
        template="plotly_white", height=430, hovermode="x unified",
        xaxis_title=x_title, yaxis_title="Children",
        legend_title="", margin=dict(l=10, r=10, t=25, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    threshold = filtered["Total System Load"].quantile(.90)
    high_days = filtered[filtered["Total System Load"] >= threshold]
    st.markdown("### High-load monitoring")
    a, b = st.columns(2)
    a.metric("90th percentile reference", f"{threshold:,.0f}")
    b.metric("Days at/above reference", f"{len(high_days):,}")
    st.caption("The 90th percentile is a dataset-based high-load reference, not an official facility capacity limit.")

with tab2:
    st.markdown("### CBP custody compared with HHS care")
    fig = go.Figure()
    if "CBP Custody" in selected_metrics:
        fig.add_trace(go.Scatter(x=plot_df[DATE], y=plot_df[CBP_LOAD], name="CBP custody", mode="lines", line=dict(width=2.5, color="#2463A6")))
    if "HHS Care" in selected_metrics:
        fig.add_trace(go.Scatter(x=plot_df[DATE], y=plot_df[HHS_LOAD], name="HHS care", mode="lines", line=dict(width=2.5, color="#299D8F")))
    if "Total System Load" in selected_metrics:
        fig.add_trace(go.Scatter(x=plot_df[DATE], y=plot_df["Total System Load"], name="Total system load", mode="lines", line=dict(width=2.5, color="#E59A36")))
    fig.update_layout(template="plotly_white", height=430, hovermode="x unified", xaxis_title=x_title, yaxis_title="Children", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Latest recorded care distribution")
    pie = px.pie(
        names=["CBP custody", "HHS care"],
        values=[latest[CBP_LOAD], latest[HHS_LOAD]],
        hole=.62,
        color_discrete_sequence=["#2463A6", "#299D8F"]
    )
    pie.update_layout(template="plotly_white", height=330, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(pie, use_container_width=True)

with tab3:
    st.markdown("### Transfers into HHS and HHS discharges")
    flow = go.Figure()
    flow.add_trace(go.Scatter(x=filtered[DATE], y=filtered[TRANSFER], name="Transfers out of CBP", mode="lines", line=dict(color="#2463A6", width=2)))
    flow.add_trace(go.Scatter(x=filtered[DATE], y=filtered[DISCHARGE], name="HHS discharges", mode="lines", line=dict(color="#299D8F", width=2)))
    flow.update_layout(template="plotly_white", height=390, hovermode="x unified", xaxis_title="Date", yaxis_title="Children", legend_title="")
    st.plotly_chart(flow, use_container_width=True)

    st.markdown("### Net daily intake")
    net_fig = px.bar(plot_df, x=DATE, y="Net Daily Intake", template="plotly_white")
    net_fig.update_traces(marker_color="#2463A6")
    net_fig.update_layout(height=330, xaxis_title=x_title, yaxis_title="Transfers − discharges")
    st.plotly_chart(net_fig, use_container_width=True)

    st.markdown("### 7-day cumulative net intake indicator")
    backlog_fig = px.line(filtered, x=DATE, y="7-Day Net Intake", template="plotly_white")
    backlog_fig.update_traces(line_color="#D18A32", line_width=2.5)
    backlog_fig.update_layout(height=330, xaxis_title="Date", yaxis_title="7-day net intake")
    st.plotly_chart(backlog_fig, use_container_width=True)
    st.caption("This is a rolling flow-imbalance indicator, not a verified count of children waiting in a queue.")

with tab4:
    st.markdown("### Dataset integrity checks")
    full_dates = pd.date_range(df[DATE].min(), df[DATE].max(), freq="D")
    missing_dates = full_dates.difference(pd.DatetimeIndex(df[DATE].drop_duplicates()))
    duplicate_dates = int(df[DATE].duplicated().sum())
    missing_cells = int(raw_df[REQUIRED].isna().sum().sum())
    transfer_anomalies = filtered[filtered[TRANSFER] > filtered[CBP_LOAD]]
    discharge_anomalies = filtered[filtered[DISCHARGE] > filtered[HHS_LOAD]]

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Missing calendar dates", f"{len(missing_dates):,}")
    q2.metric("Duplicate date rows", f"{duplicate_dates:,}")
    q3.metric("Rows: transfer > CBP load", f"{len(transfer_anomalies):,}")
    q4.metric("Rows: discharge > HHS load", f"{len(discharge_anomalies):,}")

    st.warning("Data-quality flags are displayed for review. The dashboard does not silently replace missing dates with zero or delete flagged records.")
    if len(missing_dates):
        with st.expander("View missing calendar dates"):
            st.dataframe(pd.DataFrame({"Missing date": missing_dates}), use_container_width=True, hide_index=True)
    if len(transfer_anomalies):
        with st.expander("View transfer validation flags"):
            st.dataframe(transfer_anomalies[[DATE, CBP_LOAD, TRANSFER]], use_container_width=True, hide_index=True)
    if len(discharge_anomalies):
        with st.expander("View discharge validation flags"):
            st.dataframe(discharge_anomalies[[DATE, HHS_LOAD, DISCHARGE]], use_container_width=True, hide_index=True)

    st.markdown("### Filtered records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
# ---------- Growth & Forecast ----------
with tab5:

    st.markdown("### Early vs Late Timeline Comparison")

    mid = len(df) // 2

    early = df.iloc[:mid]
    late = df.iloc[mid:]

    comparison = pd.DataFrame({
        "Period": ["Early Period", "Late Period"],
        "Average System Load": [
            early["Total System Load"].mean(),
            late["Total System Load"].mean()
        ]
    })

    fig = px.bar(
        comparison,
        x="Period",
        y="Average System Load",
        color="Period",
        title="Early vs Late Average Care Load",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # High Load Period Detection
    st.markdown("### Prolonged High-Load Detection")

    threshold = df["Total System Load"].quantile(0.90)

    high_load = df[
        df["Total System Load"] >= threshold
    ].copy()

    high_load["High Load Group"] = (
        high_load[DATE].diff().dt.days.ne(1)
    ).cumsum()

    prolonged = (
        high_load.groupby("High Load Group")
        .filter(lambda x: len(x) >= 7)
    )

    st.metric(
        "Prolonged High-Load Days",
        len(prolonged)
    )

    st.caption(
        "High load is identified using the dataset's "
        "90th percentile reference and a minimum of 7 "
        "consecutive recorded high-load days."
    )

    if not prolonged.empty:
        st.dataframe(
            prolonged[[DATE, "Total System Load"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No prolonged high-load period detected.")

    # Forecasting
    st.markdown("### 14-Day Care Load Trend Projection")

    forecast_data = (
        df[["Total System Load"]]
        .dropna()
        .tail(30)
    )

    if len(forecast_data) >= 7:

        x = np.arange(len(forecast_data))
        y = forecast_data["Total System Load"].values

        coefficients = np.polyfit(x, y, 1)

        future_x = np.arange(
            len(forecast_data),
            len(forecast_data) + 14
        )

        predicted = np.polyval(
            coefficients, future_x
        )

        future_dates = pd.date_range(
            start=df[DATE].max() + pd.Timedelta(days=1),
            periods=14,
            freq="D"
        )

        forecast_df = pd.DataFrame({
            "Date": future_dates,
            "Projected System Load": np.maximum(predicted, 0)
        })

        fig = px.line(
            forecast_df,
            x="Date",
            y="Projected System Load",
            title="14-Day Linear Trend Projection",
            template="plotly_white"
        )

        fig.update_traces(
            line=dict(dash="dash", width=3)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            forecast_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Illustrative linear trend projection based on "
            "the last 30 available observations. "
            "Not an official capacity forecast."
        )

    else:
        st.warning(
            "Insufficient historical data for projection."
        )

# ---------- Export ----------
st.markdown("---")
st.subheader("Download dashboard data")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered analytics CSV",
    data=csv,
    file_name="UAC_Dashboard_Filtered_Analytics.csv",
    mime="text/csv"
)
st.caption("Decision-support analytics only. Values describe the uploaded dataset and should be interpreted with source-data limitations.")
