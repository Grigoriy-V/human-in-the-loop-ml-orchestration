"""Create a deliberately small, self-contained adapter skeleton."""
import argparse, json, shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=['.codex','tools/agent_ledger.py','tools/validate_orchestration.py','reports/agent_execution_ledger.schema.json','core/task_spec.schema.json','core/project_manifest.schema.json','docs/agent_orchestration.md','requirements.txt','VERSION']
def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument('--target',required=True,type=Path);p.add_argument('--adapter-type',required=True);p.add_argument('--adapter-name',required=True);p.add_argument('--dry-run',action='store_true');a=p.parse_args(argv)
 target=a.target
 if target.exists() and any(target.iterdir()): print('refusing nonempty target',file=sys.stderr);return 2
 if a.dry_run: print(f'dry-run: would bootstrap {a.adapter_type} adapter at {target}');return 0
 target.mkdir(parents=True,exist_ok=False)
 for item in FILES:
  src=ROOT/item; dst=target/item
  if src.is_dir(): shutil.copytree(src,dst)
  else: dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 (target/'reports/agent_execution_ledger.jsonl').write_text('',encoding='utf-8')
 (target/'AGENTS.md').write_text('# Adapter Rules\n\n<!-- CORE-MANAGED-START -->\nUse the project-local ledger helper. One repository, workdir, and ledger per task.\n<!-- CORE-MANAGED-END -->\n\n<!-- ADAPTER-LOCAL-START -->\nAdd domain-specific policy here.\n<!-- ADAPTER-LOCAL-END -->\n',encoding='utf-8')
 (target/'PROJECT_LOG.md').write_text('# Project Log\n\nAdapter initialized; no domain operations have run.\n',encoding='utf-8')
 (target/'PROJECT_ROADMAP.md').write_text(f'# {a.adapter_name} Roadmap\n\nAdapter type: `{a.adapter_type}`. Define the first human-approved task before execution.\n',encoding='utf-8')
 (target/'orchestration.lock.json').write_text(json.dumps({'core_version':(ROOT/'VERSION').read_text().strip(),'adapter_type':a.adapter_type,'adapter_name':a.adapter_name},indent=2)+'\n',encoding='utf-8')
 print(f'bootstrapped {target}')
 return 0
if __name__=='__main__': raise SystemExit(main())
