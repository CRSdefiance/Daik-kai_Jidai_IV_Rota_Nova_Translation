"""Clarify three distinct navigation frames and one same-frame final duplicate; retain the exact masks/tables."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/HELP_active_skill_labels_20261105')
if __name__=='__main__':
    old=ROOT/'active_terms_binding_v1.json';out=ROOT/'active_terms_binding_v2.json';assert not out.exists()
    prior=load(old);doc=deepcopy(prior);report=load(doc['actual_capture_report'])
    frames=[r for r in report['frames_captured']if r['frame']>=8200]
    assert len(frames)==4 and sorted({r['frame']for r in frames})==[8200,8400,8600]
    duplicate=[r for r in frames if r['frame']==8600];assert len(duplicate)==2 and duplicate[0]['PNG_sha256']==duplicate[1]['PNG_sha256']
    doc.pop('all_four_individual_navigation_frames_directly_viewed')
    doc.update(three_distinct_navigation_frames_directly_viewed=[8200,8400,8600],four_capture_files_include_exact_same_frame_final_duplicate=True,
        no_additional_coverage_from_duplicate_final_frame=True,previous_binding=str(old),previous_binding_sha256=sha(old.read_bytes()),
        scope_metadata_clarified_all_actual_masks_tables_andreferences_exact=True,scope_metadata_producer_sha256=sha(Path(__file__).read_bytes()))
    assert doc['active_label_tables']==prior['active_label_tables']and doc['actual_all10_complete_skill_masks']==prior['actual_all10_complete_skill_masks']
    save(out,doc);print('Active-term scope clarified:three distinct viewed navigation frames;exact final duplicate adds no coverage. All masks/tables unchanged.')
