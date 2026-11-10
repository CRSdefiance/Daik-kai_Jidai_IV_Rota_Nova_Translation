"""Research-only reconstruction of speeches plus separately validated native captions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/rebuild_reviewed_editorial_batch.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'from dk4tool.script.reviewed_scene_rebuild import rebuild_block':
        'from dk4tool.script.reviewed_scene_rebuild_v2 import rebuild_block\nfrom dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices',
    "    for arg in ('manuscript','plan','packet','native','out'):":
        "    for arg in ('manuscript','plan','packet','native','menu','out'):",
    "    assert len(doc['records'])==len(layout['records'])==len(native['records']) and not layout['failures']":
    """    assert doc['physical_speech_objects']==len(layout['records'])==len(native['records']) and not layout['failures']
    typed=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    doc['records']=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    menu=load(args.menu)
    assert len(typed)==doc['typed_choice_objects']==2
    assert menu['manuscript_sha256']==sha(args.manuscript.read_bytes()) and not menu['direct_view_pending']
    typed_source,typed_current=[bytes.fromhex(typed[0][key]) for key in ['source_choice_object_hex','current_choice_object_hex']]
    typed_target=compile_choices(typed_source,typed_current,typed,require_formatting=False)
    assert typed_target.hex()==menu['native_choice_object_hex']""",
    "        block=group['block'];current=blocks[block];clean=bytes.fromhex(group['clean_block_hex'])":
    """        block=group['block']
        if block not in doc['blocks']:
            assert block==doc['unchanged_control_only_reference_block'] and not group['records']
            continue
        current=blocks[block];clean=bytes.fromhex(group['clean_block_hex'])""",
    '        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory)':
    """        choices=[]
        if any(r['block']==block for r in typed):
            assert all(r['block']==block for r in typed)
            choices=[dict(id='B'+str(block)+'_native_two_choice',offset=typed[0]['current_reference']['command_offset'],
                current_hex=typed_current.hex(),source_hex=typed_source.hex(),compiled_hex=typed_target.hex(),records=typed)]
        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,choices)""",
    "        command_count=sum(len(g['command_map']) for g in groups),speech_count=len(doc['records']),":
        "        command_count=sum(len(g['command_map']) for g in groups),speech_count=len(doc['records']),typed_choice_count=len(typed),menu=str(args.menu),menu_sha256=sha(args.menu.read_bytes()),",
    "Path('dk4tool/script/reviewed_scene_rebuild.py')":
        "Path('dk4tool/script/reviewed_scene_rebuild.py'),Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),original",
})
exec(compile(source,__file__+'::source-bound-speech-and-menu-reconstruction','exec'),globals())
