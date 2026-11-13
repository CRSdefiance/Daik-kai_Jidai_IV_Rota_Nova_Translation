"""Focused current/reviewed typed-menu constructor fixtures;no B166 story activation claim."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_menu_fixture_v4076')
PARENT=Path('out/all_routes_combined_v4046_candidate.nds')
WIDTHS=Path('work/analysis/lil_B166_menu_diagnostic_v4070/original_VM_widths_and_preserved_failed_probe.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(WIDTHS);parent=NdsImage.open(PARENT);arm=parent.read_file('/__arm9__.bin');bank=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;native,_,_=scoped_inventory();commands,_=native(arm,bank[22]);first=next(c['offset'] for c in commands if c['word']==0x4000);assert first==56;prelude=bank[22][8:first];assert len(commands[:9])==9 and sum(c['word']==0xA000 for c in commands[:9])==4;ROOT.mkdir(parents=True);fixtures=[]
    for case in d['cases']:
        value=bytes.fromhex(case['object_hex']);raw=bytearray(bank[22][:8]+prelude+value+bytes(4));struct.pack_into('<H',raw,4,len(raw)-8);raw=bytes(raw)+bytes(-len(raw)%4);walk,speech=native(arm,raw);assert len(walk)==11 and not speech and walk[-2]['word']==0x2100 and walk[-1]['word']==0 and bytes.fromhex(walk[-2]['whole_command_hex'])==value
        path=Path(f'out/lil_B166_menu_v4076_{case["version"]}_RESEARCH_ONLY.nds');assert not path.exists();image=NdsImage.open(PARENT);blocks=list(bank);blocks[22]=raw;image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(path);saved=NdsImage.open(path)
        assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
        fixtures.append(dict(case=case['version'],research_ROM=str(path),research_ROM_sha256=sha(path.read_bytes()),original_B22_nine_init_commands=commands[:9],fixture_block_hex=raw.hex(),all11_fixture_commands=walk,typed_menu_object_hex=value.hex(),typed_menu_offset=56,logical_menu_width_px=case['width_px'],expected_native_menu_rectangle=case['VM']['native_menu_rectangle'],source_B166_menu_offset=2152,no_B166_speech_or_branch_or_recruitment_effect=True))
    save(ROOT/'focused_typed_menu_constructor_fixtures.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),source_width_diagnostic=str(WIDTHS),source_width_diagnostic_sha256=sha(WIDTHS.read_bytes()),fixtures=fixtures,only_B22_entry_ROM_fixture_not_natural_source_event166=True,original_B22_four_initialization_effects_retained=True,no_RAM_roster_funds_or_savestate_fixture=True,no_registry_release_or_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Two focused original/reviewed menu fixtures created;no B166 story coverage.')
