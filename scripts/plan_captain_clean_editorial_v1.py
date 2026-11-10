"""Run the established full-width planner with explicit source archive and measured macros."""
import argparse
from pathlib import Path
import sys
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap = argparse.ArgumentParser(description=__doc__,add_help=False)
    ap.add_argument('--root',type=Path,required=True)
    args, remaining = ap.parse_known_args()
    doc = load(args.root/'formatting_v1/formatting_input.json')
    macros = load(args.root/'formatting_v1/native_macro_measurements.json')
    assert macros['runtime']==doc['runtime']
    assert doc['file_path'] in ['/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4']
    assert {r['file_path'] for r in doc['records']}=={doc['file_path']}
    source = checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'), {
        "Path('work/Maria_B0_B32_clean_20261109')":f'Path({str(args.root)!r})',
        'assert MACRO_LENGTHS==dict(FI=5,FA=2,FO=7,FU=15)':f"assert MACRO_LENGTHS=={macros['macro_ascii_lengths']!r}",
        "doc['file_path']=='/data/SC3.DK4'":f"doc['file_path']=={doc['file_path']!r}",
        "doc['physical_speech_objects']==299":f"doc['physical_speech_objects']=={doc['physical_speech_objects']}",
        "doc['blocks']==list(range(15))+list(range(16,33))":f"doc['blocks']=={doc['blocks']!r}",
        "len(bound)==len(original)==len(doc['records'])==301":f"len(bound)==len(original)==len(doc['records'])=={len(doc['records'])}",
        "assert before[:2]==now[:2]==b'\\0!'":
            "assert before[:2]==now[:2]==int(row['source_word']).to_bytes(2,'little') and row['source_word'] in (0x2100,0x2200) and row['source_count']=={0x2100:2,0x2200:3}[row['source_word']]",
        'assert len(bindings)==299':f"assert len(bindings)=={doc['physical_speech_objects']}",
        "        bindings.append(dict(id=row['id']":
            "        if raw[0]==254 and row.get('native_object_kind')!='4100-style-alternative':assert row['kind']=='system-FE' and row['FE_is_not_an_ordinary_actor_nameplate']\n        bindings.append(dict(id=row['id']",
    })
    sys.argv = [sys.argv[0],*remaining]
    exec(compile(source,__file__+'::same-full-source-current-native-width-phase-andpagination-contract', 'exec'),
        {'__file__':__file__,'__name__':'__main__'})


if __name__ == '__main__':
    main()
