"""Compose the30 reviewed Deck articles on the planned registered two-layer Help successor."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v8 import plan_articles
from scripts.prepare_help_pages_v281 import words
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104')
COMPARISON=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104/whole_article_comparisons_v3.json')
PARENT=Path('work/analysis/HELP66_Command_amendment_20261104/after_sea22_v2/metadata_rebinding_receipt_v2.json')

def plain(text):
    return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]',r'\1',text).split())

def logical_links(text):
    tokens=words(text)
    return ' '.join(t if isinstance(t,str)else'[['+str(t['id'])+'|'+t['label'].strip()+']]'for t in tokens)

if __name__=='__main__':
    assert not ROOT.exists()
    comparison,parent=map(load,[COMPARISON,PARENT]);rom=Path(parent['research_ROM'])
    assert sha(rom.read_bytes())==parent['research_ROM_sha256']
    image=NdsImage.open(rom);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file='/COMMON/HELP.DK4';raw,source,canonical=[i.read_file(file)for i in [image,clean,base]]
    blocks,original,baseline=[IlnkContainer.parse(r).blocks for r in [raw,source,canonical]]
    assert len(blocks)==217 and len(original)==len(baseline)==202
    rows=[];normalizations=[]
    for prior in comparison['records']:
        row=deepcopy(prior);n=row['topic_id']
        assert blocks[n].hex()==row['current_hex'] and original[n].hex()==row['source_hex']
        assert all(row['review'][g]for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        english=logical_links(row['english'])
        assert plain(english)==plain(row['english'])
        if english!=row['english']:normalizations.append(n)
        row.update(english=english,clean_source_hex=original[n].hex(),canonical_source_hex=baseline[n].hex(),current_source_hex=blocks[n].hex(),
            comparison_current_reference=row['current_reference'],current_reference=dict(file_path=file,block=n,
                archive_offset=int.from_bytes(raw[8+4*n:12+4*n],'little'),bytes=len(blocks[n]),offset_table_slot=8+4*n),
            old_link_phase_padding_removed_only_from_editable_markup=True,formatting_parent_registered_build_still_pending=True)
        rows.append(row)
    doc=dict(format='dk4-deck-help30-formatting-input-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path=file,
        source_clean_HELP_sha256=sha(source),source_canonical_HELP_sha256=sha(canonical),source_current_HELP_sha256=sha(raw),
        current_ROM=str(rom),current_ROM_sha256=sha(rom.read_bytes()),source_topic_count=202,current_topic_count=217,
        records=rows,proposed_revisions=12,justified_retentions=18,all_four_prose_gates_pass=True,all_fifth_gates_pending=True,
        comparison_ROM=comparison['current_ROM'],comparison_ROM_sha256=comparison['current_ROM_sha256'],
        normalized_legacy_link_padding_article_IDs=normalizations,all_complete_logical_words_punctuation_andlink_destinations_preserved=True,
        all18_retained_bodies_word_exact=True,planned_parent_registered_build_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes())for p in [COMPARISON,PARENT,Path('dk4tool/dialogue/reviewed_help_pages_v8.py'),Path(__file__)]})
    resource,plan=plan_articles(doc,source,canonical,raw,require_formatting=False)
    ROOT.mkdir();manuscript=ROOT/'formatting_input_v1.json';save(manuscript,doc)
    output=ROOT/'HELP_deck30_RESEARCH_ONLY.DK4';output.write_bytes(resource)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        research_resource=str(output),current_ROM=str(rom),current_ROM_sha256=sha(rom.read_bytes()),
        all_native_actual_visual_andfifth_gates_pending=True,no_authored_wraps_noshortened_prose_noruntime_changes=True,
        registered_parent_still_pending=True,new_credit=0))
    print(dict(articles=30,pages=len(plan['pages']),target_topics=plan['target_topic_count'],navigation_pairs=plan['compiler_generated_navigation_pairs']))
    for p in plan['pages']:print(p['topic_id'],'/'.join(p['visible_lines']))
