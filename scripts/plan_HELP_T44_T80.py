"""Fresh automatic formatting of37 reviewed articles;planned registered parent is explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v4 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T44_T80_formatting_20261104')
COMPARISON=Path('work/analysis/Shared_HELP_T44_T80_clean_20261104/whole_article_comparisons_v2.json')
PREP=Path('work/analysis/Town_HELP23_release_20261104/registered_preparation.json')
if __name__=='__main__':
    assert not ROOT.exists();comparison=load(COMPARISON);prep=load(PREP)
    parent=Path(prep['final_ROM']);assert sha(parent.read_bytes())==prep['target_ROM_sha256']
    image=NdsImage.open(parent);clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file='/COMMON/HELP.DK4';raw=image.read_file(file);source=clean.read_file(file);base=canonical.read_file(file)
    blocks,original,baseline=[IlnkContainer.parse(v).blocks for v in [raw,source,base]]
    assert len(blocks)==216 and len(original)==len(baseline)==202
    records=[]
    for old in comparison['records']:
        row=deepcopy(old);t=row['topic_id'];assert blocks[t]==bytes.fromhex(row['current_hex']) and original[t]==bytes.fromhex(row['source_hex'])
        offset=int.from_bytes(raw[8+4*t:12+4*t],'little');assert raw[offset:offset+len(blocks[t])]==blocks[t]
        row.update(heading=row['title'],clean_source_hex=original[t].hex(),canonical_source_hex=baseline[t].hex(),current_source_hex=blocks[t].hex(),
          comparison_current_reference=row['current_reference'],current_reference=dict(file_path=file,block=t,archive_offset=offset,bytes=len(blocks[t]),offset_table_slot=8+4*t),
          formatting_parent_reference_is_planned_not_yet_verified_cumulative=True)
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        records.append(row)
    doc=dict(format='dk4-shipyard-help37-formatting-input-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path=file,
      source_clean_HELP_sha256=sha(source),source_canonical_HELP_sha256=sha(base),source_current_HELP_sha256=sha(raw),
      current_ROM=str(parent),current_ROM_sha256=prep['target_ROM_sha256'],current_topic_count=216,source_topic_count=202,
      comparison_ROM=comparison['current_ROM'],comparison_ROM_sha256=comparison['current_ROM_sha256'],records=records,
      proposed_revisions=27,justified_retentions=10,all_four_prose_gates_pass=True,all_fifth_gates_pending=True,
      current_all_selected_article_bytes_exact_to_original_comparison=True,planned_parent_registered_build_still_pending=True,
      heading_policy='Use bound native command/role/room choices and concise parent context. Ten body retentions are word exact; titles,restored links and compiler line geometry are reviewed separately.',
      evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,PREP,Path('dk4tool/dialogue/reviewed_help_pages_v4.py'),Path(__file__)]},
      new_credit=0,full_goal_complete=False)
    encoded,plan=plan_articles(doc,source,base,raw,require_formatting=False)
    ROOT.mkdir();input_path=ROOT/'formatting_input_v1.json';save(input_path,doc)
    resource=ROOT/'HELP_shipyard37_RESEARCH_ONLY.DK4';resource.write_bytes(encoded)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(input_path),manuscript_sha256=sha(input_path.read_bytes()),
      research_resource=str(resource),current_ROM=str(parent),current_ROM_sha256=prep['target_ROM_sha256'],
      source_comparison=str(COMPARISON),source_comparison_sha256=sha(COMPARISON.read_bytes()),
      no_authored_wraps_noshortened_prose_noruntime_changes=True,registered_parent_still_pending=True,
      all_native_actual_visual_andfifth_gates_pending=True,new_credit=0))
    print(dict(articles=len(records),pages=len(plan['pages']),parent_topics=216,target_topics=plan['target_topic_count'],
      navigation_pairs=plan['compiler_generated_navigation_pairs'],all_unowned_bytes_andlogical_prose_exact=True,all_fifth_gates_pending=True))
    for page in plan['pages']:
        print('PAGE',page['topic_id'],'ARTICLE',page['source_article_id'],'/'.join(page['visible_lines']))
