"""57 native body/font and456 macro cases; new live controls remain pending."""
from pathlib import Path
from dataclasses import replace
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/probe_lil_london_known_fonts_v1886.py')
SOURCE_SHA = '2ab7fa55b9a77520b759b66e2528623c4352889471d3a7f806db624bfc883cc4'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    context = read('work/analysis/lil_Speyer_context_v1918/original_Hamburg_predicate_and57_macro_contexts.json')
    assert len(context['records']) == 57
    assert context['manuscript_sha256'] == sha(Path(context['manuscript']).read_bytes())
    assert set(context['native_speaker_catalog']) == {'2','9','14','20','29','151','152'}
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        "ROOT=Path('work/analysis/lil_London_known_fonts_v1886')":"ROOT=Path('work/analysis/lil_Speyer_fonts_v1922')",
        "DOC=Path('translations/lil_london_editorial_manuscript_v2.json')":"DOC=Path('translations/lil_speyer_encounter_editorial_manuscript_v1.json')",
        "ROM=Path('out/all_routes_combined_v1875_candidate.nds')":"ROM=Path('out/all_routes_combined_v1909_candidate.nds')",
        "work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json":"work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json",
        "profile=get_dialogue_profile('lil-opening-editorial-native-v1');cases=[];failures=[];pictures=[]":
            "base_profile=get_dialogue_profile('lil-opening-editorial-native-v1');profile=replace(base_profile,name='Speyer-body-and-macro-research-only',leading_speaker_bytes=base_profile.leading_speaker_bytes|frozenset({29,151,152}));cases=[];failures=[];pictures=[]",
        "assert len(doc['records'])==68":"assert len(doc['records'])==57",
        "all68_native_macros_and_complete_font_planes.json":"all57_native_macros_and_complete_font_planes.json",
        "'London_new_presentation_types_and_revised_actual_display_still_pending'":"'Speyer_new_scene_controls_choice_menu_and_revised_actual_display_still_pending'",
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    # The expanded speaker set exists in this research isolate only. It is not
    # registered, written to a global profile or approved for a playable release.
    env = {'__name__':'__main__','__file__':__file__,'replace':replace}
    exec(compile(text,str(SOURCE),'exec'),env)
