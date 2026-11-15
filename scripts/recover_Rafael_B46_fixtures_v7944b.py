"""Finalize only the missing fixture manifest after exact in-memory recovery of preserved images/pins."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_fixture_recovery_tools_v7944b');assert not root.exists()
    source=Path('scripts/create_Rafael_B46_fixtures_v7944.py').read_text('utf8')
    begin=source.index("    pins=Path('translations/rom_retention_pins.json')")
    end=source.index("    save(ROOT/'two_complete_source_English_original_Rafael_prelude_fixtures.json'",begin)
    old=source[begin:end]
    new=old.replace('before=pins.read_bytes()',"before=(ROOT/'pins.before.json').read_bytes()")
    new=new.replace(";(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before",";assert pins.read_bytes()==encoded")
    remove="    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())\n"
    assert remove in new;new=new.replace(remove,'')
    assert new!=old
    row=derive('scripts/create_Rafael_B46_fixtures_v7944.py','scripts/finalize_Rafael_B46_fixtures_v7944b.py',{
        'Two complete B46 exchanges/all24 speeches/two choices behindthe original ten-command Rafael prelude.':'Recover the missing B46 manifest by exact in-memory ROM/pin reconstruction;never overwrite preserved artifacts.',
        "assert not ROOT.exists();":"assert ROOT.exists() and not (ROOT/'two_complete_source_English_original_Rafael_prelude_fixtures.json').exists();",
        'assert all(not p.exists() for p in outputs)':'assert all(p.exists() for p in outputs)',
        'fixtures=[];ROOT.mkdir(parents=True)':'fixtures=[];assert ROOT.exists()',
        "i=r['option_index'];base=mc['offset']+6;at=base+":"i=r['option_index'];menu_base=mc['offset']+6;at=menu_base+",
        'image.save(out)':'assert image.rom.save()==out.read_bytes()',
        old:new,
    })
    root.mkdir(parents=True);save(root/'source_locked_recovery.json',dict(derivation=row,
        initial_metadata_failure_andboth_ROMs_andpins_preserved=True,recovered_ROMs_must_equal_complete_reconstruction_before_manifest=True,
        no_ROM_pin_registry_orledger_write_by_recovery=True,new_credit=0,full_goal_complete=False))
