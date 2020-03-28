'''
Main for pyeloverblik
'''
import argparse
from . import Eloverblik

def main():
    '''
    Main method
    '''
    parser = argparse.ArgumentParser("pydanfossair")
    parser.add_argument("--refresh-token", action="store", required=True)
    parser.add_argument('--metering-point', action='store', required=True)

    args = parser.parse_args()

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

if __name__ == "__main__":
    main()
