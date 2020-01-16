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
    parser.add_argument('--meetering-point', action='store', required=True)
    
    args = parser.parse_args()

    eloverblik.Eloverblik(args.refresh_token).getTimeSeries(args.meetering_point)

if __name__ == "__main__":
    main()