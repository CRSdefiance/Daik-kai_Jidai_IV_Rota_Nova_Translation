"""Expose distinct original consumers at B22 entry;exclude story predicates and item effects explicitly."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_display_fixture_v3601')
PARENT=Path('out/all_routes_combined_v3561_candidate.nds')
PLAN=Path('work/analysis/lil_B142_B145_relocation_v3593/nested_source_relocation_research.json')
DOC=Path('translations/lil_B142_B145_editorial_manuscript_v4.json')
SELECTED_B144=[5,9,35,39,43,50,75]
if __name__=='__main__':
    assert not ROOT.exists();plan,doc=map(read,[PLAN,DOC]);packet=read(doc['source_context']);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'];parent=NdsImage.open(PARENT);clean=NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin');current_blocks=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;clean_blocks=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks;target_blocks=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks;inventory,_,_=scoped_inventory();b22=current_blocks[22];commands,_=inventory(arm,b22);first=next(c['offset'] for c in commands if c['word']==0x4000);assert first==56 and b22[:4]==bytes.fromhex('43530001');prelude=b22[8:first];fixtures=[];ROOT.mkdir(parents=True)
    for case,blocks in [('clean_Japanese',clean_blocks),('reviewed_English',target_blocks)]:
        sequence=[];text_records=[];offset=first
        for block in [144,145]:
            g=next(g for g in packet['blocks'] if g['block']==block);mapping=next(b for b in plan['blocks'] if b['block']==block)
            for c in g['all_clean_native_commands']:
                row=next((r for r in packet['records'] if r['block']==block and r['source_reference']['header_offset']==c['offset']),None)
                if block==144 and (row is None or row['source_record_index'] not in SELECTED_B144):continue
                if block==145 and c['word'] not in [0x4821,0x4822,0x4823,0x4000,0x4700,0xC200,0]:continue
                mapped=next(m for m in mapping['command_map'] if m['old_offset']==c['offset']);at,extent=(c['offset'],c['native_extent']) if case=='clean_Japanese' else (mapped['new_offset'],mapped['new_extent']);value=blocks[block][at:at+extent];assert int.from_bytes(value[:2],'little')==c['word'];sequence.append(dict(source_block=block,source_offset=c['offset'],source_word=c['word'],fixture_offset=offset,native_extent=len(value),whole_command_hex=value.hex(),text_ID=None if row is None else row['id']))
                if row is not None:assert value[:6].hex()==row['source_complete_preamble_hex'];text_records.append(dict(id=row['id'],source_block=block,source_record_index=row['source_record_index'],fixture_command_offset=offset,source_selector=row['source_selector'],native_extent=len(value),complete_preamble_hex=value[:6].hex(),whole_command_hex=value.hex()))
                offset+=len(value)
        assert len(text_records)==13 and {r['source_selector'] for r in text_records}=={2,13,20,109,254};assert [r['source_word'] for r in sequence if r['source_word']!=0x4000]==[0x4822,0x4821,0x4823,0x4700,0xC200,0];logical=bytearray(b22[:8]+prelude+b''.join(bytes.fromhex(r['whole_command_hex']) for r in sequence));assert len(logical)==offset<0x2400;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+b'\0'*(-len(logical)%4);walk,_=inventory(arm,target);assert len(walk)==9+len(sequence);rompath=Path('out/lil_B142_B145_display_v3601_'+case+'_RESEARCH_ONLY.nds');assert not rompath.exists();image=NdsImage.open(PARENT);newblocks=list(current_blocks);newblocks[22]=target;image.replace_file('/data/SC2.DK4',IlnkContainer(newblocks).to_bytes());image.save(rompath);saved=NdsImage.open(rompath);assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
        for p,v in parent.iter_components():assert saved.read_file(p)==v
        fixtures.append(dict(case=case,research_ROM=str(rompath),research_ROM_sha256=sha(rompath.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=commands[:9],selected_original_objects=sequence,original_text_records=text_records,expected_command_words=[c['word'] for c in walk],all335_other_SC2_blocks_and_all_other_files_components_exact=True))
    save(ROOT/'explicit_source_consumer_B22_fixtures.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),fixtures=fixtures,B144_source_selectors13_109_FE_then_B145_pictures_and_speeches=True,B144_seven_selected_speeches=[f'DK4_MES_B144_R{n:04d}' for n in SELECTED_B144],B145_all_six_speeches_three_pictures_hide_C200_and_end=True,source_B144_predicates_6301_and_upgrade_A000_explicitly_excluded=True,source_B145_four_A000_inventory_and_progression_effects_explicitly_excluded=True,original_B22_nine_initialization_commands_retained_exact=True,not_a_natural_complete_B144_exchange_or_earned_armor_or_item_outcome=True,no_actual_source_event142_143_144_145_selection_or_eligibility_claim=True,not_registered_candidate_or_new_release_parent=True,no_RAM_story_or_roster_or_funds_fixtures=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Two explicit B22-entry display fixtures created:13speeches/Cesare0D/Shipwright6D/FE andoriginal B145pictures/hide. Predicates andlater story effects excluded;not earned progression.')
