# pyeloverblik

Python wrapper for eloverblik.dk api.

It can read the following data from eloverblik.

- Hourly data
- Monthy data
- Fees

## Installation

Install the library from PyPI: `pip install pyeloverblik`.

## Usage 

After installation either call the library directly with `python -m pyeloverblik` or integrate the library in your code like below.

```python3

client = Eloverblik(REFRESH_TOKEN)
data = client.get_latest(METERING_POINT)

or 

client = Eloverblik(REFRESH_TOKEN)
data = client.get_time_series(METERING_POINT, from_date=datetime.now()-timedelta(days=2), to_date=datetime.now(), aggregation='Hour')

# In above example from_date and to_date is datetime objects.

```

