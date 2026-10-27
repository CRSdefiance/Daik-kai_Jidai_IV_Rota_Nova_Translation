"""All76 progressive Hamburg planes and608 guarded native macro calls."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/probe_lil_london_known_fonts_v1886.py')
SOURCE_SHA = '2ab7fa55b9a77520b759b66e2528623c4352889471d3a7f806db624bfc883cc4'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'from dk4tool.dialogue.lil_stockholm_profile import profile_for':'from dk4tool.dialogue.lil_hamburg_profile import profile_for',
        "ROOT=Path('work/analysis/lil_London_known_fonts_v1886')":"ROOT=Path('work/analysis/lil_Hamburg_fonts_v1954')",
        "DOC=Path('translations/lil_london_editorial_manuscript_v2.json')":"DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')",
        "ROM=Path('out/all_routes_combined_v1875_candidate.nds')":"ROM=Path('out/all_routes_combined_v1945_candidate.nds')",
        "    inventory=read('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')":
            "    packet=read('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json');inventory={'snapshot':packet['source_snapshot'],'snapshot_sha256':packet['source_snapshot_sha256']}",
        "profile=get_dialogue_profile('lil-opening-editorial-native-v1');cases=[];failures=[];pictures=[]":
            "profile=profile_for(arm,IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[74]);cases=[];failures=[];pictures=[]",
        "assert len(doc['records'])==68":"assert len(doc['records'])==76",
        'all68_native_macros_and_complete_font_planes.json':'all76_native_macros_and_complete_font_planes.json',
        "'London_new_presentation_types_and_revised_actual_display_still_pending'":"'Hamburg_FE_choice_relocation_and_revised_actual_display_still_pending'",
    }
    for old, new in changes.items():
        assert text.count(old) == 1, old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
