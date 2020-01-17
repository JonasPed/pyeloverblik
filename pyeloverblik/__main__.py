'''
Main for pyeloverblik
'''
import argparse
from . import eloverblik

def main():
    '''
    Main method
    '''
    parser = argparse.ArgumentParser("pydanfossair")
    parser.add_argument("--refresh-token", action="store", required=True)
    parser.add_argument('--metering-point', action='store', required=True)
    
    args = parser.parse_args()

    print(eloverblik.Eloverblik(args.refresh_token).getYesterDayNiceFormat(args.metering_point))

if __name__ == "__main__":
    main()