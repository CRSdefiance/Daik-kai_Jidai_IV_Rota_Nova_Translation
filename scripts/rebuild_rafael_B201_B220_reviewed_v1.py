"""Reconstruct the 20 reviewed Rafael blocks for stored script and focused emulator checks."""
from pathlib import Path

from scripts.assemble_rafael_B201_B220_offline_v2 import AFTER, OUT_DIFF
from scripts.rebuild_rafael_B141_B160_reviewed_v1 import TEMPLATE, source as previous
from scripts.plan_rafael_B201_B220_v1 import CURRENT, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


VISUAL = AFTER.with_name('visual_review.json')
REGISTRY = Path('translations/release_stack.json')
source = checked_text(previous, {
    "len(doc['records'])==557": "len(doc['records'])==403",
    "==len(native['records'])==549": "==len(native['records'])==382",
    '==(549,0,8)': '==(382,0,21)',
    "word=0x2100,": "word=proof['source_word'],",
    'speech_count=549': 'speech_count=382',
    'total_rendered_speech_count=549': 'total_rendered_speech_count=382',
    'typed_choice_count=8,compound_objects=4': 'typed_choice_count=21,compound_objects=10',
    'ordinary_speeches=549': 'ordinary_speeches=382',
    'menu_labels=8,changed_blocks=20': 'menu_labels=21,changed_blocks=20',
    'Rafael B141-B160 complete557-object source-bound reconstruction':
        'Rafael B201–B220 complete 403-object source-bound reconstruction for stored and emulator checks',
    "args=parser.parse_args();assert not args.out.exists()":
        """args=parser.parse_args();assert not args.out.exists()
    visual=load(VISUAL)
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed']
    assert (visual['body_pages'],visual['typed_choice_captions'],visual['source_staged_FE_pages'])==(383,21,2)
    assert visual['native_sha256']==sha(args.native.read_bytes()) and args.native==AFTER
    assert args.packet==CURRENT and args.menu==AFTER.with_name('menu.json') and args.styles==AFTER.with_name('styles.json')
    assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in visual['sheets'])
    release=load(visual['runtime']['release_proof'])
    assert sha(REGISTRY.read_bytes())==release['registry_sha256']
    assert release['all_eight_registered_final_stages_preserved'] and not release['own_registered_startup_pending']""",
    "value=compile_choices(source,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']":
        """value=compile_choices(source,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']
            assert rows[0]['source_word']==proof['source_word']==int.from_bytes(value[:2],'little')""",
})

if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-mixed-object-and-inverse-contract','exec'),globals())

