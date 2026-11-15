"""Correct facility8 binding; retain2251b as non-Inn-context research."""
from pathlib import Path
source=Path('scripts/replay_inn_context_v2251.py').read_text()
source=source.replace('inn_context_v2251','inn_context_v2251c')
old='source=OLD.read_text()';assert source.count(old)==1
source=source.replace(old,'ROOT.mkdir(parents=True);source=OLD.read_text()')
marker="    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
insertion='''    old="    u.mem_write(BASE, raw)"
    replacement=old+"\\n    global_pointer=struct.unpack_from('<I',arm,0x5CD4C)[0]\\n    facility=struct.unpack('<I',u.mem_read(global_pointer,4))[0]+0x10\\n    before=bytes(u.mem_read(BASE,0x800000));facility_before=struct.unpack('<I',u.mem_read(facility,4))[0]\\n    u.mem_write(facility,struct.pack('<I',8));after=bytearray(u.mem_read(BASE,0x800000));after[facility-BASE:facility-BASE+4]=before[facility-BASE:facility-BASE+4]\\n    assert bytes(after)==before\\n    save(ROOT/'CPU_facility_context.json',dict(field=facility,before=facility_before,after=8,only_four_bytes_in8MiB_changed=True,not_an_emulator_fixture_or_actual_Inn_visit=True))"
    assert source.count(old)==1;source=source.replace(old,replacement)
'''
assert source.count(marker)==1;source=source.replace(marker,insertion+marker)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
