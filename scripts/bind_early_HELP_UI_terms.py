"""Read source/current native labels and the complete existing Rafael Help continuation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET,common_message_entries
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
if __name__=='__main__':
    output=ROOT/'native_UI_terms_andRafael_continuation_v1.json';assert not output.exists()
    binding_path=ROOT/'current_T00_T20_verified_parent_v1.json';binding=load(binding_path)
    image=NdsImage.open(binding['current_ROM']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(binding['current_ROM']).read_bytes())==binding['current_ROM_sha256']
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    assert sha(arm)=='d45932617dfffeac2932a5a8d398d236758a8c1a835081ab9601aea5ed67dac2'
    assert sha(common)=='94cfaf8debed48b1b76af82f850ac26d44c16b8d50704791e3587c49fadf5903'
    original=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    current=owned_entries(common,arm,sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    terms=['策謀の立案','艦隊誘導','偽文書制作','悪い噂','買収','参謀','勢力値','謎の小物','発展度','水夫編成','交易所','軍事投資']
    rows=[]
    for term in terms:
        for source in original:
            if len(source.text)>48 or term.encode('cp932') not in source.text:continue
            target=current[source.message_id]
            rows.append(dict(Japanese_term=term,message_id=source.message_id,source_hex=source.text.hex(),
                source_text=source.text.decode('cp932'),source_reference=dict(file_path='/COMMON/MESFILE.DK4',block=source.block,offset=source.block_offset,record_index=source.record_index),
                current_hex=target.text.hex(),current_text=target.text.decode('cp932'),
                current_reference=dict(file_path='/COMMON/MESFILE.DK4',block=target.block,offset=target.block_offset,record_index=target.record_index)))
    archive=image.read_file('/COMMON/HELP.DK4');blocks=IlnkContainer.parse(archive).blocks
    continuation=202;raw=blocks[continuation];offset=int.from_bytes(archive[8+continuation*4:12+continuation*4],'little')
    assert [r['current_link_IDs'] for r in binding['records'] if r['topic_id']==7]==[[37,202]]
    save(output,dict(current_ROM=binding['current_ROM'],current_ROM_sha256=binding['current_ROM_sha256'],
        source_current_UI_labels=rows,HELP_heading_bindings=binding['UI_heading_bindings'],
        Rafael_article_continuation=dict(topic_id=continuation,reference=dict(file_path='/COMMON/HELP.DK4',block=continuation,archive_offset=offset,bytes=len(raw)),
            current_hex=raw.hex(),current_text=readable_source(raw),current_link_IDs=[r['topic_id'] for r in source_links(raw)],
            clean_Japanese_meaning_owned_by_topic7=True,not_an_additional_source_article_orcompletion_unit=True),
        current_topic_count=len(blocks),nine_added_current_topics_andall_unselected_bytes_must_be_preserved=True,
        original_parser_code_andexact_current_directory_unchanged=True,
        native_execution_ornew_gameplay_claim=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [binding_path,Path(__file__)]}))
    print('Native UI labels',[(r['Japanese_term'],r['message_id'],r['current_text']) for r in rows])
    print('Existing Rafael continuation202:',readable_source(raw))
