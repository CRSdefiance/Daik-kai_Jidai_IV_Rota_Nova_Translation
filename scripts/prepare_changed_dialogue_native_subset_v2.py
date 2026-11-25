"""Bind native subset consumer counts to its actual immutable membership."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_changed_dialogue_native_subset.py').read_text(encoding='utf-8'),{
    "    manuscript=args.out/'manuscript.json';save(manuscript,subset)":
        """    subset.update(blocks=sorted({r['block'] for r in subset['records']}),
        physical_speech_objects=sum(r['kind'] in ['progressive','system-FE'] for r in subset['records']),
        ordinary_speech_objects=sum(r['kind']=='progressive' for r in subset['records']),
        FE_speech_objects=sum(r['kind']=='system-FE' for r in subset['records']),
        typed_choice_objects=sum(r['kind']=='typed-choice-label' for r in subset['records']))
    manuscript=args.out/'manuscript.json';save(manuscript,subset)""",
})
exec(compile(source,__file__+'::same-bound-subset-with-complete-consumer-counts','exec'),globals())
