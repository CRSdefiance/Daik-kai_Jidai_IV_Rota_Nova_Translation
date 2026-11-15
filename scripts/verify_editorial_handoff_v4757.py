"""Independently validate all B180 source/gloss references and apply six staged files."""
import argparse
import gzip
import json
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_lil_B180_glosses_v4756 import ROOT as CHECKPOINT,PACKET,PRIOR,KEY
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/editorial_handoff_verification_v4757')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    assert not ROOT.exists()
    plan=read(CHECKPOINT/'mutation_plan.json');receipt=read(CHECKPOINT/'staged_receipt.json')
    assert len(plan)==len({r['target'] for r in plan})==6
    lp=Path('translations/editorial_review_current_v1.json')
    for r in plan:
        a,b=Path(r['target']),Path(r['planned'])
        assert a.is_relative_to(Path.cwd()) and b.is_relative_to(CHECKPOINT.resolve())
        assert sha(a.read_bytes())==r['before_sha256'] and sha(b.read_bytes())==r['planned_sha256']
    assert lp.read_bytes()==gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes())
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    old=read(lp);row=next(r for r in plan if Path(r['target'])==lp.resolve());new=read(row['planned'])
    assert set(new)==set(old)|{KEY} and KEY not in old
    assert {k:v for k,v in new.items() if k not in [KEY,'latest_checkpoint']}=={k:v for k,v in old.items() if k!='latest_checkpoint'}
    assert new['goal_status']=='active' and not new['full_goal_complete']
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5912,5915,3748,2164)
    fresh=new['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release'])==(5912,5912,0)
    assert Path(row['planned']).read_bytes()==encode_ledger(new) and Path(row['planned']).stat().st_size<100*1024*1024
    packet=read(PACKET);group=packet['block'];rows=group['records']
    assert new[KEY]['packet_sha256']==sha(PACKET.read_bytes()) and new[KEY]['uncredited_objects']==11
    assert new[KEY]['manuscript_authored'] is False and new[KEY]['source_prose_or_completion_credit_added']==0
    assert len(rows)==packet['total_editorial_objects']==11 and packet['no_predecessor_English_exposed']
    image=NdsImage.open('work/clean.nds');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[180]
    assert sha(block)==group['clean_block_sha256'] and len(block)==576
    for r in rows:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert raw[1:].decode('cp932')==r['source_Japanese'] and r['fresh_source_gloss']
        assert r['clean_source_complete_exchange_read_before_predecessor_English']
    commands=group['complete_native_commands']
    assert len(commands)==28 and sum(c['word']==0x4000 for c in commands)==11
    assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==10
    assert [c['offset'] for c in commands if c['word']==0x8000]==[452,484]
    assert [c['offset'] for c in commands if c['word']==0xA000]==[472,504,516]
    assert [c['offset'] for c in commands if c['word']==0xC200]==[570]
    assert [c['offset'] for c in commands if c['word']==0]==[572]
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert new['current_integrated_candidate']['profile']=='all-routes-unified-v4749'
    assert read('translations/promoted_build.json')['profile']=='all-routes-unified-v4701'
    for p,h in {**receipt['evidence'],**receipt['preserved_release_files'],**packet['evidence']}.items():assert sha(Path(p).read_bytes())==h,p
    for r in plan:
        if Path(r['target']).suffix=='.md':
            assert Path(r['target']).read_bytes()==(CHECKPOINT/(Path(r['target']).name+'.before')).read_bytes()
            assert Path(r['planned']).read_text(encoding='utf-8').endswith(Path(r['target']).read_text(encoding='utf-8').split('\n',1)[1])
    ROOT.mkdir(parents=True)
    save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,
        complete_prior_root_nested_history_and_counts_unchanged=True,all11_clean_source_gloss_references_bound=True,
        no_predecessor_English_manuscript_or_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if args.apply:
        for r in plan:assert sha(Path(r['target']).read_bytes())==r['before_sha256'] and sha(Path(r['planned']).read_bytes())==r['planned_sha256']
        for r in plan:
            data=Path(r['planned']).read_bytes()
            with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['planned_sha256']
        for p,h in receipt['preserved_release_files'].items():assert sha(Path(p).read_bytes())==h,p
        receipt.update(ledger_sha256=sha(lp.read_bytes()),updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in plan})
        save(CHECKPOINT/'checkpoint_receipt.json',receipt)
        save(ROOT/'verified_handoff.json',dict(checkpoint='V4756',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5912,integrated=5912,pending=0,
            source_prose=5915,revised=3748,retained=2164,uncredited_B180_clean_glosses=11,
            all_prior_root_nested_history_counts_and_full_objective_preserved=True,all11_clean_gloss_references_bound=True,
            conditional28_command_source_shape_preserved_and_native_binding_still_pending=True,
            main_V4701_latest_experimental_V4749_exact_patch_and_city_alias_lead_preserved=True,
            all_jobs_terminal=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V4756 applied after independent audit:5912 completed;11 uncredited B180 glosses,conditional source shape bound;main/latest/full objective preserved.')
    else:print('Independent staged audit passed;no current metadata writes.')
