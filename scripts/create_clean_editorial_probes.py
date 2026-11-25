"""Source-owned complete scene fixtures for new native behavior; no translated release."""
import argparse
import struct
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['packet','release','out']:parser.add_argument('--'+arg,type=Path,required=True)
    parser.add_argument('--scenes',nargs='+',required=True);args=parser.parse_args();assert not args.out.exists()
    packet,release=map(load,[args.packet,args.release]);reference=Path(release['candidate'])
    assert not release['own_registered_startup_pending'] and sha(reference.read_bytes())==release['candidate_sha256']
    image=NdsImage.open(reference);arm=image.read_file('/__arm9__.bin');path=packet['file_path'];archive=image.read_file(path);bank=IlnkContainer.parse(archive).blocks
    clean=NdsImage.open(packet['source_ROM']);assert sha(Path(packet['source_ROM']).read_bytes())==packet['source_ROM_sha256']
    clean_bank=IlnkContainer.parse(clean.read_file(path)).blocks;inventory,_,_=scoped_inventory()
    commands,speeches=inventory(arm,bank[42]);first=speeches[0]['offset'];prelude=bank[42][8:first]
    assert first==42 and len(prelude)==34 and prelude==clean_bank[42][8:first]
    initializers=[c for c in commands if c['offset']<first];assert len(initializers)==8
    ordinary_path=Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json');ordinary=load(ordinary_path)
    args.out.mkdir(parents=True);fixtures=[]
    for number,frames in [tuple(map(int,s.split(':'))) for s in args.scenes]:
        group=next(g for g in packet['groups'] if g['block']==number);selected=bytes.fromhex(group['clean_block_hex']);assert selected==clean_bank[number]
        assert selected[:4]==bank[42][:4] and selected[6:8]==bank[42][6:8]
        end=8+struct.unpack_from('<H',selected,4)[0];assert not any(selected[end:])
        logical=bytearray(bank[42][:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        block=bytes(logical)+bytes(-len(logical)%4);mapped,_=inventory(arm,block)
        assert len(block)<0x2400 and len(mapped)==len(group['all_source_commands'])+8
        for original in group['all_source_commands']:
            moved=next(c for c in mapped if c['offset']==original['offset']+34)
            assert moved['word']==original['word'] and moved['whole_command_hex']==original['whole_command_hex'] and moved['native_extent']==original['native_extent']
        target=deepcopy(image);blocks=list(bank);blocks[42]=block;target.replace_file(path,IlnkContainer(blocks).to_bytes())
        assert [p for _,p,v in image.iter_files() if target.read_file(p)!=v]==[path]
        assert all(target.read_file(p)==v for p,v in image.iter_components())
        restore=deepcopy(target);restore.replace_file(path,archive);assert bytes(restore.rom.save())==reference.read_bytes()
        rom=args.out/f'B{number}_source_initialized_RESEARCH_ONLY.nds';rom.write_bytes(bytes(target.rom.save()))
        inputs=args.out/f'B{number}_ordinary_inputs.json';save(inputs,ordinary+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,frames-480,240)])
        fixtures.append(dict(block=number,frames=frames,ROM=str(rom),ROM_sha256=sha(rom.read_bytes()),source_block_sha256=sha(selected),inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),source_complete_commands_preserved=True,fixture_block=42,initializer_bytes=prelude.hex()))
    save(args.out/'fixtures.json',dict(reference=str(reference),reference_sha256=sha(reference.read_bytes()),fixtures=fixtures,source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),
        old_catalogue_may_select_existing_English_not_new_translation=True,initialized_scene_not_natural_optional_activation=True,no_savestate_RNG_roster_role_eventflag_orconditional_override=True,actual_coverage_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    pins=Path('translations/rom_retention_pins.json');values=load(pins)
    for row in fixtures:values.append(dict(path=str(Path(row['ROM']).resolve()),reason='Preserve source-owned B111-B130 native behavior QA fixture;not a registered release. SHA256 '+row['ROM_sha256']))
    save(pins,values);print(dict(source_scene_fixtures=len(fixtures),registered_release=False,actual_coverage_pending=True))

if __name__=='__main__':main()
