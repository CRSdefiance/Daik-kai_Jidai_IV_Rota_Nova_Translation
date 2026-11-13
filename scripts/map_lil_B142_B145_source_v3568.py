"""Bind38 untouched source/current speeches and reconcile130 already-reviewed exact keys."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_next_source_v3568')
INVENTORY=Path('work/analysis/lil_B142_B148_clean_scope_v3567/complete_clean_B142_B148_next_exchange_inventory.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3566/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,inventory=map(read,[PRIOR,INVENTORY]);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];ledger=read(lp);known={historical_key(r):r for g in ledger['completed_editorial_families'] for r in g['records']};image=NdsImage.open(prior['candidate']);clean=NdsImage.open('work/clean.nds');a,b=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,image]];native,walker,inventory_source=scoped_inventory();groups=[];rows=[];overlap=[]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and not inventory['unclassified']
    for group in inventory['blocks']:
        if group['block'] in [146,147,148]:
            assert all(r['already_contextually_reviewed'] for r in group['records'])
            for r in group['records']:
                old=known[historical_key(r)];assert old['source_hex']==r['source_hex'];overlap.append(dict(file_path=r['file_path'],id=r['id'],block=r['block'],source_hex=r['source_hex'],existing_final_candidate=old.get('completed_candidate_reference'),no_new_credit=True))
            continue
        n=group['block'];assert n in [142,143,144,145] and not any(r['already_contextually_reviewed'] for r in group['records']);commands,speeches=native(image.read_file('/__arm9__.bin'),b[n]);sourcecommands=group['complete_native_commands'];shape=lambda cs:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in cs];assert shape(commands)==shape(sourcecommands) and len(speeches)==len(group['records']);selected=[]
        for original,c in zip(group['records'],speeches,strict=True):
            r=deepcopy(original);at=c['offset']+5;value=b[n][at:b[n].index(b'\0',at+1)];assert b[n][at-5:at+1].hex()==r['source_complete_preamble_hex'] and value[0]==r['source_selector'] and historical_key(r) not in known
            r.update(current_reference=dict(offset=at,bytes=len(value),header_offset=at-5),current_record_index=b[n][:at].count(b'\0'),current_hex=value.hex(),current_native_extent=c['native_extent'],source_kind='system-FE' if r['source_selector']==254 else 'progressive',current_native_voice_macro_entry_and_context_pending=True,source_prose_or_completion_credit_added=0);selected.append(r);rows.append(r)
        groups.append(dict(block=n,clean_block_sha256=sha(a[n]),current_block_sha256=sha(b[n]),source_bytes=len(a[n]),current_bytes=len(b[n]),source_header_hex=a[n][:4].hex(),current_header_hex=b[n][:4].hex(),all_clean_native_commands=sourcecommands,all_current_native_commands=commands,records=selected,physical_speeches=len(selected),source_selectors=group['source_selectors'],source_macro_counts=group['source_macro_counts'],FE_panels=group['FE_panels'],relative_sites=group['relative_sites'],all_complete_preambles_and_native_command_shapes_equal=True,entry_copy_voices_controls_and_full_clean_context_still_require_review=True))
    assert len(rows)==38 and len(overlap)==130 and len(groups)==4 and sum(g['FE_panels'] for g in groups)==1 and sum(g['relative_sites'] for g in groups)==25
    ROOT.mkdir(parents=True)
    for g in groups:(ROOT/f"SC2_B{g['block']}_complete_clean_exchange.txt").write_text('\n\n'.join(r['id']+' selector'+format(r['source_selector'],'02X')+'\n'+r['source_Japanese'] for r in g['records']),encoding='utf-8')
    save(ROOT/'all38_unreviewed_clean_current_and130_prior_exact_source_keys.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(image.read_file('/data/EV2.DK4')),source_inventory=str(INVENTORY),source_inventory_sha256=sha(INVENTORY.read_bytes()),prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),blocks=groups,records=rows,total_physical_speech_leads=38,ordinary_progressive_leads=37,system_FE_leads=1,relative_sites=25,total_native_commands=91,source_macro_counts={'FI':2,'FA':0,'FO':0},source_static_selectors=[2,4,9,13,16,20,23,109,171],source_system_selector=254,all38_source_current_complete_preambles_extents_and_headers_bound=True,source_transcripts_extracted_not_yet_fully_read_or_gloss_approved=True,all38_uncredited_keys_exclude5031_reviewed=True,exact_reviewed_B146_B148_source_reconciliation=overlap,excluded_already_reviewed_records=130,B141_exact_source_copy_in_B142_still_unreviewed=inventory['exact_prior_B141_copy_navigation_leads'],current_native_voice_macro_entry_controls_full_context_and_oldEnglish_comparison_pending=True,not_full_Lil_or_project_denominator=True,no_ROM_registry_ledger_review_orcompletion_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(next_blocks=[142,143,144,145],new_leads=38,progressive=37,FE=1,relative_sites=25,commands=91,prior_exact_source_keys_reconciled=130,source_FI=2,credit=0))
