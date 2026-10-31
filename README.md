# System-Capacity-Care-Load-Analytics-for-Unaccompanied-Children-Project


1. Project Overview

UAC Care Load Analytics is a data analytics  and data science and visualization project designed to monitor the care load across the Unaccompanied Alien Children (UAC) Program.

The project analyzes daily operational data related to children in CBP custody, transfers to HHS care, and discharges from HHS care. It transforms raw data into meaningful insights through interactive visualizations, performance indicators, trend analysis, and illustrative forecasting.

Project Organization: Unified Mentor
Domain: U.S. Department of Health and Human Services (HHS)
Project Type: Healthcare Data Analytics and Visualization

2. Background and Context

The Unaccompanied Alien Children (UAC) Program is a federally mandated initiative under which children apprehended by U.S. Customs and Border Protection (CBP) are transferred to the Department of Health and Human Services (HHS) for medical screening, quarantine, sheltering, and eventual placement with vetted sponsors.

From a healthcare systems perspective, this program functions as a dynamic care pipeline involving:

- Intake into CBP custody
- Transfer to HHS care facilities
- Medical, psychological, and welfare support
- Discharge and reunification with sponsors

Effective functioning of this pipeline depends on accurate capacity awareness and care-load monitoring, especially during sudden influxes.

3. Problem Statement

Although daily operational data is collected, a centralized analytical framework is needed to continuously assess:

- Total care system load
- Balance between inflow and outflow
- Capacity stress and relief periods
- Sustainability of care delivery over time

Without structured analytics, decision-making can become reactive, increasing the risk of overcrowding, delayed care, and strain on healthcare infrastructure.

This project addresses the need by developing an interactive analytics dashboard for monitoring UAC care-load patterns.

4. Project Objectives

Primary Objectives

- Quantify daily and cumulative care load across CBP and HHS.
- Identify periods of potential capacity strain and relief.
- Analyze the balance between intake, transfers, and discharges.

Secondary Objectives

- Support healthcare staffing and shelter planning.
- Improve situational awareness for policymakers.
- Enable data-driven humanitarian response evaluation.

5. Dataset Description

Dataset File: "UAC_Final_Cleaned_Data.csv"

The dataset contains daily time-series records related to the UAC care system.

Column| Description
Date| Reporting date
Children apprehended and placed in CBP custody| Daily intake volume
Children in CBP custody| Active CBP care load
Children transferred out of CBP custody| Flow from CBP into HHS
Children in HHS Care| Active HHS care load
Children discharged from HHS Care| Sponsor placements

The dashboard derives additional analytical metrics from these original dataset columns.

6. Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

7. Methodology

7.1 Data Ingestion and Structuring

- Load the cleaned daily time-series dataset.
- Convert the Date column into datetime format.
- Arrange records in chronological order.
- Prepare data for daily, weekly, and monthly analysis.

7.2 Data Quality and Validation

- Identify missing calendar dates.
- Check for duplicate dates.
- Validate transfers against CBP custody figures.
- Validate discharges against HHS care figures.
- Flag reporting anomalies for transparency.

7.3 Derived Healthcare Capacity Metrics

The dashboard calculates the following metrics:

Total System Load

CBP Custody + HHS Care

Represents the combined number of children under recorded CBP and HHS care.

Net Daily Intake

Transfers from CBP to HHS − HHS Discharges

Indicates the daily balance between transfers into HHS and discharges.

Care Load Growth Rate

Day-over-day percentage change in total system load.

Backlog Indicator

Uses sustained positive net intake as an indicator of potential accumulation of care pressure. The rolling 7-day net intake is used to monitor this imbalance.

7.4 Trend and Temporal Analysis

- Daily, weekly, and monthly care-load trends.
- Rolling 7-day and 14-day averages.
- Identification of high-load periods.
- Early versus late timeline comparison.
- Analysis of changes in care-load patterns.

7.5 Pressure and Stress Identification

- Rolling average analysis.
- Care-load variability analysis.
- Detection of prolonged high-load periods.
- Monitoring of sustained positive net intake.

7.6 Forecasting

A 14-day illustrative linear trend projection is generated using the last 30 available observations.

This projection helps visualize a possible short-term trend. It is not an official forecast of facility capacity or future care requirements.

8. Key Performance Indicators (KPIs)

KPI Name| Description
Total Children Under Care| Combined CBP and HHS care load
Net Intake Pressure| Difference between transfers and discharges
Care Load Volatility Index| Variability in system care load
Backlog Accumulation Indicator| Sustained positive net intake
Discharge Offset Ratio| Discharges as a percentage of transfers
Care Load Growth Rate| Percentage change in total system load

9. Streamlit Web Application

The project includes an interactive Streamlit dashboard with the following modules.

Core Modules

1. System Load Overview

- Current recorded system load
- Average system load
- Peak system load
- Net intake pressure
- Care-load growth rate

2. CBP vs HHS Load Comparison

- CBP custody trends
- HHS care trends
- Total system load comparison
- Latest care distribution

3. Net Intake and Backlog Trends

- Transfers from CBP
- HHS discharges
- Net daily intake
- 7-day cumulative net intake indicator

4. Data Quality

- Missing calendar dates
- Duplicate date records
- Transfer validation flags
- Discharge validation flags

5. Growth and Forecast

- Early versus late timeline comparison
- Prolonged high-load period detection
- 14-day illustrative trend projection

User Capabilities

- Select a reporting date range.
- Choose daily, weekly, or monthly granularity.
- Toggle different care-load metrics.
- Enable or disable rolling averages.
- Download filtered dashboard data as a CSV file.

10. Project Structure

System-Capacity-Care-Load-Analytics-for-Unaccompanied-Children-Project

│
├── app.py
├── UAC_Final_Cleaned_Data.csv
├── requirements.txt
└── README.md
├── Dataset(https://drive.google.com/file/d/1xZo782T4EfnkC0BmCwJTb0DZYYHoOXKm/view)
├── app.py 
├── UAC_Cleaned_Data.csv



11. Expected Output

The application provides:

- Interactive system care-load overview.
- CBP and HHS comparison charts.
- Intake and discharge analysis.
- Data-quality reports.
- Growth and high-load analysis.
- 14-day trend projection.
- Downloadable filtered analytics data.

12. Deliverables

The project deliverables include:

- Research Paper: Exploratory Data Analysis (EDA), insights, and recommendations.
- Streamlit Dashboard: Interactive application for care-load analytics.
- Executive Summary: Key findings and recommendations for government stakeholders.

13. Important Note

The dashboard is designed as an analytical and decision-support tool. Its indicators are based on the uploaded dataset and should be interpreted with the source-data limitations in mind.

The 90th percentile high-load reference is not an official facility capacity limit. The 14-day projection is illustrative and should not be treated as an official operational forecast.

The dashboard does not make individual decisions about children.

14. Conclusion

UAC Care Load Analytics delivers a structured healthcare analytics framework for monitoring the UAC care system.

By translating daily operational counts into meaningful capacity insights, the project helps stakeholders understand care-load patterns, evaluate intake and discharge trends, identify potential periods of increased operational pressure, and support more informed planning.

15. Future Scope

- Advanced time-series forecasting models.
- Improved backlog and capacity-pressure indicators.
- Additional operational performance metrics.
- Interactive location-based analysis, if suitable data becomes available.
- Enhanced reporting and executive summaries.

16. Author

Durga Prasad Annamdevula

BCA Graduate | Data Science and AI/ML Enthusiast

Project Category

Healthcare Analytics | Data Analytics | Python | Streamlit | Data Visualization
