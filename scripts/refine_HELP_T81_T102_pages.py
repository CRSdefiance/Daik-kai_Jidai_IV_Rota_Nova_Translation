"""Resolve observed marker/single-word tails andcontrol clauses without shortening prose oradding pages."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v7 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104')
if __name__=='__main__':
    out=ROOT/'refined_v2';assert not out.exists()
    before=load(ROOT/'automatic_plans_v1.json');doc=load(before['manuscript']);image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    encoded,plan=plan_articles(doc,clean.read_file(file),base.read_file(file),image.read_file(file),require_formatting=False)
    assert len(plan['pages'])==22 and plan['target_topic_count']==217 and not plan['compiler_generated_navigation_pairs']
    changed=[p['source_article_id']for p,q in zip(plan['pages'],before['pages'],strict=True)if p!=q]
    assert changed==[86,87,90,94,95,96,98,101],changed
    for p in plan['pages']:
        assert not any(line.endswith('[Tip]') for line in p['visible_lines'])
        if p['source_article_id']==94:assert p['visible_lines'][1:]==['Defeat the monster.','You may receive an item.']
        if p['source_article_id']==98:assert p['visible_lines'][-1]=='Deck positions.'
    out.mkdir();input_path=out/'formatting_input_v1.json';save(input_path,doc);resource=out/'HELP_sea22_RESEARCH_ONLY.DK4';resource.write_bytes(encoded)
    save(out/'automatic_plans_v1.json',dict(**plan,manuscript=str(input_path),manuscript_sha256=sha(input_path.read_bytes()),research_resource=str(resource),
      current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],previous_plan=str(ROOT/'automatic_plans_v1.json'),previous_plan_sha256=sha((ROOT/'automatic_plans_v1.json').read_bytes()),
      refined_article_IDs=changed,no_prose_changes_oradded_pages=True,all22_source_link_sequences_andcomplete_prose_exact=True,
      registered_parent_still_pending=True,all_native_actual_visual_andfifth_gates_pending=True,new_credit=0))
    for p in plan['pages']:
        if p['source_article_id']in changed:print(p['source_article_id'],'/'.join(p['visible_lines']))
