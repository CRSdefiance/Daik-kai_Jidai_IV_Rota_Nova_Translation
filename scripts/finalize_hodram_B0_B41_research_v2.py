"""Recover the validated394-story seal and supply explicit v2 name-document metadata."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/finalize_hodram_B0_B41_research_v1.py').read_text(encoding='utf-8'),{
    "assert not any(p.exists() for p in [OUT,FINAL,FINAL_NAMES,FINAL_FIELDS])":
        "assert OUT.is_dir() and not any(OUT.iterdir()) and FINAL.is_file() and not FINAL_NAMES.exists() and not FINAL_FIELDS.exists()",
    '    OUT.mkdir()':'    assert OUT.is_dir() and not any(OUT.iterdir())',
    '    validate_natural_dialogue_batch(doc);save(FINAL,doc)':
        '    validate_natural_dialogue_batch(doc);assert load(FINAL)==doc',
    "        row['actual_changed_header_observed']=row['actor_ID'] in observed":
        """        row['actual_changed_header_observed']=row['actor_ID'] in observed
        row.update(id='ACTOR'+str(row['actor_ID'])+'_SCOPED_NAME',speaker='Source actor '+str(row['actor_ID']),
            context='Progressive/name-constructor identity for exact SC1 dialogue references: '+', '.join(row['context_record_ids']),
            source_meaning='The source-bound name components identify '+row['english']+'. '+row['finding'],
            natural_name_localization_andnative_planes_still_pending=False,
            native_plane_status='complete-qualified-native-planes-anddirect-visual-review',
            representative_gameplay_andregistered_name_layer_pending=True)""",
})
exec(compile(source,__file__+'::same-all-gates-readback-recovery-andexplicit-name-schema','exec'),globals())
