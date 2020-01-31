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

    result = Eloverblik(args.refresh_token).get_yesterday_parsed(args.metering_point)

    total = 0
    print(f"Date: {result.data_date}")
    for x in range(24):
        data = result.get_metering_data(x)
        total += data
        print(f"Hour {x}-{x+1}: {data}kWh")
    
    print(f"Total: {total}kWh")
if __name__ == "__main__":
    main()