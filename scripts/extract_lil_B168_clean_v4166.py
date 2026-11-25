"""Re-read the complete clean B168 exchange before exposing predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_clean_v4166')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
if __name__=='__main__':
    assert not ROOT.exists();lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==168))
    clean=Path('work/clean.nds');image=NdsImage.open(clean);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[168]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='53de30dc8018fb309688a4bf34e3d7f35f2650f747c6c1a294ce04e69ec8e335'
    assert len(block)==2916 and lead['speeches']==54 and lead['FE_panels']==3
    assert lead['source_selectors']==[2,6,9,20,76,87,165,166,254] and lead['source_macro_counts']=={'FI':7,'FA':1,'FO':1}
    for c in lead['complete_native_commands']:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and raw[1:].decode('cp932')==r['source_Japanese']
    assert sum(c['word']==0x2100 for c in lead['complete_native_commands'])==0
    assert [c['offset'] for c in lead['complete_native_commands'] if c['word']==0]==[2906,2910]
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B168_complete_clean_exchange.txt'
    lines=['B168 clean source:54 complete speech objects including three FE system panels. Current names/voices,commands,entry,effects and display consumers still need exact binding.']
    for r in lead['records']:lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X')+' ancestors'+str(r['ancestor_0100_offsets']),r['source_Japanese']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'complete_clean54_objects_before_English.json',dict(format='dk4-editorial-clean-source-context-v1',source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),block=lead,total_editorial_objects=54,source_selectors=lead['source_selectors'],source_macro_counts=lead['source_macro_counts'],source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),whole_clean_exchange_gloss_before_predecessor_English_pending=True,native_voice_control_entry_effect_fonts_actual_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]},full_goal_complete=False))
    print('B168:54 clean speech objects/three FE panels,FI7/FA1/FO1,no typed menu;predecessor English unexposed,no credit.')
