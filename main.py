import argparse

parser = argparse.ArgumentParser(description='Run stability tests on a kubernetes deployment')
parser.add_argument('name', type=str, nargs='+',
                    help='Name of the kubernetes deployment to target for testing')

args = parser.parse_args()
print(args.name)

