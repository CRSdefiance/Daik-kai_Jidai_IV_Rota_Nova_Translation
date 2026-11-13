"""Keep the actual descriptive map label separate from the spoken temple proper name."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_hodram_B301_B310_terms_v1.py').read_text(encoding='utf-8'),{
    "assert '金閣寺' in items[1]['source_Japanese']":"assert items[1]['source_Japanese']=='黄金の寺への地図'",
    'spoken_place_alias=dict(':'spoken_place_forms=dict(',
    'no_new_map_purchase_location_ororiginal_event_trigger_claim=True)':
        "map_label_alone_does_not_prove_Kinkakuji_event_identity=True,\n            no_new_map_purchase_location_ororiginal_event_trigger_claim=True)",
    'source_cultural_andgeographic_statements_not_external_historical_verification=True,':
        "first_binding_attempt_stopped_before_output_on_incorrect_named_map_assumption=True,\n        source_cultural_andgeographic_statements_not_external_historical_verification=True,",
})
env={'__file__':__file__,'__name__':'corrected_descriptive_map_binding'}
exec(compile(source,__file__+'::exact-labels-no-inferred-event-link','exec'),env)
TERMS=env['TERMS']
if __name__=='__main__':env['main']()
