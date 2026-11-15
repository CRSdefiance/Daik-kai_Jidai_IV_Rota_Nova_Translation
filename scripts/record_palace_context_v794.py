"""Record original Palace context and an actual blank-page defect;no prose credit."""

import shutil
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.arrival_notices_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save
from unicorn.arm_const import UC_ARM_REG_R0

ROOT=Path('work/analysis/palace_editorial_v794')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v794_context')
DOC=Path('docs/palace_context_v794_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V794 Palace source and original context')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    report=read(CAP/'capture_report.json')
    assert report['frames']==7200 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    donor=report['battery_save_preloaded'];assert donor['source']!=donor['destination']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']=='fd58ada7b41a60a48fdb5e78a59891176653a0aa9ca2326f2645968662a453bc'
    frames={r['frame']:r for r in report['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    raw={}
    for r in report['read_only_pause_RAM_snapshots']+report['read_only_capture_RAM_snapshots']:
        data=Path(r['path']).read_bytes();assert len(data)==0x400000 and sha(data)==r['sha256'] and r['read_only_export']
        raw[r['frame']]=data
    rom=NdsImage.open(report['ROM']);a=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),a)
    owner,printed,wrapped=[struct.unpack_from('<I',a,n)[0] for n in (0x552A0,0x5444C,0x54450)]
    rows=[]
    for f,n in ((4800,1156),(5200,1156),(5600,1157),(6400,1158)):
        assert cstring(raw[f],owner+0x2030)==entries[n].text
        rows.append({'frame':f,'message_id':n,'template_hex':entries[n].text.hex(),
            'printf_hex':cstring(raw[f],printed).hex(),'wrapped_hex':cstring(raw[f],wrapped).hex(),'capture':frames[f]})
    assert '２８４２'.encode('cp932') in cstring(raw[4800],printed)
    assert cstring(raw[4800],wrapped)==cstring(raw[5200],wrapped)
    blank=Image.open(frames[5200]['path']).convert('RGB')
    assert not [(x,y) for y in range(294,366) for x in range(16,244) if blank.getpixel((x,y))==(0,8,0)]
    money=[]
    for f,data in sorted(raw.items()):
        if f<3200:continue
        assert state(a,data)['cash']==8371
        money.append({'frame':f,'cash':8371})
    for fn in (state,models,persistent_objects,tasks):assert fn(a,raw[3200])==fn(a,raw[7200])
    cpu=machine(a);cpu.mem_write(BASE,raw[4800])
    def get(fn,args=()):call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);actors=get(0xCB184)
    ruler=get(0xB2CD8,(town,4));minister=get(0xB2CD8,(town,11))
    assert (ruler-actors-4)//32==92 and (minister-actors-4)//32==121
    context={'candidate_sha256':report['ROM_sha256'],'report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'actual_original_English_holds':rows,'ruler_building_role4_actor92':ruler,'minister_building_role11_actor121':minister,
        'old1156_extra_blank_page_at5200':True,'actual_printf_minimum_fee':2842,
        'all_fee_digits_need_exact_Glyph_recheck_during_repair':True,'all_cash_observations':money,
        'cash_models_actors_towns_items_goods_couriers_exact_initial_to_return':True,
        'normal_town_return_frame':7200,'no_transaction_fees_or_test_fixtures':True,
        'old_wording_or_formatting_not_editorially_approved':True,'source_inventory_only_IDs':list(range(1146,1177)),
        'no_new_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes())}
    save(ROOT/'original_context_proof.json',context)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==496 and ledger['records_with_source_and_prose_pass']==499
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    ledger['findings'].append({'id':'Palace1156-extra-blank-page-original-display','native_message_ids':[1156],
        'status':'actual-defect-confirmed-unrevised','proof':str(ROOT/'original_context_proof.json'),
        'detail':'4800 shows old fee offer;5200 is blank while the same1156 wrapped paragraph remains resident;5600 advances to1157. Check all four fee digits against native printf2842 during repair.'})
    ledger['findings'].append({'id':'Palace1162-insufficient-funds-meaning','native_message_ids':[1162],
        'status':'source-inventory-lead-context-and-editorial-review-pending',
        'detail':'Clean Japanese says funds are insufficient for the contract;older English says The fee is too high. Needs full original branch/provider review.'})
    ledger['palace_next_source_packet']={'inventory':str(ROOT/'source_inventory.json'),'context':str(ROOT/'original_context_proof.json'),
        'source_reference_leads':str(ROOT/'source_contract_and_letter_branches.json'),
        'review_credit':0,'next':'Bind full Palace recommendation/introduction-letter,defense,contract-fee and treasure-loan branches before authoring31 source-based paragraphs.'}
    save(ledger_path,ledger)
    DOC.write_text('''# V794: Palace source inventory and original context

V792 remains the exact current combined ROM/patch. V793 completed49 diplomatic
entries;coverage remains496 complete(359 revised/137 retained),499 source/prose,
three reviewed drafts750-752. Palace1146-1176 is now inventoried against exact clean
Japanese/current ROM and record references. Inventory is not source/context/prose
review approval and adds no review or completion credit.

An ordinary7200-frame cold boot from an isolated byte-exact Istanbul DSV visits
the Palace without any condition/location/inventory/RNG fixtures. The first touch
at20,20 selects Market without entering it;128,20 selects Palace. A opens the
Palace menu. Contract displays1156 at4800,an empty page at5200,then1157 at5600.
The number picker at6000 shows the full minimum2842 and projected funds5529.
B cancels;1158 at6400 is the King's annoyance. A dismisses and B returns to town
at7200. The native wallet remains8371 throughout. All covered financial/model/
actor/town/item/goods/courier objects are exact between3200 and7200;no fee is paid.
The original save is unchanged. This is context evidence for old wording,not
approval of the existing translation or a full-route/hardware playthrough.

Original town lookup confirms ruler role4/actor92(the actual King portrait) and
minister role11/actor121. Original branch fragments5D698..5D970 and5DD64..5E1F8
are saved as source leads.1150/1152 refer to use of a document in another city;
the introduction/recommendation distinction and every argument/branch remain to
bind before prose authoring.1162 currently reverses an insufficient-funds warning
into The fee is too high;it is a source lead awaiting full context review.

The blank5200 paper has no dialogue ink in the native text region while the same
1156 owner/template/wrapped bytes remain resident. This is a confirmed extra empty
page in actual playback. Its exact padding/page mechanism remains to verify as
part of the rewrite. Native printf includes full-width2842;check all four visible
digits explicitly during repair. No unverified glyph-loss cause is asserted.

Source packet:work/analysis/palace_editorial_v794/source_inventory.json.
Context:original_context_proof.json and the terminal capture report under
E:/Rota Nova translations/Generated/work/emulation_v193/palace_v794_context.
Source branch files are research leads;low-valued literal matches in other data
are not automatically live Palace callers. No new English draft or ROM layer is
created. The separate graphics audit/18 plaques,Online-body exclusion,brown marks,
approved names and older-record follow-up remain unchanged. Full goal active.
''',encoding='utf-8')
    heading='## V794: Palace inventory and actual original blank-page defect'
    summary='31 Palace entries inventoried with exact clean/current pins;ordinary King contract quote1156,blank extra page1156,share question1157,amount picker and cancel1158 captured.8371 coins and native persistent objects return unchanged. No new prose or completion credit;496 complete,499 source/prose,three reviewed pending. Full Palace branch/argument mapping and blank-page/glyph repair remain next.'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        p=Path(name);text=p.read_text(encoding='utf-8');assert heading not in text
        p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V794 context](palace_context_v794_checkpoint.md).\n',encoding='utf-8')
    paths=list(ROOT.glob('*.json'))+[DOC,ledger_path,Path('scripts/record_palace_context_v794.py')]
    rows=[]
    for p in paths:
        assert not p.is_absolute();d=ARCHIVE/p;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
        assert sha(p.read_bytes())==sha(d.read_bytes());rows.append({'source':str(p),'copy':str(d),'sha256':sha(p.read_bytes())})
    receipt={'copies':rows,'all_copies_SHA256_exact':True};save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'Palace context/blank-page finding saved;{len(rows)} artifacts exact.496 complete unchanged;no review credit;goal active.',flush=True)


if __name__=='__main__':main()
