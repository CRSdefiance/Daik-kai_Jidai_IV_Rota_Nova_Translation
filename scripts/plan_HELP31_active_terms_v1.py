"""Reformat five corrected Deck pages and one zero-credit Coerce amendment; reuse unchanged25 page bytes."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v11 import plan_articles
from scripts.plan_HELP_T103_T132_v1 import logical_links
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/HELP31_active_terms_20261105')
COMPARE=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104/whole_article_comparisons_v5.json')
OLD31=Path('translations/help_town23_contextual_final_review_v2.json')
OLD30=Path('translations/help_deck30_contextual_final_review_v1.json')
BIND=Path('work/analysis/HELP_active_skill_labels_20261105/active_terms_binding_v2.json')

if __name__=='__main__':
    assert not ROOT.exists()
    prior=load(OLD30);comp=load(COMPARE);binding=load(BIND)
    parent=Path(prior['current_ROM']);assert sha(parent.read_bytes())==prior['current_ROM_sha256']
    image=NdsImage.open(parent);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file='/COMMON/HELP.DK4';raw,source,canonical=[r.read_file(file)for r in [image,clean,base]]
    current,original,baseline=[IlnkContainer.parse(r).blocks for r in [raw,source,canonical]]
    assert len(current)==217 and binding['Help66_Command_confirmed_active']
    amended=deepcopy(next(r for r in load(OLD31)['records']if r['topic_id']==33))
    assert 'Persuasion' in amended['english']and '説得力２００以上' in amended['source_Japanese_with_link_IDs']
    amended.update(english=amended['english'].replace('Persuasion','Speech'),decision='revision',retention_reason=None,
        finding='Use the current active Speech skill label for 説得力. Preserve the First Mate requirement, at least200 threshold and that sea region\'s Proof of Conquest. This is a previously credited record amendment, never a new source completion.',
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0,
        previously_credited_amendment=True,active_term_binding=str(BIND),active_term_binding_sha256=sha(BIND.read_bytes()))
    amended['localization_note']=amended['finding'];amended['planned_stored_pages']=[]
    records=[amended]
    for r in comp['records']:
        row=deepcopy(r)
        if row['topic_id']not in [116,117,118,121,126]:
            old=next(p for p in prior['records']if p['topic_id']==row['topic_id']);row['review']['formatting']=True
            row['unchanged_display_evidence_from']=str(OLD30);row['unchanged_display_evidence_sha256']=sha(OLD30.read_bytes())
        row['previously_credited_amendment']=False;records.append(row)
    for row in records:
        n=row['topic_id'];assert original[n].hex()==row['source_hex']
        row.update(heading=row.get('heading',row.get('title')),english=logical_links(row['english']),
            clean_source_hex=original[n].hex(),canonical_source_hex=baseline[n].hex(),current_source_hex=current[n].hex(),
            current_hex=current[n].hex(),current_reference=dict(file_path=file,block=n,archive_offset=int.from_bytes(raw[8+4*n:12+4*n],'little'),bytes=len(current[n]),offset_table_slot=8+4*n))
    doc=dict(format='dk4-deck30-Coerce33-active-terms-input-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path=file,
        current_ROM=str(parent),current_ROM_sha256=sha(parent.read_bytes()),source_clean_HELP_sha256=sha(source),source_canonical_HELP_sha256=sha(canonical),source_current_HELP_sha256=sha(raw),
        current_topic_count=217,source_topic_count=202,records=records,records_count=31,proposed_revisions=11,justified_retentions=20,
        new_source_records=30,new_source_revisions=10,new_source_retentions=20,previously_credited_amendments=[33],
        all_four_prose_gates_pass=True,pending_fresh_formatting_topic_IDs=[33,116,117,118,121,126],new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes())for p in [COMPARE,OLD31,OLD30,BIND,Path('dk4tool/dialogue/reviewed_help_pages_v11.py'),Path(__file__)]})
    resource,plan=plan_articles(doc,source,canonical,raw,require_formatting=False)
    old_plan=load('work/analysis/Shared_HELP_T103_T132_formatting_20261104/production_plan_v1.json')
    old_by_topic={p['topic_id']:p for p in old_plan['pages']}
    changed=[p['topic_id']for p in plan['pages']if p['topic_id']not in old_by_topic or p!=old_by_topic[p['topic_id']]]
    assert changed==[33,116,117,118,121,126]and len(plan['pages'])==31 and plan['target_topic_count']==217
    assert not plan['compiler_generated_navigation_pairs']
    ROOT.mkdir();input_path=ROOT/'formatting_input_v1.json';save(input_path,doc);target=ROOT/'HELP31_active_terms_RESEARCH_ONLY.DK4';target.write_bytes(resource)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(input_path),manuscript_sha256=sha(input_path.read_bytes()),research_resource=str(target),
        current_ROM=str(parent),current_ROM_sha256=sha(parent.read_bytes()),fresh_page_IDs=changed,exact_reused_page_IDs=sorted(set(range(103,133))-set(changed)),
        fresh_native_andvisual_for_six_pages_pending=True,twentyfive_unchanged_native_actual_pages_reusable_with_exact_dependency_binding=True,
        new_credit=0,registered_integration_pending=True))
    print('31-page plan:6 fresh pages/25 exact-byte reused;10 new revisions/20 retentions pluszero-credit Coerce amendment.')
    for p in plan['pages']:
        if p['topic_id']in changed:print(p['topic_id'],'/'.join(p['visible_lines']))
