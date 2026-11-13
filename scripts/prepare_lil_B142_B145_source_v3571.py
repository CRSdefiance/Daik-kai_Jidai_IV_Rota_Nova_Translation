"""Bind38 new complete source/current objects and the existing actual Lil context."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_source_v3571')
LEAD=Path('work/analysis/lil_B142_B145_next_source_v3568/all38_unreviewed_clean_current_and130_prior_exact_source_keys.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3570/verified_handoff.json')
HISTORY=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();lead,prior,history=map(read,[LEAD,PRIOR,HISTORY]);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];known={historical_key(r) for r in read(lp)['contextual_story_natural_dialogue_pass_v1871']['record_keys']};image,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds');assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==lead['current_ROM_sha256'];a,b=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,image]];groups=deepcopy(lead['blocks']);rows=[]
    for g in groups:
        assert sha(a[g['block']])==g['clean_block_sha256'] and sha(b[g['block']])==g['current_block_sha256']
        for i,r in enumerate(g['records']):
            assert historical_key(r) not in known
            for data,ref,k in [(a[g['block']],r['source_reference'],'source_hex'),(b[g['block']],r['current_reference'],'current_hex')]:
                at=ref['offset'];v=bytes.fromhex(r[k]);assert data[at:at+len(v)]==v and data[at+len(v)]==0 and data[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
            r.update(kind='system-FE' if r['source_selector']==254 else 'progressive',source_presentation_prefix_hex=format(r['source_selector'],'02x'),native_command_extent=r['source_native_extent'],spoken_sequence_index=i,ordinary_predecessor_English_not_translation_source=True,current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0);rows.append(r)
        g.update(source_block_sha256=g['clean_block_sha256'],source_native_commands=g['all_clean_native_commands'],current_native_commands=g['all_current_native_commands'],source_current_native_command_shape_exact=True)
    assert len(rows)==38 and image.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4') and sha(Path(history['actual_historical_snapshot']).read_bytes())==history['actual_historical_snapshot_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'all38_clean_current_complete_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(image.read_file('/data/EV2.DK4')),actual_historical_snapshot=history['actual_historical_snapshot'],actual_historical_snapshot_sha256=history['actual_historical_snapshot_sha256'],historical_snapshot_ROM=history['historical_snapshot_ROM'],historical_snapshot_is_Lil_London_not_selected_B142_B145=True,blocks=groups,records=rows,typed_choice_records=[],typed_actor_style_records=[],source_macro_counts={'FI':2,'FA':0,'FO':0},total_editorial_objects=38,speech_objects=38,ordinary_source_speeches=37,system_FE_panels=1,source_selectors=[2,4,9,13,16,20,23,109,171,254],source_static_actor_selectors=[2,4,9,13,16,20,23,109,171],source_native_commands=91,source_relative_sites=25,source_0D_and_printable6D_are_unreviewed_current_scope_not_older_technical_reaudit=True,current_native_full_context_gloss_and_oldEnglish_comparison_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [LEAD,PRIOR,HISTORY,Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('38 new source/current objects bound:37 progressive,one FE,FI2,25 relative sites;no credit.')
