"""Check this exact single eight-body personality object with the unchanged compiler/getter."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'), {
    '    assert len(objects)==8 and cases==64 and sum(len(o[\'physical_record_IDs\']) for o in objects)==48':
    "    assert len(objects)==1 and objects[0]['block']==133 and objects[0]['source_command_offset']==10 and cases==8 and sum(len(o['physical_record_IDs']) for o in objects)==8",
    'physical_alternatives=48,': 'physical_alternatives=8,',
    'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks; virtual prefixes not stored.':
    'PASS1 compiled4100 object/8 physical alternatives/8 original target slot cases/9 semantic rejection checks; virtual prefixes not stored.',
})
exec(compile(source, __file__ + '::source-bound-B133-one-complete-style-object', 'exec'), globals())
