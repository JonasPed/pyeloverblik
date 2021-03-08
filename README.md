# pyeloverblik
Python wrapper for eloverblik.dk api.

## Installation
Install the library from PyPI: `pip install pyeloverblik`.

## Usage 
After installation either call the library directly with `python -m pyeloverblik` or integrate the library in your code like below.

```python3

client = Eloverblik(REFRESH_TOKEN)
data = client.get_latest(METERING_POINT)

or 

client = Eloverblik(REFRESH_TOKEN)
data = client.get_time_series(METERING_POINT, from_date='2021-01-01', to_date='2021-01-03', aggregation='Hour')


```
