"""Keep full prose when word distribution or an intact question tag needs pagination."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=ROOT/'planned_boundary_preferences_v2.json';output=ROOT/'planned_boundary_preferences_v3.json'
    assert not output.exists()
    doc=deepcopy(load(prior));rows=doc['records']
    a=rows['DK4_MES_B65_R0035'];a.pop('one_page')
    a.update(page_clause='Everyone in the village already has their hands full.',
        reason='A four-row fit would split wouldn\'t it across rows. Keep that short question tag intact, then begin the second page with the complete village-workload sentence. Preserve all prose and native geometry.')
    b=rows['DK4_MES_B70_R0193'];b.pop('one_page')
    b.update(page_clause="they get away so quickly that we often can't catch them.",
        reason='No complete-word four-row fit exists at the validated guard/phase widths. Start the second page with the full main clause instead of stranding catch them.')
    kept=rows.pop('DK4_MES_B75_R0238')
    doc.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        rejected_one_page_attempts_preserved=str(ROOT/'automatic_v3/automatic_plans.json'),
        exact_two_page_layout_retention={
            'id':'DK4_MES_B75_R0238','bindings':kept['bindings'],
            'lines':kept['previous_lines'],
            'reason':'No complete-word four-row fit exists at validated native guard/phase widths. The first page ends the tradition/dignity sentence; the second is the complete contempt sentence You are beneath my notice. Retain this coherent sentence boundary rather than shorten prose or widen bounds.'},
        no_text_geometry_orQA_guard_changes=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
    print('Retained necessary native pagination for three long/word-distribution cases;two one-page candidates and five coherent-clause refinements remain. No prose shortened.',flush=True)
