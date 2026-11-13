"""Prepare fresh source-bound automatic pages onthe exact pending Help212 parent;no release claim."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v2 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
COMPARISON=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104/whole_article_comparisons_v4.json')
PREP=Path('work/analysis/Early_HELP23_release_20261104/registered_preparation.json')
HEADINGS={21:'Market',22:'Trade (Market)',23:'Commercial Investment',24:'Market Info',25:'Trends (Market Info)',
    26:'Guild (Cities only)',27:'Send Letter (Guild)',28:'Goodwill (Send Letter)',29:'Alliance (Send Letter)',
    30:'Break Pact (Send Letter)',31:'Truce (Send Letter)',32:'Declare War (Send Letter)',33:'Coerce (Send Letter)',
    34:'Inn',35:"Palace / Governor's Office",36:'Contract (Palace)',37:"Military Investment (Palace / Governor's Office)",
    38:'Use Letter of Introduction (Palace)',39:'Use Letter of Recommendation (Palace)',40:'Lend Item (Palace)',
    41:'Retrieve Item (Palace)',42:'Square',43:'Distribute Goods (Square)'}

if __name__=='__main__':
    assert not ROOT.exists();comparison=load(COMPARISON);prep=load(PREP)
    parent=Path(prep['final_ROM']);assert sha(parent.read_bytes())==prep['target_ROM_sha256']
    image=NdsImage.open(parent);clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file='/COMMON/HELP.DK4';raw=image.read_file(file);blocks=IlnkContainer.parse(raw).blocks
    source=clean.read_file(file);base=canonical.read_file(file);source_blocks=IlnkContainer.parse(source).blocks;base_blocks=IlnkContainer.parse(base).blocks
    assert len(blocks)==212 and len(source_blocks)==len(base_blocks)==202
    records=[]
    for old in comparison['records']:
        row=deepcopy(old);t=row['topic_id'];original_current=row['current_reference']
        assert blocks[t]==bytes.fromhex(row['current_hex']) and source_blocks[t]==bytes.fromhex(row['source_hex'])
        offset=int.from_bytes(raw[8+4*t:12+4*t],'little');assert raw[offset:offset+len(blocks[t])]==blocks[t]
        row.update(heading=HEADINGS[t],speaker='Help narrator',localization_note=row['finding'],
            clean_source_hex=source_blocks[t].hex(),canonical_source_hex=base_blocks[t].hex(),current_source_hex=blocks[t].hex(),
            comparison_current_reference=original_current,current_reference=dict(file_path=file,block=t,archive_offset=offset,bytes=len(blocks[t]),offset_table_slot=8+4*t),
            formatting_parent_reference_is_planned_not_yet_verified_cumulative=True)
        if t==37:
            row['current_continuations']=deepcopy(row['complete_current_continuations'][1:])
            for continuation in row['current_continuations']:
                n=continuation['topic_id'];assert blocks[n]==bytes.fromhex(continuation['current_hex'])
                a=int.from_bytes(raw[8+4*n:12+4*n],'little')
                continuation['comparison_current_reference']=continuation['current_reference']
                continuation['current_reference']=dict(file_path=file,block=n,archive_offset=a,bytes=len(blocks[n]),offset_table_slot=8+4*n)
            english=row['english'];at=english.index("Investment raises the city's Arms rating.")
            row['semantic_sections']=[english[:at].strip(),english[at:].strip()]
            row['semantic_section_reason']='The clean military-investment article has a cost paragraph andan outcome paragraph. Keep them logical semantic paragraphs,withordinary lines entirely compiler-wrapped;reuse onlyneeded existing204/205 continuation slots andpreserve unused older data.'
            assert ' '.join(row['semantic_sections'])==english
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        records.append(row)
    manuscript=dict(format='dk4-town-help23-formatting-input-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path=file,
        source_clean_HELP_sha256=sha(source),source_canonical_HELP_sha256=sha(base),source_current_HELP_sha256=sha(raw),
        current_ROM=str(parent),current_ROM_sha256=prep['target_ROM_sha256'],current_topic_count=212,source_topic_count=202,
        comparison_ROM=comparison['current_ROM'],comparison_ROM_sha256=comparison['current_ROM_sha256'],records=records,
        proposed_revisions=19,justified_retentions=4,all_four_prose_gates_pass=True,all_fifth_gates_pending=True,
        current_all_selected_article_andcontinuation_bytes_exact_to_original_comparison=True,
        planned_parent_registered_build_still_pending=True,new_credit=0,full_goal_complete=False,
        heading_policy='Keep existing readable command headings andnative short service names;use nativeMarket Info andclarify Introduction/Recommendation. Palace is the existing short shared-service heading;full palace/governor alternatives remain inroot35 andexplicit scoped prose. Body retentions aretracked separately fromtitle capitalization/context.',
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,PREP,Path('dk4tool/dialogue/reviewed_help_pages_v2.py'),Path(__file__)]})
    encoded,plan=plan_articles(manuscript,source,base,raw,require_formatting=False)
    ROOT.mkdir();input_path=ROOT/'formatting_input_v1.json';save(input_path,manuscript)
    resource=ROOT/'HELP_town23_RESEARCH_ONLY.DK4';resource.write_bytes(encoded)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(input_path),manuscript_sha256=sha(input_path.read_bytes()),
        research_resource=str(resource),current_ROM=str(parent),current_ROM_sha256=prep['target_ROM_sha256'],
        source_comparison=str(COMPARISON),source_comparison_sha256=sha(COMPARISON.read_bytes()),
        no_authored_wraps_noshortened_prose_noruntime_changes=True,registered_parent_still_pending=True,
        all_native_actual_visual_andfifth_gates_pending=True,new_credit=0))
    print(dict(articles=len(records),pages=len(plan['pages']),parent_topics=212,target_topics=plan['target_topic_count'],
        navigation_pairs=plan['compiler_generated_navigation_pairs'],all_unowned_bytes_andlogical_prose_exact=True,all_fifth_gates_pending=True))
