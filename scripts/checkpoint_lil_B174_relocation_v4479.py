"""Audit reversible bytes/stored cases and checkpoint the next unresolved B174 gate."""
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
from scripts.lil_B174_checkpoint_text_v4475 import NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_relocation_checkpoint_v4479')
AUDIT=Path('work/analysis/editorial_handoff_verification_v4480')
DOC=Path('translations/lil_B174_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/lil_B174_relocation_v4477/nested_source_relocation_research.json')
STORED=Path('work/analysis/lil_B174_stored_v4478/all33_final_stored_targets132_macro_cases_and_complete_planes.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4476/verified_handoff.json')

if __name__=='__main__':
    assert not ROOT.exists() and not AUDIT.exists()
    lp=Path('translations/editorial_review_current_v1.json')
    prior,doc,plan,stored=map(read,[PRIOR,DOC,PLAN,STORED])
    before_bytes=lp.read_bytes();before=read(lp)
    assert sha(before_bytes)==prior['ledger_sha256'] and plan['manuscript_sha256']==stored['manuscript_sha256']==sha(DOC.read_bytes())
    assert stored['relocation_plan_sha256']==sha(PLAN.read_bytes())
    assert (stored['current_final_stored_macro_alignment_cases'],stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(132,48,84)
    assert len(stored['final_target_parity_cases'])==33
    image=NdsImage.open(doc['current_ROM']);container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    block=plan['blocks'][0];assert block['block']==174
    source=container.blocks[174];target=Path(block['research_block']).read_bytes()
    assert sha(source)==block['source_block_sha256'] and sha(target)==block['research_block_sha256']
    assert (len(source),len(target))==(2092,2208)
    inventory,_,_=scoped_inventory();commands,speeches=inventory(image.read_file('/__arm9__.bin'),target)
    assert len(commands)==45 and len(speeches)==33
    assert len(block['command_map'])==45 and len(block['relative_skip_fixups'])==4 and len(block['target_native_skip_cases'])==20
    by={r['id']:r for r in doc['records']}
    for row,proof in zip(block['text_records'],stored['final_target_parity_cases'],strict=True):
        assert row['id']==proof['id'] and row['target_hex']==proof['stored_target_hex']
        value=bytes.fromhex(row['target_hex']);at=row['new_offset'];old=row['old_offset']
        assert target[at:at+len(value)]==value and target[at+len(value)]==0
        assert source[old-5:old+1]==target[at-5:at+1]==bytes.fromhex(by[row['id']]['source_complete_preamble_hex'])
        assert proof['complete_final_target_native_plane_equals_reviewed_plane'] and proof['tail_padding_consumed_without_blank_page_or_lost_glyph']
    # Independently reconstruct the complete predecessor logical stream.
    restored=bytearray(target[:block['research_logical_end']])
    struct.pack_into('<H',restored,4,block['source_logical_end']-8)
    for edge in block['relative_skip_fixups']:
        assert edge['new_offset']+4+edge['target_span']==edge['new_matched_skip_target']
        struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for row in reversed(block['text_records']):
        old=source[row['old_offset']:row['old_offset']+row['old_length']]
        restored[row['new_offset']:row['new_offset']+row['new_length']]=old
    assert bytes(restored)==source[:block['source_logical_end']]
    target_SC2=Path(plan['target_SC2']).read_bytes();assert sha(target_SC2)==plan['target_SC2_sha256']
    target_blocks=IlnkContainer.parse(target_SC2).blocks
    assert [n for n,(a,b) in enumerate(zip(container.blocks,target_blocks,strict=True)) if a!=b]==[174]
    assert len(container.blocks)==len(target_blocks)==336 and target_blocks[174]==target
    next_text=('Create the disclosed B174 one-block research reference from registered V4445; relocation V4477 '
        'and stored proof V4478 are complete and must not be repeated without a new finding. Run original '
        'whole-block loaders, entry/end census and relocated predicate/C200/relative controls. Then capture '
        'paired Japanese/English cold boots preserving all45 source commands, the unforced optional Emilio '
        'aside,6240,two A000s,C200 and single end. Record actual versus offline coverage, seal references, '
        'register the atomic compiler, integrate cumulatively and verify the clean-input patch and startup. '+
        PREVIOUS_NEXT[PREVIOUS_NEXT.index('Continue B175-B180'):])
    summary=('V4479 completes B174 reversible relocation and final stored native checks after the33 contextual/native '
        'reviews approved atV4475. The block grows2092 to2208 stored bytes. All45 commands,33 complete preambles, '
        'four relative sites/20 relocated native cases,eight nonrelative leaves,the conditional Emilio aside, '
        '6240,two A000s,C200 and single tail end are preserved. Independent inverse reconstruction recovers every '
        'predecessor logical byte;all335 other SC2 blocks remain exact. All132 stored alignment cases pass:48 fresh '
        'parity-tail cases/twelve planes and84 exact-reused cases/21 planes. Complete native planes match the '
        'reviewed text with no missing leading/internal/trailing glyph,bounds,extra page or padding defect. '
        'No source condition or effect is flattened. Full source/current/native references and23 revisions/10 '
        'justified retentions remain preserved. No new ROM or emulator run is created by this checkpoint.\n\n'
        'Coverage stays5833 fresh rereads:5800 integrated/completed and33 pending;source/prose5836,including3980 '
        'SC2 and64 SC3;route reviewed/completed4234/4201;historical completed decisions3686 revised/2114 retained. '
        'Promoted main remains V4445 with549 manuscript batches/114 accepted layers and its byte-exact clean-input '
        'patch. Registry,builder,canonical inputs,all prior completions,all generated ROMs and every translation, '
        'draft,executed producer,proof and failure remain preserved. Source prose gains and completion gains are0. '
        'The complete one-space CRLF ledger encoding remains unchanged. These offline proofs do not establish '
        'actual event174 eligibility,earned flags,selected B174 gameplay,full-route completion or hardware behavior.\n\n'+next_text)
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py',
        'out/all_routes_combined_v4445_candidate.nds','out/all_routes_combined_v4445_candidate.xdelta',
        'out/raphael_natural_v2_accepted_base.nds','work/clean.nds']
    stable_hashes={p:sha(Path(p).read_bytes()) for p in stable}
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,STORED,PRIOR,Path(block['research_block']),Path(__file__)]}
    ledger=deepcopy(before)
    ledger['lil_B174_reversible_relocation_v4479']=dict(summary=summary,evidence=evidence,next=next_text,
        no_new_review_orcompletion_credit=True,registered_reference_actual_and_release_pending=True,full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert {k:v for k,v in before.items() if k not in {'latest_checkpoint','lil_B174_reversible_relocation_v4479'}}=={
        k:v for k,v in ledger.items() if k not in {'latest_checkpoint','lil_B174_reversible_relocation_v4479'}}
    planned={lp:encode_ledger(ledger)}
    section='## V4479: B174 reversible relocation and stored native checks pass\n\n'+summary+'\n\nNext: '+next_text+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;first,rest=path.read_text(encoding='utf-8').split('\n',1)
        if name=='editorial_handoff_current.md':
            assert first=='# Current editorial handoff - V4475';first='# Current editorial handoff - V4479'
        planned[path]=(first+'\n\n'+section+rest).encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes,mtime=0))
    staged=ROOT/'staged';staged.mkdir();mutations=[]
    for n,(path,data) in enumerate(planned.items()):
        (ROOT/(str(n)+'.before')).write_bytes(path.read_bytes());stage=staged/(str(n)+'.planned');stage.write_bytes(data)
        mutations.append(dict(path=str(path),before_sha256=sha(path.read_bytes()),planned=str(stage),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutations)
    for row in mutations:
        assert sha(Path(row['path']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    for row in mutations:
        data=Path(row['planned']).read_bytes()
        with Path(row['path']).open('r+b') as stream:
            stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
        assert sha(Path(row['path']).read_bytes())==row['planned_sha256']
    for path,digest in {**stable_hashes,**evidence}.items():assert sha(Path(path).read_bytes())==digest
    assert lp.read_bytes()==encode_ledger(read(lp)) and lp.stat().st_size<100*1024*1024
    receipt=dict(checkpoint='V4479',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5833,integrated=5800,pending=33,
        source_prose=5836,revised=3686,retained=2114,candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        exact_inverse_all_predecessor_logical_bytes=True,source_bytes=2092,target_bytes=2208,
        target_logical_end=block['research_logical_end'],source_end_maps=block['original_declared_end_word_maps'],
        structural_commands=45,speeches=33,relative_sites=4,target_relative_cases=20,
        final_stored_alignment_cases=132,fresh_stored_cases=48,exact_reused_stored_cases=84,
        all_prior_ledger_records_and_full_objective_preserved=True,preserved_release_files=stable_hashes,evidence=evidence,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,new_ROMs=0,
        remaining_B175_B180_physical_speeches=90,full_goal_active=True,full_goal_complete=False)
    save(ROOT/'checkpoint_receipt.json',receipt);AUDIT.mkdir(parents=True);save(AUDIT/'verified_handoff.json',receipt)
    print('V4479 audited/applied:2092 to2208 bytes,45 commands,20 relative cases,132 stored cases. Counts unchanged;main V4445 preserved. Reference/gameplay/release remain.')
