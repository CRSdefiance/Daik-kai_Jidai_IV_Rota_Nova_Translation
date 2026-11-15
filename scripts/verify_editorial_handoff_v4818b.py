"""Independently audit the full ledger preservation and apply six staged files."""
from pathlib import Path
from copy import deepcopy
import argparse
import gzip
import json
import os
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer

CHECKPOINT=Path('work/analysis/lil_B180_reference_checkpoint_v4817b')
ROOT=Path('work/analysis/editorial_handoff_verification_v4818b')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
    assert not ROOT.exists();plan=read(CHECKPOINT/'mutation_plan.json');files=plan['files'];assert len(files)==6
    for r in files:
        assert sha(Path(r['target']).read_bytes())==r['before_sha256']
        assert sha(Path(r['staged']).read_bytes())==r['after_sha256']
    lp=Path('translations/editorial_review_current_v1.json');row=next(r for r in files if Path(r['target'])==lp.resolve())
    before=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());assert lp.read_bytes()==before
    old=json.loads(before);new=read(row['staged']);key=plan['ledger_key']
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop('previous_latest_checkpoint_before_B180_references_v4817');inverse.pop(key)
    assert inverse==old
    assert Path(row['staged']).read_bytes()==encode_ledger(new) and len(Path(row['staged']).read_bytes())<100*1024*1024
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5912,5915,3748,2164)
    assert new['goal_status']=='active' and new['full_goal_complete'] is False
    for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
    entry=new[key];doc=read(entry['manuscript']);assert sha(Path(entry['manuscript']).read_bytes())==entry['manuscript_sha256']
    assert entry['approved_uncredited_objects']==len(doc['records'])==11 and entry['source_prose_or_completion_credit_added']==0
    assert entry['records']==doc['records'] and (doc['revised'],doc['retained'])==(5,6)
    current=new['current_integrated_candidate'];image=NdsImage.open(current['path']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
    cblock=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[180]
    jblock=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[180]
    for r in doc['records']:
        assert all(r['review'].values()) and r['source_meaning'] and r['localization_note']
        for b,field,hexkey in [(jblock,'source_reference','source_hex'),(cblock,'current_reference','current_hex')]:
            at=r[field]['offset'];raw=bytes.fromhex(r[hexkey]);assert b[at:at+len(raw)]==raw and b[at+len(raw)]==0
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification']
    assert all(r['source_selector'] in [166,167,254] for r in doc['records'])
    reg=read('translations/release_stack.json');manifest=read(current['manifest'])
    assert len(reg['accepted_layers'])==114 and reg['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==561 and all(manifest['checks'].values())
    from scripts.verify_lil_B180_checkpoint_v4818b import audit_actual
    audit_actual(new[key])
    ROOT.mkdir(parents=True)
    receipt=dict(ledger_sha256=row['after_sha256'],candidate=current['path'],candidate_sha256=current['sha256'],
        all_original_root_and_nested_ledger_history_preserved=True,all_coverage_counters_unchanged=True,
        source_current_and_native_approval_references_exact=True,approved_uncredited_B180_objects=11,
        revised=5,retained=6,no_new_registered_ROM_or_completion_credit=True,new_research_ROMs=2,new_emulator_runs=4,
        all_current561_entries114_accepted_and_promoted_main_preserved=True,full_goal_active=True,
        applied=args.apply,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT/'pre_apply_audit.json',receipt)
    if args.apply:
        for r in files:
            target=Path(r['target']);assert sha(target.read_bytes())==r['before_sha256']
        for r in files:
            data=Path(r['staged']).read_bytes()
            with Path(r['target']).open('r+b') as stream:
                stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['after_sha256']
        assert lp.read_bytes()==Path(row['staged']).read_bytes()
        save(ROOT/'verified_handoff.json',receipt)
    print(dict(applied=args.apply,metadata_files=6,approved_uncredited_B180=11,all_history_preserved=True,full_goal_active=True),flush=True)
