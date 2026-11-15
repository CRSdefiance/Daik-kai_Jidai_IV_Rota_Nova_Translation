"""Inventory the next seven clean blocks without editorial or gameplay credit."""
import traceback
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B148_clean_scope_v3567')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3566/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read(PRIOR);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];ledger=read(lp);image=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;inventory,walker,inventory_source=scoped_inventory();known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};results=[];failures=[];ROOT.mkdir(parents=True)
    for number in range(142,149):
        block=blocks[number]
        try:commands,speeches=inventory(arm,block)
        except (AssertionError,ValueError) as e:failures.append(dict(block=number,clean_block_sha256=sha(block),error=repr(e),diagnostic=traceback.format_exc(),not_a_game_crash_or_full_source_classification=True));continue
        rows=[]
        for c in speeches:
            at=c['offset']+5;raw=block[at:block.index(b'\0',at+1)];index=block[:at].count(b'\0');ident=f'DK4_MES_B{number}_R{index:04d}'
            rows.append(dict(id=ident,file_path='/data/SC2.DK4',block=number,source_record_index=index,source_reference=dict(offset=at,bytes=len(raw),header_offset=at-5),source_hex=raw.hex(),source_selector=raw[0],source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=raw[1:].decode('cp932'),source_native_extent=c['native_extent'],ancestor_0100_offsets=c['ancestor_0100_offsets'],already_contextually_reviewed=('/data/SC2.DK4',ident) in known))
        (ROOT/f'SC2_B{number}_complete_clean_exchange.txt').write_text('\n\n'.join(r['id']+' selector'+format(r['source_selector'],'02X')+'\n'+r['source_Japanese'] for r in rows),encoding='utf-8')
        results.append(dict(block=number,source_header_hex=block[:4].hex(),source_block_sha256=sha(block),source_block_bytes=len(block),complete_native_commands=commands,records=rows,speeches=len(rows),source_selectors=sorted({r['source_selector'] for r in rows}),source_macro_counts={k:sum(bytes.fromhex(r['source_hex']).count(k.encode()) for r in rows) for k in ['FI','FA','FO']},FE_panels=sum(r['source_selector']==254 for r in rows),typed_menu_2100_commands=sum(c['word']==0x2100 for c in commands),typed_actor_style_4100_commands=sum(c['word']==0x4100 for c in commands),relative_sites=sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands),all_canonical_raw_headers_equal_typed_speech_set=True,current_native_binding_entry_and_context_pending=True))
    (ROOT/'explicit_unmatched_native_walk.txt').write_text(walker,encoding='utf-8');(ROOT/'scoped_inventory_source.txt').write_text(inventory_source,encoding='utf-8');rows=[r for b in results for r in b['records']];copies=[]
    prior_review=read('translations/lil_B141_contextual_final_review_v1.json');jp141={bytes.fromhex(r['source_hex']):r for r in prior_review['records'] if len(''.join(r['source_Japanese'].split()))>=12}
    for r in rows:
        if bytes.fromhex(r['source_hex']) in jp141:copies.append(dict(id=r['id'],block=r['block'],reviewed_B141_id=jp141[bytes.fromhex(r['source_hex'])]['id'],source_hex=r['source_hex'],navigation_lead_only_no_context_or_duplicate_credit=True))
    save(ROOT/'complete_clean_B142_B148_next_exchange_inventory.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),current_registered_ROM=prior['candidate'],current_registered_ROM_sha256=prior['candidate_sha256'],prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),blocks=results,unclassified=failures,physical_source_speeches=len(rows),not_yet_reviewed_physical_speeches=sum(not r['already_contextually_reviewed'] for r in rows),already_reviewed_keys=sum(r['already_contextually_reviewed'] for r in rows),exact_prior_B141_copy_navigation_leads=copies,explicit_unmatched_result=0xFFFFFFFF,source_transcripts_extracted_not_yet_read_or_gloss_approved=True,current_references_voices_macros_entry_conditions_and_controls_pending=True,typed_alternatives_require_separate_inventory_if_any=True,not_full_Lil_or_project_denominator=True,no_new_ROM_registry_ledger_or_review_credit=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(blocks=[dict(block=b['block'],commands=len(b['complete_native_commands']),speeches=b['speeches'],FE=b['FE_panels'],choices=b['typed_menu_2100_commands'],actor_styles=b['typed_actor_style_4100_commands']) for b in results],failures=[r['block'] for r in failures],new_physical_leads=sum(not r['already_contextually_reviewed'] for r in rows),already_reviewed=sum(r['already_contextually_reviewed'] for r in rows),B141_exact_copies=len(copies),credit=0))
