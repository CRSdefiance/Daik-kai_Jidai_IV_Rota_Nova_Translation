"""Replay Inn source consumers and complete registered time arguments on V2171."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/inn_context_v2251')
OLD=Path('scripts/context_inn_v801.py')
if __name__=='__main__':
    assert not ROOT.exists();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    source=OLD.read_text()
    changes={'work/analysis/inn_context_v801':'work/analysis/inn_context_v2251','out/all_routes_combined_v799_candidate.nds':'out/all_routes_combined_v2171_candidate.nds',"raw = (LIVE/'frame_004000_arm9_ram.bin').read_bytes()":"raw = Path("+repr(snapshot['path'])+").read_bytes()", "assert sha(ROM.read_bytes()) == 'f855781b6b2a23482874a81c4d3f8f77262fe7f7db2846399b1409da8cc67c79'":"assert sha(ROM.read_bytes()) == '4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a'", "assert arm[lo:hi] == clean[lo:hi], hex(lo)":"expected = bytearray(clean[lo:hi])\n        for at in (0x5CB2C,0x5CB30,0x5CB34,0x5CB38):\n            if lo<=at<hi:expected[at-lo:at-lo+4]=arm[at:at+4]\n        assert arm[lo:hi] == bytes(expected), hex(lo)", "b'This Mo'":"b'This month'", "b'Last Mo'":"b'Last month'", "b' Mo. Ago'":"b' months ago'", "=='Last Mo'":"=='Last month'", "japanese=clean[p-BASE:].split(b'\\0')[0].decode('cp932')":"japanese=clean[struct.unpack_from('<I',clean,at)[0]-BASE:].split(b'\\0')[0].decode('cp932')", "live_RAM=str(LIVE/'frame_004000_arm9_ram.bin')":"live_RAM="+repr(snapshot['path'])}
    for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    arm=NdsImage.open('out/all_routes_combined_v2171_candidate.nds').read_file('/__arm9__.bin');prior=NdsImage.open('out/all_routes_combined_v803_candidate.nds').read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    pointers=[]
    for at in(0x5CB2C,0x5CB30,0x5CB34,0x5CB38):
        assert arm[at:at+4]==prior[at:at+4];p=struct.unpack_from('<I',arm,at)[0]-0x02000000;value=arm[p:p+64].split(bytes(1))[0];assert value==prior[p:p+64].split(bytes(1))[0]
        pointers.append(dict(field=at,source_pointer=struct.unpack_from('<I',clean,at)[0],registered_pointer=p+0x02000000,current_text_hex=value.hex(),registered_V803_pointer_and_string_exact=True))
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,source_code_exact_except_four_registered_time_pointers=pointers,current144_full_month_phrases_not_superseded_abbreviations=True,CPU_event_fields_months_and_fragments_not_naturally_occurring_gameplay=True,no_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
