"""Inventory direct retainer-role speech in every clean storyline with complete native context."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retainer_speaker_uses_v7740')
SOURCE=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
if __name__=='__main__':
    assert not ROOT.exists();im=NdsImage.open('work/clean.nds');arm=im.read_file('/__arm9__.bin')
    inventory,walker,invsource=scoped_inventory();blocks=[];summary=[];total_blocks=0
    signatures=[bytes.fromhex('0040ffff00')+bytes([n]) for n in [151,152,153,154,155,156,157,158,159]]
    for route in range(4):
        path=f'/data/SC{route}.DK4';data=im.read_file(path);bank=IlnkContainer.parse(data).blocks;total_blocks+=len(bank)
        selected=[]
        for number,blob in enumerate(bank):
            if not any(s in blob for s in signatures):continue
            commands,speeches=inventory(arm,blob);records=[]
            for speech in speeches:
                at=speech['offset']+5;end=blob.index(0,at+1);raw=blob[at:end]
                records.append(dict(source_record_index=blob[:at].count(b'\0'),source_selector=raw[0],source_hex=raw.hex(),
                    complete_preamble_hex=blob[at-5:at+1].hex(),Japanese=raw[1:].decode('cp932'),
                    source_reference=dict(file_path=path,block=number,header_offset=at-5,offset=at,bytes=len(raw))))
            direct=[r for r in records if r['source_selector'] in [151,152,153,154,155,156,157,158,159]]
            if not direct:continue
            blocks.append(dict(route=route,file_path=path,source_file_sha256=sha(data),block=number,source_block_hex=blob.hex(),
                source_block_sha256=sha(blob),all_native_commands=commands,all_speech_records=records,direct_retainer_speech_records=direct))
            selected.append(dict(block=number,direct_role_speeches=len(direct),complete_speeches=len(records),
                exact_source_references=[r['source_reference'] for r in direct]))
        summary.append(dict(route=route,file_path=path,source_blocks=len(bank),selected_blocks=selected))
    assert total_blocks==1307
    ROOT.mkdir(parents=True);save(ROOT/'all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json',dict(
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(arm),
        initial_Maria_informant_context=str(SOURCE),initial_Maria_informant_context_sha256=sha(SOURCE.read_bytes()),source_blocks_scanned=total_blocks,
        direct_role_selectors=[151,152,153,154,155,156,157,158,159],route_census=summary,selected_native_blocks=blocks,
        exact4000_full_preamble_prefilter_then_original_native_inventory_confirms_every_reported_hit=True,
        no_claim_that_this_literal_census_excludes_dynamic_selector_typed_role_or_other_UI_consumers=True,
        current_nameplate_catalogue_direct_literal_pointer_and_runtime_consumers_still_require_separate_binding=True,
        all_selected_exchanges_clean_only_no_old_English_as_translation_source=True,
        clean_inventory_walker=walker,clean_inventory_function=invsource,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in summary:print('route',r['route'],'selected',[(b['block'],b['direct_role_speeches'],b['complete_speeches']) for b in r['selected_blocks']])
    print('direct role speeches',sum(len(b['direct_retainer_speech_records']) for b in blocks),'complete contextual speeches',sum(len(b['all_speech_records']) for b in blocks))
