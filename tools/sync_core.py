"""Conservative v0.1 sync: validate scope and report; never mutates."""
import argparse, sys
from pathlib import Path
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--target',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args(argv)
 if not (a.target/'orchestration.lock.json').is_file(): print('refusing target without adapter lock',file=sys.stderr);return 2
 if a.apply: print('v0.1 does not implement apply; no files changed',file=sys.stderr);return 2
 print(f'dry-run: validated one target only; no mutation: {a.target}')
 return 0
if __name__=='__main__': raise SystemExit(main())
