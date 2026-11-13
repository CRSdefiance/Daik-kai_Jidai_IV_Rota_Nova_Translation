"""Bind selected Help prose to the verified cumulative parent after clean drafts are sealed."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
if __name__=='__main__':
    draft_path=ROOT/'T00_T20_clean_meanings_andindependent_drafts_v1.json'
    draft=load(draft_path);output=ROOT/'current_T00_T20_verified_parent_v1.json';assert not output.exists()
    assert len(draft['records'])==21 and draft['independent_drafts_precede_first_selected_current_English_extraction']
    release_path=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
    release=load(release_path);rom=Path(release['candidate']);assert sha(rom.read_bytes())==release['candidate_sha256']
    image=NdsImage.open(rom);file=draft['file_path'];archive=image.read_file(file);blocks=IlnkContainer.parse(archive).blocks
    assert len(blocks)==211 and IlnkContainer(blocks).to_bytes()==archive
    assert sha(archive)=='015ee6aaab9544555a2bcd90f74dbd10450ca20e441954cf5b99f8196e275cc0'
    latest=load('work/analysis/Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json')
    successor=NdsImage.open(latest['research_ROM'])
    dependencies=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT',file]
    assert sha(Path(latest['research_ROM']).read_bytes())==latest['research_ROM_sha256']
    assert all(successor.read_file(path)==image.read_file(path) for path in dependencies)
    rows=[]
    for original in draft['records']:
        index=original['topic_id'];raw=blocks[index]
        start=int.from_bytes(archive[8+4*index:12+4*index],'little')
        assert archive[start:start+len(raw)]==raw
        rows.append(dict(id=original['id'],topic_id=index,source_reference=original['source_reference'],
            source_hex=original['source_hex'],current_reference=dict(file_path=file,block=index,
                archive_offset=start,bytes=len(raw),offset_table_slot=8+4*index),
            current_hex=raw.hex(),current_sha256=sha(raw),current_English_with_link_IDs=readable_source(raw),
            current_links=source_links(raw),current_link_IDs=[link['topic_id'] for link in source_links(raw)]))
    labels=[]
    for index in [21,26,34,35,37,42,44,73,80,82,103,118,139,143,144,145,148,150,184]:
        raw=blocks[index];heading=readable_source(raw).split('\n',1)[0]
        labels.append(dict(topic_id=index,current_heading=heading,current_block_sha256=sha(raw),
            only_UI_heading_consulted_not_the_unselected_body=True))
    save(output,dict(file_path=file,current_ROM=str(rom),current_ROM_sha256=release['candidate_sha256'],
        current_archive_sha256=sha(archive),current_topic_count=211,original_clean_topic_count=202,
        records=rows,UI_heading_bindings=labels,
        clean_independent_drafts=str(draft_path),clean_independent_drafts_sha256=sha(draft_path.read_bytes()),
        verified_parent_release=str(release_path),verified_parent_release_sha256=sha(release_path.read_bytes()),
        same_HELP_ARM9_COMMON_andfont_in_pending_successor=True,
        pending_successor_research_ROM=latest['research_ROM'],pending_successor_sha256=latest['research_ROM_sha256'],
        unselected_andnine_added_current_topics_must_be_preserved=True,
        actual_gameplay=False,no_new_completion_credit=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound21 current Help articles aftersealed clean drafts;211 current/202 clean topics,nine addedcurrent topics preserved. No gameplay orcompletion claim.')
