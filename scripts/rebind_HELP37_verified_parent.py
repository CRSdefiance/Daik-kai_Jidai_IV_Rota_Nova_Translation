"""Rebind ready37 research to its byte-identical verified Town parent;retain all reviewed page bytes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_help_pages_v5 import plan_articles
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    old=Path('translations/help_shipyard37_contextual_final_review_v1.json');new=old.with_name('help_shipyard37_contextual_final_review_v2.json')
    root=Path('work/analysis/Shared_HELP_T44_T80_formatting_20261104');plan_path=root/'production_plan_v2.json';proof_path=root/'registered_parent_metadata_rebinding_v1.json'
    assert not new.exists() and not plan_path.exists() and not proof_path.exists()
    release_path=Path('work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json');release=load(release_path)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert load(release_path.parent/'completion_checkpoint.json')['new_credit']==23
    doc=load(old);parent=Path(release['candidate']);research=Path(doc['current_ROM'])
    assert parent.read_bytes()==research.read_bytes() and sha(parent.read_bytes())==doc['current_ROM_sha256']==release['candidate_sha256']
    previous=load(root/'production_plan_v1.json');doc.update(current_ROM=str(parent),registered_parent_still_pending=False,
      planned_parent_registered_build_still_pending=False,reviewed_parent_research_ROM=str(research),
      registered_parent_release=str(release_path),registered_parent_release_sha256=sha(release_path.read_bytes()),
      previous_final_review=str(old),previous_final_review_sha256=sha(old.read_bytes()),parent_rebinding_is_metadata_only_no_new_editorial_credit=True)
    for row in doc['records']:row['formatting_parent_reference_is_planned_not_yet_verified_cumulative']=False
    controls=Path('work/analysis/Shared_HELP_T44_T80_clean_20261104/HELP51_native_controls_v1.json')
    terms=controls.with_name('native_UI_terms_andfour_limits_v1.json')
    for p in [release_path,controls,terms,Path(__file__)]:doc['evidence'][str(p)]=sha(p.read_bytes())
    image=NdsImage.open(parent);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    encoded,production=plan_articles(doc,clean.read_file(file),base.read_file(file),image.read_file(file))
    assert encoded==Path(previous['research_resource']).read_bytes() and production['pages']==previous['pages']
    save(new,doc);save(plan_path,dict(**production,manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),research_resource=previous['research_resource'],
      all_native_visual_andactual_bytes_unchanged=True,registered_parent_andintegration_pending=False,registered_integration_pending=True,new_credit=0))
    save(proof_path,dict(previous_final=str(old),previous_final_sha256=sha(old.read_bytes()),new_final=str(new),new_final_sha256=sha(new.read_bytes()),
      verified_parent=str(parent),verified_parent_sha256=release['candidate_sha256'],all38_page_bytes_andcompleted_proofs_unchanged=True,new_credit=0))
    print('Ready37 metadata bound toverified Town parent;all38 page bytes/checks unchanged,no new credit.')
