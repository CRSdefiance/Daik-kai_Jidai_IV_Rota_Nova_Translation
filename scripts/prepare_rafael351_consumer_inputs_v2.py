"""Keep the two already present caption bindings;restore only the eight missing fields."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL=Path('scripts/prepare_rafael351_consumer_inputs_v1.py')
source=checked_text(ORIGINAL.read_text(encoding='utf-8'),{
    "            assert 'current_choice_object_hex' not in b\n            b['current_choice_object_hex']=actual['current_choice_object_hex'];changed.append(b['id'])":
        "            if 'current_choice_object_hex' in b:\n                assert b['current_choice_object_hex']==actual['current_choice_object_hex']\n            else:\n                b['current_choice_object_hex']=actual['current_choice_object_hex'];changed.append(b['id'])",
    'assert len(changed)==10':'assert len(changed)==8',
    'ten_exact_current_compound_caption_bindings_restored_no_prose_controls_decisions_or_gates_changed':
        'all10_current_compound_caption_bindings_qualified_eight_restored_no_prose_controls_decisions_or_gates_changed',
    'Restored ten exact current compound-caption fields;':'Restored eight missing current compound-caption fields;allten exact bindings qualified;',
    '[IDENTITY,MACROS,default_path,Path(__file__)]':'[IDENTITY,MACROS,default_path,ORIGINAL,Path(__file__)]',
    '[DOC,OBJECTS,IDENTITY,MACROS,PLAN,NATIVE,STYLE,OUT,Path(__file__)]':'[DOC,OBJECTS,IDENTITY,MACROS,PLAN,NATIVE,STYLE,OUT,ORIGINAL,Path(__file__)]',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-bindings-preserve-the-two-existing-captions','exec'),globals())
