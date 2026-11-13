"""Focused one changed ordinary progressive paragraph: native plane and8 calls."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/probe_lil_london_known_fonts_v1886.py')
SOURCE_SHA = '2ab7fa55b9a77520b759b66e2528623c4352889471d3a7f806db624bfc883cc4'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        "ROOT=Path('work/analysis/lil_London_known_fonts_v1886')":"ROOT=Path('work/analysis/lil_Lookout_affiliation_fonts_v1978')",
        "DOC=Path('translations/lil_london_editorial_manuscript_v2.json')":"DOC=Path('translations/lil_lessons_editorial_manuscript_v6.json')",
        "ROM=Path('out/all_routes_combined_v1875_candidate.nds')":"ROM=Path('out/all_routes_combined_v1971_candidate.nds')",
        "    inventory=read('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')":
            """    report=read('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY/capture_report.json')
    snapshot=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==76170)
    assert report['ROM_sha256']==doc['current_ROM_sha256']
    inventory={'snapshot':snapshot['path'],'snapshot_sha256':snapshot['sha256']}""",
        "doc['records']=[r for r in doc['records'] if int(r['source_presentation_prefix_hex'],16) in profile.leading_speaker_bytes]":
            "doc['records']=[r for r in doc['records'] if r['id']=='DK4_MES_B23_R0142']",
        "assert len(doc['records'])==68":"assert len(doc['records'])==1",
        'all68_native_macros_and_complete_font_planes.json':'one_changed_native_macros_and_complete_font_plane.json',
        "'London_new_presentation_types_and_revised_actual_display_still_pending'":
            "'lesson_reference_revised_actual_and_registered_integration_still_pending'",
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
