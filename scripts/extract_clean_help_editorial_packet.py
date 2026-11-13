"""Capture clean HELP articles and binary links before consulting earlier English."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import save

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
if __name__=='__main__':
    assert not ROOT.exists();path=Path('work/clean.nds')
    assert sha(path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(path);file='/COMMON/HELP.DK4';archive=image.read_file(file)
    blocks=IlnkContainer.parse(archive).blocks
    assert len(blocks)==202 and IlnkContainer(blocks).to_bytes()==archive
    records=[]
    for index,raw in enumerate(blocks):
        offset=int.from_bytes(archive[8+index*4:12+index*4],'little')
        end=int.from_bytes(archive[12+index*4:16+index*4],'little')
        assert archive[offset:end]==raw
        links=source_links(raw)
        assert all(0<=link['topic_id']<len(blocks) for link in links)
        records.append(dict(id=f'HELP_TOPIC_{index}',topic_id=index,
            source_reference=dict(file_path=file,block=index,archive_offset=offset,bytes=len(raw),offset_table_slot=8+index*4),
            source_hex=raw.hex(),source_sha256=sha(raw),source_Japanese_with_link_IDs=readable_source(raw),
            original_links=links,original_link_IDs=[r['topic_id'] for r in links],
            source_only=True,earlier_English_unconsulted=True))
    ROOT.mkdir()
    save(ROOT/'clean_HELP_source_packet.json',dict(source_ROM=str(path),source_ROM_sha256=sha(path.read_bytes()),
        file_path=file,source_archive_sha256=sha(archive),records=records,selected_initial_topic_ids=list(range(21)),
        all202_source_topics_context_available=True,original_binary_link_IDs_character_aware=True,
        no_current_English_extracted_ornew_editorial_credit=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(clean_topics=202,initial_topics=21,current_English_extracted=False,new_credit=0))
