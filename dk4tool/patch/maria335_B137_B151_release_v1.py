"""Pure335-record transaction retaining all registered source/current/inverse guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('dk4tool/patch/maria337_release_v1.py').read_text(encoding='utf-8'),{
    'list(range(125,137))':'list(range(137,152))',
    'Maria337 release: ':'Maria335 B137-B151 release: ',
    '==(337,335,335,0,2,339,430,6)':'==(335,333,333,0,2,333,100,18)',
    '12 complete source exchanges':'15 complete source exchanges',
    '==(337,224,113)':'==(335,185,150)',
    "visual['body_pages']==339 and visual['all339_final_pages_directly_viewed']":
        "visual['body_pages']==333 and visual['all333_final_pages_directly_viewed']",
    "native['selected_alignment_cases']==1340":"native['selected_alignment_cases']==1332",
    '==(176,163,430)':'==(172,161,100)',
    "lookup['all335_physical_bodies_checked']":"lookup['all333_physical_bodies_checked']",
    "len(stored['records'])==335":"len(stored['records'])==333",
    "for r in stored['records'])==6,'six original FE panels'":"for r in stored['records'])==18,'18 original FE panels'",
    '==(6,18,4)':'==(6,18,6)',
    "==['産es','札ecline']":"==['丑o']",
    "menu['menus']==load(rebuilt['menu'])['menus']":
        "original_menu['current_valid_ASCII_option_normal_highlight_planes']==2 and menu['menus']==load(rebuilt['menu'])['menus']",
    '==(33202,2,48,52,287,2,1)':'==(31522,2,44,44,289,2,1)',
    'all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed':'all44_selected_pages_two_captions_andboth_host_transitions_directly_viewed',
    'all_four_two_page_tutorial_A_andfollowing_returns_observed':'all_three_reclaimed_one_page_paragraph_A_andfollowing_returns_observed',
    'all_six_FE_panels_andnamed_returns_observed':'all_eleven_FE_panels_andreturns_observed',
    'both_mixed_font_Latin_I_repairs_observed':'Julio_mixed_font_I_andIndeed_repairs_observed',
    '==(337,335,335,335,1)':'==(335,333,333,333,1)',
    "names['all21_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==21":
        "names['all26_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==26",
    "'dk4-reviewed-maria337-release-v1'":"'dk4-reviewed-maria335-b137-b151-release-v1'",
    "env={**previous.env,'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}":
        "from scripts.rebuild_maria335_B137_B151_reviewed_v2 import rebuild_block\n"
        "env={**previous.env,'rebuild_block':rebuild_block,'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}",
    "    validate_natural_dialogue_batch(names)":
        "    alignment=load(conf['inherited_alignment_qualification'])\n"
        "    require(alignment['all_five_negative_controls_rejected'] and alignment['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()),'exact inherited alignment qualification')\n"
        "    require(actual['all_six_scoped_FE_guard_repairs_observed'],'all scoped FE guards observed')\n"
        "    validate_natural_dialogue_batch(names)",
})
exec(compile(source,__file__+'::same-pure-complete-transaction-one-qualified-inherited-alignment','exec'),globals())
