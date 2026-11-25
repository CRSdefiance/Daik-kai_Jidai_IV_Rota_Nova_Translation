"""Keep exact subset membership and report ordinary/style counts for the selected rows."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_editorial_native_subset_v1.py').read_text(encoding='utf-8'),{
    'physical_speech_objects=len(records),ordinary_speech_objects=len(records),typed_choice_objects=0,typed_choice_commands=0,':
        "physical_speech_objects=len(records),ordinary_speech_objects=sum(r.get('native_object_kind')!='4100-style-alternative' for r in records),\n        style_physical_speech_objects=sum(r.get('native_object_kind')=='4100-style-alternative' for r in records),\n        style_command_objects=len({(r['block'],r['source_command_offset']) for r in records if r.get('native_object_kind')=='4100-style-alternative'}),typed_choice_objects=0,typed_choice_commands=0,",
})
exec(compile(source,__file__+'::same-immutable-parent-subset-explicit-style-counts','exec'),globals())
