"""Bind next23 full current articles aftersealed clean drafts; disclose earlier producer exposure."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104')
if __name__=='__main__':
    draft_path=ROOT/'clean_meanings_andfull_drafts_v2.json';draft=load(draft_path)
    output=ROOT/'current_full_articles_verified_parent_v1.json';assert not output.exists()
    assert len(draft['records'])==23 and draft['prior_producer_English_exposure_disclosed_topic_IDs']==[21,23]
    release_path=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json')
    release=load(release_path);rom=Path(release['candidate']);assert sha(rom.read_bytes())==release['candidate_sha256']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    image=NdsImage.open(rom);file='/COMMON/HELP.DK4';archive=image.read_file(file);blocks=IlnkContainer.parse(archive).blocks
    assert len(blocks)==211 and IlnkContainer(blocks).to_bytes()==archive
    assert sha(archive)=='015ee6aaab9544555a2bcd90f74dbd10450ca20e441954cf5b99f8196e275cc0'
    rows=[]
    for original in draft['records']:
        index=original['topic_id'];raw=blocks[index];start=int.from_bytes(archive[8+4*index:12+4*index],'little')
        assert archive[start:start+len(raw)]==raw
        rows.append(dict(id=original['id'],topic_id=index,source_reference=original['source_reference'],source_hex=original['source_hex'],
            current_reference=dict(file_path=file,block=index,archive_offset=start,bytes=len(raw),offset_table_slot=8+4*index),
            current_hex=raw.hex(),current_sha256=sha(raw),current_English_with_link_IDs=readable_source(raw),
            current_links=source_links(raw),current_link_IDs=[link['topic_id'] for link in source_links(raw)]))
    labels=[]
    for index in [117,118,119,121,142,150,151,152,157,187,194,201]:
        raw=blocks[index];labels.append(dict(topic_id=index,current_heading=readable_source(raw).split('\n',1)[0],
            current_block_sha256=sha(raw),only_heading_consulted_not_the_unselected_body=True))
    save(output,dict(file_path=file,current_ROM=str(rom),current_ROM_sha256=release['candidate_sha256'],
        current_archive_sha256=sha(archive),current_topic_count=211,original_clean_topic_count=202,records=rows,UI_heading_bindings=labels,
        sealed_draft=str(draft_path),sealed_draft_sha256=sha(draft_path.read_bytes()),
        draft_precedes_this_current_extraction=True,no_wholly_unconsulted_old_English_claim_for21_and23=True,
        verified_parent_release=str(release_path),verified_parent_release_sha256=sha(release_path.read_bytes()),
        actual_gameplay=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    for row in rows:print('\nTOPIC',row['topic_id'],row['current_English_with_link_IDs'])
    print('Term headings:',[(r['topic_id'],r['current_heading']) for r in labels])
