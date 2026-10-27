"""Successor uses the verified canonical-mode parser;clean-source guards stay intact."""
from pathlib import Path

if __name__=='__main__':
    path=Path('scripts/author_battle_reactions_v1480.py')
    source=path.read_text(encoding='utf-8')
    old="base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'))"
    new="base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)"
    assert source.count(old)==1
    source=source.replace(old,new)
    old="'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})"
    new="'canonical_parser_predecessor':str(path),'canonical_parser_predecessor_sha256':sha(path.read_bytes()),"+old
    assert source.count(old)==1
    source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
