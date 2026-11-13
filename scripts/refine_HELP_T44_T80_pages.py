"""Resolve the measured commander-sentence page split without changing any prose."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v5 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T44_T80_formatting_20261104')
if __name__=='__main__':
    out=ROOT/'refined_v2';assert not out.exists()
    input_path=ROOT/'formatting_input_v1.json';doc=load(input_path)
    row=next(r for r in doc['records'] if r['topic_id']==66);english=row['english'];at=english.index('Each new fleet needs')
    row['semantic_sections']=[english[:at].strip(),english[at:].strip()]
    row['semantic_section_reason']='Clean66 separates fleet delegation/policy from operating funds,maximum fleets andcommander return. Preserve those two logical paragraphs so the sinking/commander sentence doesnot straddle a page. The formatter owns all ordinary lines.'
    assert ' '.join(row['semantic_sections'])==english
    parent=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    file=doc['file_path'];clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    encoded,plan=plan_articles(doc,clean.read_file(file),base.read_file(file),parent.read_file(file),require_formatting=False)
    before=load(ROOT/'automatic_plans_v1.json');assert len(plan['pages'])==len(before['pages'])==38
    assert all(r['english']==old['english'] for r,old in zip(doc['records'],load(input_path)['records'],strict=True))
    assert all(p==q for p,q in zip(plan['pages'],before['pages'],strict=True) if p['source_article_id']!=66)
    out.mkdir();new_input=out/'formatting_input_v1.json';save(new_input,doc);resource=out/'HELP_shipyard37_RESEARCH_ONLY.DK4';resource.write_bytes(encoded)
    save(out/'automatic_plans_v1.json',dict(**plan,manuscript=str(new_input),manuscript_sha256=sha(new_input.read_bytes()),research_resource=str(resource),
      current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],previous_plan=str(ROOT/'automatic_plans_v1.json'),previous_plan_sha256=sha((ROOT/'automatic_plans_v1.json').read_bytes()),
      source66_definition_andoperating_rules_kept_together=True,threshold_at_least150_not_orphaned=True,no_prose_orother36_article_changes=True,
      registered_parent_still_pending=True,all_native_actual_visual_andfifth_gates_pending=True,new_credit=0))
    for page in plan['pages']:
        if page['source_article_id']==66: print(page['topic_id'],'/'.join(page['visible_lines']))
