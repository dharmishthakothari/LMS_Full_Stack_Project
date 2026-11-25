# Analytics & Multi-Format Reporting Module

## 1. Overview
Aggregates institute KPIs, enrollment trends, attendance patterns, and revenue collections into executive dashboards with one-click multi-format data exports.

## 2. Technical Specifications
- **Export Formats**:
  - `CSV`: Comma-separated values streaming.
  - `Excel (.xlsx)`: Styled workbook generation via `openpyxl`.
  - `PDF (.pdf)`: High-fidelity tabular document rendering via `reportlab`.
- **Supported Datasets**: Students, Courses, Batches, Attendance, Fees/Revenue.

## 3. Endpoints Implemented
- `GET /api/reports/dashboard-stats`: Role-specific dynamic KPI counts and statistics.
- `GET /api/reports/enrollment-trends`: Monthly enrollment volume chart data.
- `GET /api/reports/revenue-analytics`: Monthly revenue collection data.
- `GET /api/reports/attendance-overview`: Batch-wise average attendance distribution.
- `GET /api/reports/export/{dataset}`: Stream data file in requested format (`format=csv|xlsx|pdf`).

## 4. Frontend Integration
- View: `ReportsPage.jsx` equipped with Recharts graphs (BarChart, LineChart, PieChart) and export control panel.
