"""Inventory the next clean exchanges without prose or completion credit."""
import traceback
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_after_B119_clean_scope_v3257b')
if __name__=='__main__':
    assert not ROOT.exists();rom=Path('work/clean.nds');image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(rom.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==4575
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    inventory,walker,invsource=scoped_inventory();ROOT.mkdir(parents=True);results=[];failures=[]
    for n in range(122,141):
        block=blocks[n]
        try:commands,speeches=inventory(arm,block)
        except (AssertionError,ValueError) as e:
            failures.append(dict(block=n,source_block_sha256=sha(block),error=repr(e),diagnostic=traceback.format_exc()));continue
        rows=[]
        for c in speeches:
            at=c['offset']+5;raw=block[at:block.index(bytes([0]),at)];ident=f'DK4_MES_B{n}_R{block[:at].count(bytes([0])):04d}'
            try:jp=raw[1:].decode('cp932')
            except UnicodeDecodeError:jp=None
            rows.append(dict(id=ident,file_path='/data/SC2.DK4',block=n,source_reference=dict(offset=at,bytes=len(raw),header_offset=at-5),source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_selector=raw[0] if raw else None,zero_length_native4000_requires_original_consumer_classification=not raw,whole_native_command_hex=c['whole_command_hex'],source_Japanese=jp,complete_prefix_native_binding_and_whole_exchange_review_pending=True,native_extent=c['native_extent'],ancestor_0100_offsets=c['ancestor_0100_offsets'],already_contextually_completed=('/data/SC2.DK4',ident) in known))
        results.append(dict(block=n,source_block_sha256=sha(block),source_bytes=len(block),commands=commands,records=rows,speeches=len(rows),nonempty_physical_speech_bodies=sum(bool(r['source_hex']) for r in rows),zero_length_native4000_objects=sum(not r['source_hex'] for r in rows),FE_panels=sum(r['source_selector']==254 for r in rows),typed_text_command_words={hex(w):sum(c['word']==w for c in commands) for w in sorted({c['word'] for c in commands if 0x2000<=c['word']<0x3000 or c['word']==0x4100})},prefixes=sorted({r['source_selector'] for r in rows if r['source_selector'] is not None}),all_physical_source_headers_match_native_speech_inventory=True))
    (ROOT/'explicit_unmatched_native_walk.py.txt').write_text(walker,encoding='utf-8');(ROOT/'unchanged_inventory_function.py.txt').write_text(invsource,encoding='utf-8')
    save(ROOT/'complete_clean_next_exchange_inventory.json',dict(source_ROM=str(rom),source_ROM_sha256=sha(rom.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),blocks=results,unclassified=failures,explicit_last_result=0xFFFFFFFF,all0100_bodies_recursed_and_physical_speech_headers_matched_in_classified_blocks=True,all0200_0300_0400_unmatched_structural_inventory_not_runtime_eligibility=True,next_scope=list(range(122,141)),B120_B121_and_all_prior_completed_families_excluded=True,raw_B141_and_SC3_B109_classification_remain_separate_open_leads=True,canonical_Maria_SC3_B97_32_targets_still_queued_uncredited=True,whole_clean_context_current_source_mapping_typed_text_and_all_prose_native_release_gates_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(b['block'],len(b['commands']),b['speeches'],b['FE_panels'],b['typed_text_command_words']) for b in results]);print(dict(classified_blocks=len(results),unclassified_blocks=len(failures),physical_speeches=sum(b['speeches'] for b in results),not_previously_completed=sum(not r['already_contextually_completed'] for b in results for r in b['records']),zero_length_native4000_objects=sum(b['zero_length_native4000_objects'] for b in results),new_editorial_credit=0))
