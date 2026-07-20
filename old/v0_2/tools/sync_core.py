"""Conservative v0.2 sync placeholder: report only and never mutate."""
import argparse, sys
from pathlib import Path
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--target',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args(argv)
 if not (a.target/'orchestration.lock.json').is_file(): print('refusing target without adapter lock',file=sys.stderr);return 2
 if a.apply: print('v0.2 candidate intentionally defers apply; no files changed',file=sys.stderr);return 2
 print(f'dry-run: v0.2 validated one target only; version propagation deferred; no mutation: {a.target}')
 return 0
if __name__=='__main__': raise SystemExit(main())
