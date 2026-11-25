"""Extract complete clean B166 dialogue and typed choices before English comparison."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_clean_v4052')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
if __name__=='__main__':
    assert not ROOT.exists();inv=read(INVENTORY);lead=deepcopy(next(b for b in inv['blocks'] if b['block']==166))
    clean=Path('work/clean.nds');image=NdsImage.open(clean);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[166]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256'] and len(block)==2952 and lead['speeches']==42
    for c in lead['complete_native_commands']:assert block[c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex']
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0 and block[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert raw[1:].decode('cp932')==r['source_Japanese']
    menus=[c for c in lead['complete_native_commands'] if c['word']==0x2100];assert len(menus)==1
    menu=menus[0];data=bytes.fromhex(menu['whole_command_hex']);labels=[];at=menu['offset']+6
    for option in range(2):
        end=block.index(b'\0',at);value=block[at:end];index=block[:at].count(b'\0')
        labels.append(dict(id=f'DK4_MES_B166_R{index:04d}',file_path='/data/SC2.DK4',block=166,source_record_index=index,kind='typed-choice-label',source_reference=dict(offset=at,bytes=len(value),command_offset=menu['offset'],option_index=option),source_hex=value.hex(),source_Japanese=value.decode('cp932')))
        at=end+2
    assert [r['source_Japanese'] for r in labels]==['お願いする','遠慮する'] and at==menu['offset']+menu['native_extent']
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B166_complete_clean_exchange_and_choices.txt';lines=['B166 complete clean source:42 speeches plus two typed choice labels. Ancestors/choice offsets are storage structure;path ownership still requires native binding.']
    objects=sorted([*lead['records'],*labels],key=lambda r:r['source_reference']['offset'])
    for r in objects:
        lines.extend(['\n'+r['id']+' '+r.get('kind','progressive')+' actor'+str(r.get('source_selector'))+' ancestors'+str(r.get('ancestor_0100_offsets',[])),r['source_Japanese']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'complete_clean42_speeches_two_choice_labels_before_English.json',dict(format='dk4-editorial-clean-source-context-v1',source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),block=lead,typed_choice_records=labels,total_editorial_objects=44,source_selectors=[2,9,20,23],source_macro_counts=lead['source_macro_counts'],source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),whole_clean_exchange_gloss_before_predecessor_English_pending=True,native_voice_control_choice_entry_effect_fonts_actual_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]},full_goal_complete=False))
    print('B166 clean-only packet:42 speeches,2 typed labels;no predecessor English orcredit.')
