"""Extract the complete clean B167 exchange and source-owned choice pointers before English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_clean_v4116')
INVENTORY = Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    inventory = read(INVENTORY)
    lead = deepcopy(next(b for b in inventory['blocks'] if b['block']==167))
    clean = Path('work/clean.nds')
    image = NdsImage.open(clean)
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[167]
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block) == lead['clean_block_sha256'] and len(block) == 2176 and lead['speeches'] == 27
    assert lead['source_selectors'] == [2,4,13,23,109] and lead['source_macro_counts'] == {'FI':0,'FA':0,'FO':0}
    for command in lead['complete_native_commands']:
        at = command['offset']
        assert block[at:at+command['native_extent']].hex() == command['whole_command_hex']
    for row in lead['records']:
        at,raw = row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)] == raw and block[at+len(raw)] == 0
        assert block[at-5:at+1].hex() == row['source_complete_preamble_hex']
        assert raw[1:].decode('cp932') == row['source_Japanese']
    menus = [c for c in lead['complete_native_commands'] if c['word']==0x2100]
    assert len(menus) == 1 and menus[0]['offset'] == 152
    menu = menus[0]
    labels = []
    for option in [0,1]:
        at = menu['offset']+6+struct.unpack_from('<H',block,menu['offset']+2+2*option)[0]
        end = block.index(b'\0',at)
        assert at < end < menu['offset']+menu['native_extent']
        raw = block[at:end]
        labels.append(dict(id=f'DK4_CHOICE_B167_C152_O{option}',file_path='/data/SC2.DK4',block=167,
            source_record_index=block[:at].count(b'\0'),kind='typed-choice-label',command_offset=152,option_index=option,
            source_reference=dict(offset=at,bytes=len(raw),command_offset=152,option_index=option),
            source_hex=raw.hex(),source_Japanese=raw.decode('cp932')))
    ROOT.mkdir(parents=True)
    transcript = ROOT/'SC2_B167_complete_clean_exchange_and_choices.txt'
    lines = ['B167 clean source:27 speeches and two typed labels. Native path,actor and effect ownership still require binding.']
    for row in sorted([*lead['records'],*labels],key=lambda r:r['source_reference']['offset']):
        lines.extend(['\n'+row['id']+' '+row.get('kind','progressive')+' actor'+str(row.get('source_selector'))+
            ' ancestors'+str(row.get('ancestor_0100_offsets',[])),row['source_Japanese']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'complete_clean27_speeches_two_choice_labels_before_English.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,typed_choice_records=labels,total_editorial_objects=29,source_selectors=lead['source_selectors'],
        source_macro_counts=lead['source_macro_counts'],source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        whole_clean_exchange_gloss_before_predecessor_English_pending=True,
        native_voice_control_choice_entry_effect_fonts_actual_release_pending=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]},full_goal_complete=False))
    print('B167 clean-only packet:27 speeches and two typed labels;predecessor English unexposed,no credit.')
