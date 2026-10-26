"""Classify rejected new clean-source objects without editorial or display credit."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import inventory_lil_lessons_v1717 as original
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_next_nonstandard_preambles_v3151')
if __name__=='__main__':
    assert not ROOT.exists()
    path=Path('work/clean.nds');image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    text=inspect.getsource(original.inventory);old="    assert raw_headers==[r['offset'] for r in rows]";assert text.count(old)==1
    diagnostic=text.replace(old,'    return commands,rows,raw_headers');env=dict(original.__dict__);exec(compile(diagnostic,__file__,'exec'),env);walk=env['inventory']
    ROOT.mkdir(parents=True);(ROOT/'diagnostic_inventory_source.txt').write_text(diagnostic,encoding='utf8');results=[]
    for n in [105,109,110]:
        block=blocks[n];commands,rows,headers=walk(arm,block);native={r['offset']for r in rows};extra=[]
        assert set(headers)<=native
        for row in rows:
            at=row['offset'];raw=block[at+5:block.index(bytes([0]),at+5)]
            item=dict(offset=at,preamble_hex=block[at:at+6].hex(),source_hex=raw.hex(),source_Japanese=raw[1:].decode('cp932'),record_index=block[:at+5].count(bytes([0])),command=row)
            if at not in headers:extra.append(item)
        result=dict(block=n,source_block_sha256=sha(block),commands=commands,speech_commands=rows,canonical_raw_headers=headers,nonstandard_preambles=extra,all_raw_headers_are_typed_speech_commands=True,global_inventory_helper_unchanged=True,editorial_credit=0,native_display_approval=False)
        results.append(result)
    ledger=read('translations/editorial_review_current_v1.json');fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={(r['file_path'],r['id']) for r in fresh['record_keys']};scope=read('work/analysis/lil_after_Crew_Items_clean_scope_v3150/clean_next_exchange_inventory.json');overlap=[dict(block=b['block'],id=r['id'])for b in scope['blocks']for r in b['records']if ('/data/SC2.DK4',r['id'])in known]
    save(ROOT/'clean_source_nonstandard_header_diagnostic.json',dict(source_ROM=str(path),source_ROM_sha256=sha(path.read_bytes()),diagnostic_only=True,blocks=results,already_contextually_completed_overlap=overlap,source_inventory='work/analysis/lil_after_Crew_Items_clean_scope_v3150/clean_next_exchange_inventory.json',global_helper_sha256=sha(Path(original.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),editorial_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('Already completed overlap:',overlap)
    for b in results:print(b['block'],len(b['speech_commands']),[(r['offset'],r['preamble_hex'],r['source_Japanese'])for r in b['nonstandard_preambles']])
