"""Independently invert B177 relocation and checkpoint the next unresolved gates."""
from copy import deepcopy
import gzip
import os
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.lil_B177_relocation_checkpoint_text_v4627 import NEXT,SUMMARY
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_relocation_checkpoint_v4627')
AUDIT=Path('work/analysis/editorial_handoff_verification_v4628')
DOC=Path('translations/lil_B177_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/lil_B177_relocation_v4625/nested_source_relocation_research.json')
STORED=Path('work/analysis/lil_B177_stored_v4626/all10_final_stored_targets40_macro_cases_and_complete_planes.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4624/verified_handoff.json')

if __name__=='__main__':
    assert not ROOT.exists() and not AUDIT.exists()
    lp=Path('translations/editorial_review_current_v1.json')
    prior,doc,plan,stored=map(read,[PRIOR,DOC,PLAN,STORED]);before_bytes=lp.read_bytes();before=read(lp)
    assert sha(before_bytes)==prior['ledger_sha256']
    assert plan['manuscript_sha256']==stored['manuscript_sha256']==sha(DOC.read_bytes())
    assert stored['relocation_plan_sha256']==sha(PLAN.read_bytes())
    assert (stored['current_final_stored_macro_alignment_cases'],stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(40,24,16)
    assert len(stored['final_target_parity_cases'])==10
    image=NdsImage.open(doc['current_ROM']);container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    assert len(plan['blocks'])==1
    b=plan['blocks'][0];assert b['block']==177
    source=container.blocks[177];target=Path(b['research_block']).read_bytes()
    assert sha(source)==b['source_block_sha256'] and sha(target)==b['research_block_sha256']
    assert (len(source),len(target),b['source_logical_end'],b['research_logical_end'])==(488,472,486,470)
    inventory,_,_=scoped_inventory();commands,speeches=inventory(image.read_file('/__arm9__.bin'),target)
    assert len(commands)==13 and len(speeches)==10 and len(b['command_map'])==13
    assert not b['relative_skip_fixups'] and not b['target_native_skip_cases']
    assert [(r['source_offset'],r['target_offset']) for r in b['original_declared_end_word_maps']]==[(482,466)]
    assert [c['word'] for c in commands if c['word']!=0x4000]==[0xA000,0xC200,0]
    by={r['id']:r for r in doc['records']}
    for row,proof in zip(b['text_records'],stored['final_target_parity_cases'],strict=True):
        assert row['id']==proof['id'] and row['target_hex']==proof['stored_target_hex']
        value=bytes.fromhex(row['target_hex']);at=row['new_offset'];old=row['old_offset']
        assert target[at:at+len(value)]==value and target[at+len(value)]==0
        assert source[old-5:old+1]==target[at-5:at+1]==bytes.fromhex(by[row['id']]['source_complete_preamble_hex'])
        assert proof['complete_final_target_native_plane_equals_reviewed_plane'] and proof['tail_padding_consumed_without_blank_page_or_lost_glyph']
    restored=bytearray(target[:b['research_logical_end']]);struct.pack_into('<H',restored,4,b['source_logical_end']-8)
    for row in reversed(b['text_records']):
        restored[row['new_offset']:row['new_offset']+row['new_length']]=source[row['old_offset']:row['old_offset']+row['old_length']]
    assert bytes(restored)==source[:b['source_logical_end']]
    target_SC2=Path(plan['target_SC2']).read_bytes();assert sha(target_SC2)==plan['target_SC2_sha256']
    target_blocks=IlnkContainer.parse(target_SC2).blocks
    assert len(target_blocks)==len(container.blocks)==336
    assert [n for n,(a,z) in enumerate(zip(container.blocks,target_blocks,strict=True)) if a!=z]==[177]
    assert target_blocks[177]==target
    next_text,summary=NEXT,SUMMARY
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py',
        'out/all_routes_combined_v4595_candidate.nds','out/all_routes_combined_v4595_candidate.xdelta',
        'out/raphael_natural_v2_accepted_base.nds','work/clean.nds']
    stable_hashes={p:sha(Path(p).read_bytes()) for p in stable}
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,STORED,PRIOR,Path(b['research_block']),Path(__file__)]}
    ledger=deepcopy(before)
    ledger['lil_B177_reversible_relocation_v4627']=dict(summary=summary,evidence=evidence,next=next_text,
        no_new_review_orcompletion_credit=True,registered_reference_actual_and_release_pending=True,full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert {k:v for k,v in ledger.items() if k not in ['lil_B177_reversible_relocation_v4627','latest_checkpoint']}=={
        k:v for k,v in before.items() if k!='latest_checkpoint'}
    planned={lp:encode_ledger(ledger)}
    section='## V4627: B177 reversible relocation and stored native tests complete\n\n'+summary+'\n\nNext: '+next_text+'\n\n'
    for i,name in enumerate(['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']):
        p=Path('docs')/name;first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4627' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    assert len(planned[lp])<100*1024*1024
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes,mtime=0))
    staged=ROOT/'staged';staged.mkdir();mutation_plan=[]
    for i,(path,data) in enumerate(planned.items()):
        if path!=lp:(ROOT/(path.name+'.before')).write_bytes(path.read_bytes())
        output=staged/(str(i)+'.planned');output.write_bytes(data)
        mutation_plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutation_plan)
    for row in mutation_plan:
        assert sha(Path(row['target']).read_bytes())==row['before_sha256']
        assert sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    for row in mutation_plan:
        data=Path(row['planned']).read_bytes()
        with Path(row['target']).open('r+b') as stream:
            stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
    assert all(sha(Path(p).read_bytes())==h for p,h in stable_hashes.items())
    receipt=dict(checkpoint='V4627',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5885,integrated=5875,pending=10,
        source_prose=5888,revised=3733,retained=2142,stored_alignment_cases=40,fresh_stored_cases=24,exact_reused_stored_cases=16,
        all_prior_ledger_records_and_full_objective_preserved=True,preserved_release_files=stable_hashes,evidence=evidence,
        independent_inverse_recovers_every_predecessor_logical_byte=True,source_ends_mapped=[[482,466]],
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,new_ROMs=0,
        remaining_B178_B180_physical_speeches=38,full_goal_active=True,full_goal_complete=False)
    save(ROOT/'checkpoint_receipt.json',receipt);AUDIT.mkdir(parents=True);save(AUDIT/'verified_handoff.json',receipt)
    print('V4627 independently inverted/audited/applied:488 to472 bytes,13 commands,single end,40 stored cases. Counts and main V4541 unchanged.')
