"""Correct the final-frame label:13600 is a rats notice,not normal Sea View."""
import inspect,struct
from pathlib import Path
from scripts import verify_hot_spring_actual_v1628 as previous
from scripts.verify_village_wrap_v608 import read
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hot_spring_editorial import current_entries
if __name__=='__main__':
    rom=NdsImage.open(previous.ROM);arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    raw=(previous.CAP/'frame_013600_arm9_ram.bin').read_bytes();owner=struct.unpack_from('<I',arm,0x552A0)[0]-0x02000000
    text=raw[owner+0x2030:owner+0x2230].split(b'\0')[0]
    assert b'Rats!' in text and b'Food' in text
    matching=[e.message_id for e in entries if e.text==text];assert matching
    source=inspect.getsource(previous)
    old="'normal_final_Sea_View13600_actually_viewed':True";assert source.count(old)==1
    source=source.replace(old,"'terminal13600_is_original_rats_notice_not_normal_Sea_View':True,'terminal_rats_message_IDs':"+repr(matching)+",")
    # Remove the duplicate separator following the substituted dictionary fields.
    source=source.replace(repr(matching)+",,",repr(matching)+",")
    source=source.replace("ROOT=Path('work/analysis/hot_spring_actual_v1628')","ROOT=Path('work/analysis/hot_spring_actual_v1628b')")
    old="'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}"
    new="'supersedes_terminal_label_only':'work/analysis/hot_spring_actual_v1628/two_original_hot_spring_discovery_and_minus15_visits.json','normal_returns_claimed_only_at10000_and11700':True,"+old
    assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
