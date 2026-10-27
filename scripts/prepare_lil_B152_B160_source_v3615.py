"""Prepare342 exact source/current objects and the unchanged historical Lil context."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B160_source_v3615')
LEAD=Path('work/analysis/lil_B152_B160_next_source_v3614/all342_unreviewed_clean_current_and99_prior_exact_source_keys.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3612/verified_handoff.json')
HISTORY=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();lead,prior,history=map(read,[LEAD,PRIOR,HISTORY]);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];known={historical_key(r) for r in read(lp)['contextual_story_natural_dialogue_pass_v1871']['record_keys']};current,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds');assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==lead['current_ROM_sha256'];a,b=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,current]];groups=deepcopy(lead['blocks']);rows=[]
    for g in groups:
        assert sha(a[g['block']])==g['clean_block_sha256'] and sha(b[g['block']])==g['current_block_sha256']
        for i,r in enumerate(g['records']):
            assert historical_key(r) not in known
            for data,ref,k in [(a[g['block']],r['source_reference'],'source_hex'),(b[g['block']],r['current_reference'],'current_hex')]:
                at=ref['offset'];value=bytes.fromhex(r[k]);assert data[at:at+len(value)]==value and data[at+len(value)]==0 and data[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
            r.update(kind='system-FE' if r['source_selector']==254 else 'progressive',source_presentation_prefix_hex=format(r['source_selector'],'02x'),native_command_extent=r['source_native_extent'],spoken_sequence_index=i,ordinary_predecessor_English_not_translation_source=True,current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0);rows.append(r)
        g.update(source_block_sha256=g['clean_block_sha256'],source_native_commands=g['all_clean_native_commands'],current_native_commands=g['all_current_native_commands'],source_current_native_command_shape_exact=True)
    assert len(rows)==342 and current.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4') and sha(Path(history['actual_historical_snapshot']).read_bytes())==history['actual_historical_snapshot_sha256'];ROOT.mkdir(parents=True);save(ROOT/'all342_clean_current_complete_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(current.read_file('/__arm9__.bin')),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(current.read_file('/data/EV2.DK4')),actual_historical_snapshot=history['actual_historical_snapshot'],actual_historical_snapshot_sha256=history['actual_historical_snapshot_sha256'],historical_snapshot_ROM=history['historical_snapshot_ROM'],historical_snapshot_is_Lil_London_not_selected_B152_B160=True,blocks=groups,records=rows,typed_choice_records=[],typed_actor_style_records=[],source_macro_counts=lead['source_macro_counts'],total_editorial_objects=342,speech_objects=342,ordinary_source_speeches=336,system_FE_panels=6,source_selectors=lead['source_selectors'],source_static_actor_selectors=[n for n in lead['source_selectors'] if n!=254],source_native_commands=652,source_relative_sites=125,current_native_full_context_gloss_and_oldEnglish_comparison_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [LEAD,PRIOR,HISTORY,Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('342 source/current objects bound:336progressive/sixFE,652commands,125relative sites,FI18/FA2;no credit.')
