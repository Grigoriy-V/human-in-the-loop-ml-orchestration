import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import agent_ledger as ledger
class CoreTests(unittest.TestCase):
 def cmd(self,*args,cwd=ROOT): return subprocess.run([sys.executable,*args],cwd=cwd,text=True,capture_output=True)
 def test_validator_and_manifest(self):
  r=self.cmd('tools/validate_orchestration.py'); self.assertEqual(r.returncode,0,r.stderr)
 def test_clean_ledger(self):
  r=self.cmd('tools/agent_ledger.py','validate'); self.assertEqual(r.returncode,0,r.stderr)
 def metadata(self,run='first-start'):
  return {'agent_run_id':run,'parent_task':'/root','agent_name':'terra_worker','requested_model':'gpt-5.6-terra','requested_reasoning':'low','task_type':'test','roadmap_step':'repair','scope_summary':'test','constraints':['bounded'],'commands':['test'],'files_changed':[],'git_commit_before':None,'git_commit_after':None,'ml_ledger_event_ids':[],'notes':'test'}
 def test_empty_ledger_first_start_from_metadata_file(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d); meta=d/'start.json'; out=d/'ledger.jsonl';meta.write_text(json.dumps(self.metadata()),encoding='utf-8')
   r=self.cmd('tools/agent_ledger.py','--ledger',str(out),'start','--metadata-file',str(meta));self.assertEqual(r.returncode,0,r.stderr)
   self.assertEqual(len(ledger.read_events(out)),1)
 def test_windows_lock_failure_does_not_create_ledger(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'ledger.jsonl'; event=ledger.base(self.metadata())
   with mock.patch.object(ledger.os,'open',side_effect=OSError('forced lock failure')):
    with self.assertRaises(OSError): ledger.append(out,event)
   self.assertFalse(out.exists())
 def test_full_lifecycle_and_invalid_schema_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'ledger.jsonl'; start=ledger.base(self.metadata('life'));ledger.append(out,start)
   done={**start,'event_id':'done-1','timestamp_utc':ledger.utc(),'event_type':'completed','status':'completed','commands':['test'],'files_changed':[],'outcome_summary':'ok','duration_seconds':1,'supervisor_decision':None};ledger.append(out,done)
   review={**done,'event_id':'review-1','timestamp_utc':ledger.utc(),'event_type':'reviewed','status':'reviewed','agent_name':'root','requested_model':'root','requested_reasoning':'not_applicable','commands':[],'files_changed':[],'outcome_summary':'accept','duration_seconds':None,'supervisor_decision':'accept'};ledger.append(out,review)
   before=out.read_bytes(); bad=ledger.base(self.metadata('bad'));bad['constraints']='not-an-array'
   with self.assertRaises(ledger.LedgerError): ledger.append(out,bad)
   bad=ledger.base(self.metadata('bad2'));bad['unknown']=1
   with self.assertRaises(ledger.LedgerError): ledger.append(out,bad)
   self.assertEqual(before,out.read_bytes())
 def test_bootstrap_dry_run_and_actual(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/'adapter'
   r=self.cmd('tools/bootstrap_project.py','--dry-run','--target',str(target),'--adapter-type','test','--adapter-name','Test');self.assertEqual(r.returncode,0,r.stderr);self.assertFalse(target.exists())
   r=self.cmd('tools/bootstrap_project.py','--target',str(target),'--adapter-type','test','--adapter-name','Test');self.assertEqual(r.returncode,0,r.stderr)
   self.assertTrue((target/'tools/agent_ledger.py').is_file());self.assertFalse(any(str(ROOT) in p.read_text(encoding='utf-8') for p in target.rglob('*') if p.is_file()))
   r=subprocess.run([sys.executable,'tools/agent_ledger.py','validate'],cwd=target,text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr)
   r=subprocess.run([sys.executable,'tools/validate_orchestration.py'],cwd=target,text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr)
   meta=target/'start.json';meta.write_text(json.dumps(self.metadata('adapter-first')),encoding='utf-8');r=subprocess.run([sys.executable,'tools/agent_ledger.py','start','--metadata-file',str(meta)],cwd=target,text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr)
   r=self.cmd('tools/bootstrap_project.py','--target',str(target),'--adapter-type','test','--adapter-name','Test');self.assertEqual(r.returncode,2)
 def test_sync_dry_run_no_mutation_and_refusal(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/'adapter';self.assertEqual(self.cmd('tools/bootstrap_project.py','--target',str(target),'--adapter-type','test','--adapter-name','Test').returncode,0)
   before={p.relative_to(target):p.read_bytes() for p in target.rglob('*') if p.is_file()};r=self.cmd('tools/sync_core.py','--target',str(target));self.assertEqual(r.returncode,0,r.stderr);after={p.relative_to(target):p.read_bytes() for p in target.rglob('*') if p.is_file()};self.assertEqual(before,after)
   self.assertEqual(self.cmd('tools/sync_core.py','--target',str(target),'--apply').returncode,2)
 def test_no_absolute_paths_in_manifest(self):
  self.assertNotIn('D:',(ROOT/'orchestration_manifest.json').read_text())
if __name__=='__main__': unittest.main()
