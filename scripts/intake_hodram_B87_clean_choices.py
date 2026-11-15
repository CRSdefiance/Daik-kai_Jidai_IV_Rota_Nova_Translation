"""Retain the two source labels as typed menu prose, outside the 304 speeches."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

SOURCE=Path('work/analysis/Hodram_B81_B90_clean_20261101/clean_source_packet.json')
OUT=SOURCE.with_name('B87_two_clean_choice_meanings_before_English.json')

if __name__=='__main__':
    assert not OUT.exists();packet=load(SOURCE)
    menus=[(g,c) for g in packet['groups'] for c in g['all_source_commands'] if c['word']==0x2100]
    assert len(menus)==1
    group,command=menus[0];assert group['block']==87 and command['offset']==302
    raw=bytes.fromhex(command['whole_command_hex'])
    assert struct.unpack_from('<3H',raw)==(0x2100,0,12) and len(raw)==command['native_extent']==34
    rows=[]
    for index,offset in enumerate((0,12)):
        at=6+offset;end=raw.index(0,at);limit=18 if index==0 else len(raw)
        value=raw[at:end];assert not any(raw[end:limit]) and end<limit
        japanese=value.decode('cp932')
        expected=['いいだろう','そんな金はない'][index];assert japanese==expected
        rows.append(dict(id=f'SC1_B87_NATIVE_CHOICE_302_{index}',file_path=group['file_path'],
            block=87,kind='typed-choice-label',source_index=index,source_command_offset=302,
            source_relative_label_offset=offset,source_byte_offset=302+at,
            source_hex=value.hex(),source_Japanese=japanese,
            source_meaning_gloss=[
                'The player agrees to give the requested one thousand gold coins.',
                'The player declines, saying he does not have that kind of money. Preserve the stated lack of that sum, not a simple generic No.'][index],
            source_context='Actor4 asks for1000 gold; acceptance leads to repairs, tomorrow’s meeting, a ship gift and the name misunderstanding. The refusal has its own departure and silence. This source-only intake does not prove affordability, choice availability, branch eligibility or earned next-day timing.',
            earlier_English_unconsulted=True,all_five_review_gates_pending=True,new_credit=0))
    save(OUT,dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        choice_command=dict(command,source_hex=raw.hex()),records=rows,
        labels=2,speech_records=304,total_speech_andchoice_prose_objects=306,
        same_two_offset_format_as_previously_qualified_B49_B52_not_permission_to_reuse_their_source_locked_compilers=True,
        current_English_localization_native_getters_provider_caption_sizing_andgameplay_pending=True,
        source_whole_native_command_extent_andzero_padding_retained=True,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Two B87 clean menu-label meanings retained separately;304 speeches+2 labels,all earlier English unconsulted.')
