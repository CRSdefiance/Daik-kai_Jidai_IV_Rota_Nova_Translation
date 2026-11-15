"""Run the established complete three-choice checks on one source-bound menu."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_editorial_three_choice_display.py').read_text(encoding='utf-8'), {
    "assert len(rows)==doc['typed_choice_objects']==15": "assert len(rows)==doc['typed_choice_objects']==3",
    'assert len(groups)==5': 'assert len(groups)==1',
    'native_provider_alignments=30,bridged_modal_returns=120': 'native_provider_alignments=6,bridged_modal_returns=24',
    'PASS5 three-choice objects/15 labels/30 provider alignments/120 bridged returns/60 complete planes':
        'PASS1 three-choice object/3 labels/6 provider alignments/24 bridged returns/12 complete planes',
})
exec(compile(source, __file__ + '::same-three-choice-one-object', 'exec'), globals())
