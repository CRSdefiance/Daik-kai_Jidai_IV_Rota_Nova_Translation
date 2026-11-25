"""Focused cold-boot replay: revised Lookout line and original Bruges return."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/run_lil_crew_final_text_v1764.py')

if __name__ == '__main__':
    assert read('work/analysis/lil_Lookout_loader_v1981/whole_SC2_and_B23_initial_entry_proof.json')['all336_whole_blocks_and672_modes_each_pass']
    assert read('work/analysis/lil_crew_final_text_v1764/terminal.json')['frame'] == 41420
    assert read('work/analysis/lil_Lookout_relocation_v1980/current_B23_typed_relocation_research.json')['all12_relative_sites_120_cases_preserve_targets']
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'from scripts.prepare_lil_lessons_research_v1761 import ROM':'from scripts.research_lil_lookout_revision_v1980 import ROM',
        "ROOT = Path('work/analysis/lil_crew_final_text_v1764')":"ROOT = Path('work/analysis/lil_Lookout_revised_run_v1982')",
        "CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_crew_final_text_v1764_RESEARCH_ONLY')":
            "CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_revised_run_v1982_RESEARCH_ONLY')",
        'work/analysis/lil_lessons_research_v1761/research_image_receipt.json':'work/analysis/lil_Lookout_relocation_v1980/research_image_receipt.json',
        "source_journal=Path('work/analysis/lil_crew_lesson_v1756/navigation.jsonl')":
            "source_journal=Path('work/analysis/lil_crew_final_text_v1764/navigation.jsonl')",
        'final_Deck_View_wording_replaces_only_last_paragraph_in_research_ROM':
            'only_Lookout_affiliation_wording_changes_in_research_ROM',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    # The complete frozen journal already includes stop at41420. No speculative
    # inputs or conditional branch/event overrides are added to this replay.
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
