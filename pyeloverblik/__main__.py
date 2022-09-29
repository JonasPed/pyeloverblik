'''
Main for pyeloverblik
'''
import argparse
from datetime import datetime
import logging
from . import Eloverblik

def main():
    '''
    Main method
    '''
    parser = argparse.ArgumentParser("pyeloverblik")
    parser.add_argument("--log", action="store", required=False)
    parser.add_argument("--refresh-token", action="store", required=True)
    parser.add_argument('--metering-point', action='store', required=True)

    args = parser.parse_args()

    _configureLogging(args)

    # Get and print hourly meter data.
    result = Eloverblik(args.refresh_token).get_latest(args.metering_point)
    if result.status == 200:
        total = 0
        print(f"Date: {result.data_date}")
        for hour in range(24):
            data = result.get_metering_data(hour)
            total += data
            print(f"Hour {hour}-{hour+1}: {data}kWh")

        print(f"Total: {total}kWh")
    else:
        print(f"Error getting data. Status: {result.status}. Error: {result.detailed_status}")
    
    # Get and pring monthly meter data.
    result = Eloverblik(args.refresh_token).get_per_month(args.metering_point)
    if result.status == 200:
        print(f"Date: {result.data_date}")
        for month in range(1, datetime.today().month + 1):
            data = result.get_metering_data(month)
            print(f"Month {month}: {data}kWh")

        print(f"Total: {result.get_total_metering_data()}kWh")
    else:
        print(f"Error getting data. Status: {result.status}. Error: {result.detailed_status}")
    
    # Get and print fees.
    result = Eloverblik(args.refresh_token).get_tariffs(args.metering_point)
    if result.status == 200:
        for fee_name, fee_rate in result.charges.items():
            print(f"Fee '{fee_name}': {fee_rate}kr/kWh")

    else:
        print(f"Error getting data. Status: {result.status}.")

def _configureLogging(args):
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)
        
        logging.basicConfig(level=numeric_level)

if __name__ == "__main__":
    main()
