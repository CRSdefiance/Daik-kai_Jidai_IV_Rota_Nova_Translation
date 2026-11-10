"""Bind exact stat-family headings/bodies without confusing the unrelated verb influenced."""
import re
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
if __name__=='__main__':
    output=ROOT/'Power_family_complete_current_bindings_v1.json';assert not output.exists()
    draft_path=ROOT/'T181_T184_clean_meanings_independent_drafts_v1.json';draft=load(draft_path)
    current_path=ROOT/'current_T00_T20_verified_parent_v1.json';current=load(current_path)
    image=NdsImage.open(current['current_ROM']);archive=image.read_file(current['file_path']);blocks=IlnkContainer.parse(archive).blocks
    assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256'] and sha(archive)==current['current_archive_sha256']
    standalone=[i for i,raw in enumerate(blocks) if re.search(r'\bInfluence\b',readable_source(raw),re.I)]
    assert standalone==[181,184,202]
    rows=[]
    for source in draft['records']:
        index=source['topic_id'];raw=blocks[index];offset=int.from_bytes(archive[8+index*4:12+index*4],'little')
        assert archive[offset:offset+len(raw)]==raw
        rows.append(dict(id=source['id'],topic_id=index,source_reference=source['source_reference'],source_hex=source['source_hex'],
            current_reference=dict(file_path=current['file_path'],block=index,archive_offset=offset,bytes=len(raw)),
            current_hex=raw.hex(),current_text=readable_source(raw),current_links=source_links(raw)))
    headings=[dict(topic_id=i,heading=readable_source(blocks[i]).splitlines()[0].strip(),block_sha256=sha(blocks[i])) for i in [150,182,184,185,190]]
    term_path=ROOT/'native_UI_terms_andRafael_continuation_v1.json';term=load(term_path)
    notice=[r for r in term['source_current_UI_labels'] if r['message_id']==288]
    assert len(notice)==1 and notice[0]['Japanese_term']=='勢力値' and notice[0]['current_text'].startswith('Power +%s!')
    save(output,dict(current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_HELP_sha256=sha(archive),records=rows,heading_bindings=headings,
        same_source_metric_native_notice=notice[0],standalone_Influence_topic_IDs=standalone,
        all211_topics_scanned_for_word_not_substring=True,
        unrelated_influenced_by_skill_stat_prose_171_to179_and208_not_targeted=True,
        clean_body_drafts=str(draft_path),clean_body_drafts_sha256=sha(draft_path.read_bytes()),
        existing_Rafael202_continuation_is_part_of_article7_not_new_source_credit=True,
        no_ROM_changes_ornew_renderer_execution=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [draft_path,current_path,term_path,Path(__file__)]}))
    print('Standalone stat Influence isconfined to181/184/202;native notice288 saysPower. Complete currentlinked articles:')
    for row in rows:print(row['topic_id'],row['current_text'])
    print('Existing link headings',[(r['topic_id'],r['heading']) for r in headings])
