"""Rebuild the final Rafael B221–B240 display batch for stored and emulator checks."""
from pathlib import Path

from scripts.assemble_rafael_B221_B240_offline_v2 import FINAL_NATIVE, OUT
from scripts.plan_rafael_B221_B240_v1 import CURRENT
from scripts.seal_rafael_B221_B240_visual_v1 import VISUAL
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE = Path('scripts/rebuild_reviewed_editorial_batch_v4.py')
REGISTRY = Path('translations/release_stack.json')
source = checked_text(TEMPLATE.read_text(encoding='utf-8'), {
    'from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block':
        'from dk4tool.script.reviewed_scene_rebuild_with_fu_andcompounds_v1 import rebuild_block',
    "len(doc['records'])==323": "len(doc['records'])==270",
    "==len(native['records'])==308": "==len(native['records'])==263",
    '==(260,48,15)': '==(234,29,7)',
    'word=0x2200,': "word=proof['source_word'],",
    "value=compile_choices(source,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']":
        """value=compile_choices(source,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']
            assert rows[0]['source_word']==proof['source_word']==int.from_bytes(value[:2],'little')""",
    "        records=[r for r in ordinary if r['block']==block]":
        """        records=[deepcopy(r) for r in ordinary if r['block']==block]
        for row in records:
            index=row['current_reference']['record_index']
            assert row.get('current_record_index',index)==index
            row['current_record_index']=index""",
    'block==128': 'block==231',
    'unchanged_control_only_blocks=[128],speech_count=260': 'unchanged_control_only_blocks=[231],speech_count=234',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=29,total_rendered_speech_count=263,typed_choice_count=7,compound_objects=7',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=234,style_alternatives=29,menu_labels=7,changed_blocks=19',
    'B111-B130 complete source-bound reconstruction': 'Rafael B221–B240 complete source-bound reconstruction',
    "args=parser.parse_args();assert not args.out.exists()":
        """args=parser.parse_args();assert not args.out.exists()
    visual=load(VISUAL)
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed']
    assert (visual['body_pages'],visual['typed_choice_captions'],visual['source_staged_progressive_pages'])==(279,7,3)
    assert args.native==FINAL_NATIVE and visual['native_sha256']==sha(args.native.read_bytes())
    assert args.packet==CURRENT and args.menu==OUT/'menu.json' and args.styles==OUT/'styles.json'
    assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in visual['sheets'])
    release=load(visual['runtime']['release_proof'])
    assert sha(REGISTRY.read_bytes())==release['registry_sha256']
    assert release['all_eight_registered_final_stages_preserved'] and not release['own_registered_startup_pending']""",
    "[Path(__file__),Path('dk4tool/script/reviewed_scene_rebuild.py')":
        "[TEMPLATE,VISUAL,Path(__file__),Path('dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py'),Path('dk4tool/script/reviewed_scene_rebuild.py')",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-reviewed-rebuild-with-exact-270-object-scope', 'exec'), globals())

