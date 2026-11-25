"""Use the proven full-buffer native catalogue check with explicit qualified inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE = Path('scripts/check_rafael_B36_B41_stored_catalogue.py')
source = checked_text(TEMPLATE.read_text(encoding='utf-8'), {
    "if __name__=='__main__':\n    assert not ROOT.exists()":
        """if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['stored','current','qualification','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    ROOT,STORED,CURRENT=args.out,args.stored,args.current
    assert not ROOT.exists()""",
    "assert ctx.receipt()==runtime==current['runtime']":
        """qualification=load(args.qualification)
    assert ctx.receipt()==runtime==qualification['current_runtime']
    assert current['runtime']==qualification['previous_runtime']
    assert qualification['exact_ARM9_COMMON_font_andcomplete_actor_array'] and qualification['owned_source_blocks_exact']""",
    'assert len(rows)==175 and': 'assert len(rows)==len(stored[\'records\']) and',
    'assert len(previous_aliases)==3': "assert all(r in {q['id'] for q in stored['records']} for r in previous_aliases)",
    'all175_stored_effective_body_bindings.json': 'all_stored_effective_body_bindings.json',
    '[STORED,CURRENT,Path(original.__file__),Path(__file__)]': '[STORED,CURRENT,args.qualification,TEMPLATE,Path(original.__file__),Path(__file__)]',
    '175 newly stored bodies survive original catalogue lookup byte forbyte;three former alias overrides cannot restore old glyphs orwrapping.':
        'All newly stored bodies survive the original catalogue lookup byte forbyte;source-owned aliases cannot restore old glyphs orwrapping.',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-native-full-buffer-SP-and4MiB-canaries-qualified-current-inputs', 'exec'), globals())
