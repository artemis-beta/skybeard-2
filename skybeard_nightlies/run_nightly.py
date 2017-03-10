import argparse
from sb_nightlies import *
import logging
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('--branch', dest='branch_name')
parser.add_argument('--location', dest='location')
parser.add_argument('--out', dest='outloc')

args = parser.parse_args()

time_str = datetime.now().strftime("%Y-%m-%d")

skb_test = SkybeardNightlyBuilds(output_dir = args.outloc, name='skb-nightly_{}'.format(time_str), beard_directory=os.path.join(args.location, 'beards'), skb_core_tests=os.path.join(args.location, 'tests'), branch_name=args.branch_name)
skb_test.run_skb_core_tests()
skb_test.run_skb_beard_tests()
skb_test.gen_table()
skb_test.produce_logs()
