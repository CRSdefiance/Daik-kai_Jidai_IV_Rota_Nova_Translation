"""Bind40 uncredited physical speeches and preserve the distinct packed-control risk."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B141_SC3_B109_next_source_v3495')
DIAGNOSTIC=Path('work/analysis/raw_B141_SC3_B109_diagnostic_v3493/raw_header_and_original_native_boundaries.json')
CONTROL=Path('work/analysis/raw_SC3_B109_control_finding_v3494c/source_packed_UI_control_bytes_replaced_by_Jam.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v3492/verified_handoff.json');lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];ledger=read(lp);known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};diagnostic,control=map(read,[DIAGNOSTIC,CONTROL]);clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(diagnostic['current_ROM']);assert sha(Path(diagnostic['current_ROM']).read_bytes())==prior['candidate_sha256']==control['current_ROM_sha256']
    groups=[];allrows=[];copy_candidates=[]
    for unit in diagnostic['results']:
        path,n=unit['file_path'],unit['block'];specs={v['version']:v for v in unit['versions']};jp,en=[IlnkContainer.parse(im.read_file(path)).blocks[n] for im in [clean,current]];rows=[]
        assert sha(jp)==specs['clean']['block_sha256'] and sha(en)==specs['current']['block_sha256'] and not any(v['header_disagreements'] for v in specs.values())
        a,b=specs['clean']['native_4000_commands'],specs['current']['native_4000_commands'];assert len(a)==len(b)
        for s,c in zip(a,b,strict=True):
            at,now=s['offset']+5,c['offset']+5;raw=jp[at:jp.index(b'\0',at+1)];value=en[now:en.index(b'\0',now+1)];ident=f'DK4_MES_B{n}_R{jp[:at].count(bytes([0])):04d}';assert (path,ident) not in known and raw and raw[0]==value[0] and jp[at-5:at+1]==en[now-5:now+1] and s['native_extent']==c['native_extent']
            row=dict(id=ident,file_path=path,block=n,source_reference=dict(offset=at,bytes=len(raw),header_offset=at-5),current_reference=dict(offset=now,bytes=len(value),header_offset=now-5),source_record_index=jp[:at].count(b'\0'),current_record_index=en[:now].count(b'\0'),source_hex=raw.hex(),current_hex=value.hex(),source_Japanese=raw[1:].decode('cp932'),source_complete_preamble_hex=jp[at-5:at+1].hex(),source_selector=raw[0],source_native_extent=s['native_extent'],ancestor_0100_offsets=s['ancestor_0100_offsets'],kind='progressive-structural-lead;current-native-consumer-not-yet-bound',older_English_raw_hex_separate_not_translation_source=True,current_voice_macro_entry_conditional_and_whole_exchange_gloss_comparison_pending=True,source_prose_or_completion_credit_added=False)
            rows.append(row);allrows.append(row)
        groups.append(dict(file_path=path,block=n,source_header_hex=jp[:4].hex(),current_header_hex=en[:4].hex(),source_block_sha256=sha(jp),current_block_sha256=sha(en),source_bytes=len(jp),current_bytes=len(en),source_native_commands=specs['clean']['complete_native_commands'],current_native_commands=specs['current']['complete_native_commands'],records=rows,physical_speeches=len(rows),source_macro_counts={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in rows) for m in ['FI','FA','FO']},source_selectors=sorted({r['source_selector'] for r in rows}),all_complete_speech_preambles_and_native_speech_extents_equal=True,full_command_shape_equal=[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in specs['clean']['complete_native_commands']]==[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in specs['current']['complete_native_commands']],outer_loader_entry_and_runtime_eligibility_not_proven=True))
    assert len(allrows)==40 and len({historical_key(r) for r in allrows})==40 and [g['physical_speeches'] for g in groups]==[14,26] and groups[0]['full_command_shape_equal'] and not groups[1]['full_command_shape_equal']
    # Raw exact copies are navigation leads only. They do not prove shared event context.
    for group in groups:
        path,n=group['file_path'],group['block'];blocks=IlnkContainer.parse(clean.read_file(path)).blocks
        for row in group['records']:
            raw=bytes.fromhex(row['source_hex']);normalized=''.join(row['source_Japanese'].split())
            if len(normalized)<12:continue
            for other,block in enumerate(blocks):
                if other==n:continue
                start=0
                while True:
                    at=block.find(b'\0\x40\xff\xff\0'+raw+b'\0',start)
                    if at<0:break
                    pos=at+5;ident=f'DK4_MES_B{other}_R{block[:pos].count(bytes([0])):04d}';copy_candidates.append(dict(id=row['id'],file_path=path,other_block=other,other_id=ident,other_source_offset=pos,exact_source_hex=raw.hex(),other_key_previously_reviewed=(path,ident) in known,raw_exact_match_not_entry_or_context_approval=True));start=at+1
    ROOT.mkdir(parents=True)
    for g in groups:
        text='\n\n'.join(f"{r['id']} offset{r['source_reference']['offset']} selector{r['source_selector']:02X}\n{r['source_Japanese']}" for r in g['records']);(ROOT/f"SC{2 if g['file_path']=='/data/SC2.DK4' else 3}_B{g['block']}_complete_clean_exchange.txt").write_text(text,encoding='utf-8')
    save(ROOT/'all40_clean_current_source_and_packed_control_leads.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=diagnostic['current_ROM'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(current.read_file('/__arm9__.bin')),prior_verified_handoff='work/analysis/editorial_handoff_verification_v3492/verified_handoff.json',blocks=groups,records=allrows,physical_speeches=40,unique_player_facing_scope_and_entry_classification_pending=True,all40_complete_source_current_speech_preambles_and_extents_bound=True,all40_uncredited_source_keys_nonoverlapping4991_reviewed=True,nontrivial_raw_exact_copy_candidates=copy_candidates,SC2_B141_old_default_result_header_failure_resolved_by_explicit_unmatched_structural_walk_not_prose_approval=True,SC2_B141_source_money_control630A_C200_and_predicates_require_current_native_binding=True,SC3_B109_packed_UI_control_restoration_required=control['restore_owned_range'],SC3_B109_control_finding=str(CONTROL),SC3_B109_control_finding_sha256=sha(CONTROL.read_bytes()),SC3_B109_4500_configuration_changed_and4684_original_control_overwritten=True,source_UI_resource_bodies_and_extra2020_actual_context_effects_unexecuted=True,no_observed_game_crash_or_selected_scene_claim=True,source_0D_older_record_reaudit_still_separate_later=True,whole_clean_exchanges_present_but_fresh_gloss_voice_and_oldEnglish_comparison_not_approved=True,no_ROM_registry_ledger_review_orcompletion_change=True,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [DIAGNOSTIC,CONTROL,Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(physical_source_speeches=40,SC2_B141=14,SC3_B109=26,raw_nontrivial_copy_candidates=len(copy_candidates),already_reviewed_keys=0,SC3_control_restoration_pending=True,new_credit=0))
