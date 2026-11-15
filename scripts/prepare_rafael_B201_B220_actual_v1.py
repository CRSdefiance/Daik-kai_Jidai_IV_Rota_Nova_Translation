"""Prepare focused scenes using exact relocated offsets for repeated-caption menus."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


TEMPLATE=Path('scripts/prepare_reviewed_dialogue_fixtures_v1.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    "                command = next(c for c in groups[request['block']]['all_target_commands'] if c['whole_command_hex'] == proof['target_object_hex'])":
        """                group=groups[request['block']]
                item=next(q for q in group['native_objects'] if q['old_offset']==proof['source_command_offset'] and q['word']==proof['source_word'])
                assert item['compiled_hex']==proof['target_object_hex']
                saved=next(q for q in stored['typed_objects'] if q['block']==request['block'] and q['offset']==item['new_offset'])
                assert saved['object_hex']==item['compiled_hex']
                command=next(c for c in group['all_target_commands'] if c['offset']==item['new_offset'])
                assert command['whole_command_hex']==proof['target_object_hex']""",
    'ORDINARY, Path(__file__)':'ORDINARY,TEMPLATE,Path(__file__)',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-native-fixture-with-exact-distinct-menu-ownership','exec'),globals())

