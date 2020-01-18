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

    print(Eloverblik(args.refresh_token).get_time_series(args.metering_point))

if __name__ == "__main__":
    main()