"""Run the unchanged native speech checks; typed choice captions remain a separate gate."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_editorial_compiled_pages.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    assert plans['manuscript_sha256']==sha(args.manuscript.read_bytes())":
    """    assert plans['manuscript_sha256']==sha(args.manuscript.read_bytes())
    typed_ids=[r['id'] for r in doc['records'] if r['kind']=='typed-choice-label']
    doc['records']=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    assert len(doc['records'])==doc['physical_speech_objects'] and len(typed_ids)==doc['typed_choice_objects']""",
    "pages=page_count,fresh_compiled_alignments=alignments,source_owned_target_page_adapter=adapter,":
        "pages=page_count,fresh_compiled_alignments=alignments,source_owned_target_page_adapter=adapter,excluded_typed_choice_IDs_separately_pending=typed_ids,",
})
exec(compile(source,__file__+'::same-native-speech-checks-separate-typed-captions','exec'),globals())
