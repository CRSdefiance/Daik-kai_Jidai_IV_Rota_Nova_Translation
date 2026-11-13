"""Preserve a genuine name-consumer distinction instead of forcing catalog/display equality."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/prove_lil_B179_names_v4713.py','scripts/prove_lil_B179_names_v4713b.py',{
    'lil_B179_names_v4713':'lil_B179_names_v4713b',
    "progressive={i:values[i,'progressive-nameplate'] for i in full};assert progressive==full":
        "progressive={i:values[i,'progressive-nameplate'] for i in full};assert progressive=={92:'Barkeep',96:'Patron',152:'Sailor'}",
    "approved_prose_names={str(k):v for k,v in expected.items()}":
        "approved_prose_names={str(k):v for k,v in progressive.items()}",
    'source_5C_60_98_are_static_Barkeep92_Patron96_Retainer152_not_literal_halfwidth_prose':
        'source_5C_60_98_are_static_Barkeep92_Patron96_Sailor152_in_progressive_dialogue_not_literal_halfwidth_prose',
    'Retainer_label_adds_no_named_lord_faction_rank_or_personal_relationship=True':
        "catalogue_Retainer152_and_progressive_Sailor152_are_distinct_source_consumers=True,\n        catalogue_label_does_not_override_progressive_identity_or_add_named_lord_faction_rank_or_personal_relationship=True,\n        preserved_failed_catalogue_equals_progressive_assumption='scripts/prove_lil_B179_names_v4713.py'",
})
print('Prepared distinct full-catalogue Retainer152/progressive Sailor152 bindings;failed equality assumption preserved.')
