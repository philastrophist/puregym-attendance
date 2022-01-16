"""updates csv with new historical data"""

from puregym import *
import pandas as pd
from pathlib import Path

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('filename', type=Path)
    parser.add_argument('email')
    parser.add_argument('pin')
    parser.add_argument('--gym', default=None)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()
    
    client = PuregymAPIClient()
    client.login(args.email, args.pin)
    
    json, gym = client.get_gym_history(args.gym)
    df = pd.DataFrame(json)
    df['attendanceTime'] = pd.to_datetime(df['attendanceTime'])

    if args.filename.exists():
    	df_disk = pd.read_csv(args.filename)
    	df_disk['attendanceTime'] = pd.to_datetime(df_disk['attendanceTime'])
    	df = pd.concat([df, df_disk], sort=False, ignore_index=True).sort_values(['attendanceTime', 'lastRefreshed']).drop_duplicates('attendanceTime', 'last')
    df.to_csv(args.filename)

    if args.show:
        import matplotlib.pyplot as plt
        df.plot('attendanceTime', 'totalPeopleInGym')
        plt.axhline(client.get_gym_attendance(args.gym)[0], c='r')
        plt.show()
    print(f'{args.filename}')