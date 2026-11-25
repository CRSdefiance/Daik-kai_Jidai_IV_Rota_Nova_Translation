"""Preserve all new batch research ROMs; never prune earlier artifacts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B81_B89_editorial_20261101');pins=Path('translations/rom_retention_pins.json')
    before=pins.read_bytes();values=load(pins);known={str(Path(v['path']).resolve()).lower() for v in values}
    paths=[Path('work/analysis/Hodram_B81_B89_rebuild_20261101/reviewed_RESEARCH_ONLY.nds'),
        Path('work/analysis/Hodram_B81_B89_name_research_20261101/story_andname_RESEARCH_ONLY.nds')]
    paths += [Path(r['research_ROM']) for r in load('work/analysis/Hodram_B81_B89_fixtures_20261101/fixtures.json')['fixtures']]
    additions=[]
    for path in paths:
        assert path.exists();name=str(path.resolve())
        if name.lower() in known:continue
        additions.append(dict(path=name,reason='Preserve Hodram B81-B89 editorial,typed-menu andEmilio name-glyph research. Not a registered release or natural activation. SHA256 '+sha(path.read_bytes())))
    backup=root/'pins_before_research.json';assert not backup.exists();backup.write_bytes(before)
    assert pins.read_bytes()==before;save(pins,values+additions)
    save(root/'new_research_pins.json',dict(added=additions,previous_pins_sha256=sha(before),no_deletions=True))
    print('Pinned',len(additions),'new ROMs;preserved all previous pins/artifacts.')
