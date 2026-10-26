"""Clean-only complete inventory with explicit unmatched result for three-way skips."""
import inspect,traceback
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import inventory_lil_lessons_v1717 as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_after_Crew_Items_clean_scope_v3152')

def scoped_inventory():
    src=inspect.getsource(inherited.walk);needle='(RESULT, OWNER, LENGTH), instruction_limit=20000';assert src.count(needle)==1
    scoped=src.replace(needle,'(RESULT, OWNER, LENGTH, 0xFFFFFFFF), instruction_limit=20000');env=dict(inherited.walk.__globals__);exec(compile(scoped,__file__,'exec'),env);native=env['walk']
    inventory_src=inspect.getsource(inherited.inventory);env=dict(inherited.inventory.__globals__);env['walk']=native;exec(compile(inventory_src,__file__,'exec'),env)
    return env['inventory'],scoped,inventory_src

if __name__=='__main__':
    assert not ROOT.exists();rom=Path('work/clean.nds');image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(rom.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    inventory,scoped,inventory_src=scoped_inventory();ROOT.mkdir(parents=True);(ROOT/'explicit_unmatched_native_walk.py.txt').write_text(scoped,encoding='utf8');(ROOT/'unchanged_inventory_function.py.txt').write_text(inventory_src,encoding='utf8')
    fresh=read('translations/editorial_review_current_v1.json')['contextual_story_natural_dialogue_pass_v1871'];known={(r['file_path'],r['id'])for r in fresh['record_keys']};results=[];failures=[]
    for n in range(101,121):
        block=blocks[n]
        try:commands,speeches=inventory(arm,block)
        except AssertionError:
            failures.append(dict(block=n,source_block_sha256=sha(block),diagnostic=traceback.format_exc()));continue
        rows=[]
        for c in speeches:
            at=c['offset']+5;raw=block[at:block.index(bytes([0]),at)];ident=f'DK4_MES_B{n}_R{block[:at].count(bytes([0])):04d}'
            rows.append(dict(id=ident,offset=at,bytes=len(raw),source_hex=raw.hex(),source_preamble_hex=block[at-5:at+1].hex(),prefix=raw[0],Japanese=raw[1:].decode('cp932'),native_extent=c['native_extent'],ancestor_0100_offsets=c['ancestor_0100_offsets'],already_contextually_completed=('/data/SC2.DK4',ident)in known))
        results.append(dict(block=n,source_block_sha256=sha(block),commands=commands,records=rows,speeches=len(rows),FE_panels=sum(r['prefix']==254 for r in rows),typed_menu_2100_commands=sum(c['word']==0x2100 for c in commands),typed_menu_4100_commands=sum(c['word']==0x4100 for c in commands),prefixes=sorted({r['prefix']for r in rows}),all_canonical_raw_headers_equal_complete_typed_speech_set=True))
    assert not failures and len(results)==20
    save(ROOT/'complete_clean_next_exchange_inventory.json',dict(source_ROM=str(rom),source_ROM_sha256=sha(rom.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),blocks=results,unclassified=failures,explicit_last_result=0xFFFFFFFF,all_source_0100_bodies_recursed_and_all_speech_headers_matched=True,all_0200_0300_0400_skips_unmatched_structural_inventory_not_earned_progress=True,original_global_helpers_unchanged=True,helper_hashes={str(Path(p.__code__.co_filename)):sha(Path(p.__code__.co_filename).read_bytes())for p in [inherited.inventory,inherited.walk]},prior_rejected_inventory='work/analysis/lil_after_Crew_Items_clean_scope_v3150/clean_next_exchange_inventory.json',prior_diagnostic='work/analysis/lil_next_nonstandard_preambles_v3151b/clean_source_nonstandard_header_diagnostic.json',native_0400_semantics_and_all_menu_consumers_still_require_distinct_proofs=True,editorial_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(b['block'],len(b['commands']),b['speeches'],b['FE_panels'],b['typed_menu_2100_commands'],b['typed_menu_4100_commands'])for b in results]);print('NEW',sum(not r['already_contextually_completed']for b in results for r in b['records']),'OVERLAP',sum(r['already_contextually_completed']for b in results for r in b['records']))
