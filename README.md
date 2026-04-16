# Pension from Productivity
## A Responsible AI Dividend Model for Japan

Streamlit MVP prototype for:
- AI productivity measurement
- Pension productivity dividend simulation
- Executive reporting (PDF / CSV / JSON)

## Disclaimer
This prototype is a measurement, simulation, and reporting tool only.  
It does not operate as a pension administrator, financial institution, payment service, or investment advisor.

## Stack
- Python 3.11
- Streamlit
- pandas
- pydantic
- plotly
- sqlite (default local storage)
- reportlab (PDF export)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app initializes SQLite automatically at:
`data/pension_productivity.db`

## Pages
- Home
- Company Profile
- Baseline Input
- AI Deployment Input
- Dividend Simulator
- Results Dashboard
- Executive Report
- Admin / Branding

## Seed data
Demo records are inserted automatically on first run.

## Future Supabase integration notes
Add a repository layer (e.g., `core/repositories/`) with interchangeable backends:
- `sqlite_repository.py` (current)
- `supabase_repository.py` (future)

Switch by config flag:
- `ENABLE_SUPABASE=true` in environment

Keep page logic unchanged by routing CRUD through backend interface.
