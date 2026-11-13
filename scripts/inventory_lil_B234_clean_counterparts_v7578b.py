"""Locate byte-identical whole-source exchanges; grant no cross-route review credit."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_clean_counterparts_v7578b');SOURCE=Path('work/analysis/lil_B234_clean_inventory_v7571/all_clean_B234_speeches_before_predecessor_comparison.json');VERIFIED=Path('work/analysis/editorial_handoff_verification_v7570/verified_handoff.json');LEDGER=Path('translations/editorial_review_current_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();d,v=map(read,[SOURCE,VERIFIED]);assert sha(LEDGER.read_bytes())==v['ledger_sha256'];ledger=read(LEDGER);clean=NdsImage.open('work/clean.nds');target=bytes.fromhex(d['clean_block_hex']);assert sha(Path('work/clean.nds').read_bytes())==d['source_ROM_sha256'];indices={r['source_record_index'] for r in d['records']};found=[]
    for route in range(4):
        file=f'/data/SC{route}.DK4'
        for block,payload in enumerate(IlnkContainer.parse(clean.read_file(file)).blocks):
            if payload!=target:continue
            prior=[]
            for family in ledger['completed_editorial_families']:
                for r in family['records']:
                    ref=r.get('source_reference',{});index=r.get('source_record_index',ref.get('record_index'))
                    if r.get('file_path')==file and ref.get('block')==block and index in indices:prior.append(dict(id=r['id'],source_record_index=index,completed_family=family['id']))
            found.append(dict(file_path=file,block=block,whole_clean_block_sha256=sha(payload),source_stored_bytes=len(payload),complete_source_commands=20,source_speeches=18,previously_completed_positions=prior,previously_completed_unique_positions=len({r['source_record_index'] for r in prior}),whole_source_byte_equality_only_not_current_English_context_control_entry_orrelease_approval=True))
    assert any(r['file_path']=='/data/SC2.DK4' and r['block']==234 for r in found);ROOT.mkdir(parents=True);save(ROOT/'byte_identical_clean_papal_trade_exchange_counterpart_leads.json',dict(source_inventory=str(SOURCE),source_inventory_sha256=sha(SOURCE.read_bytes()),verified_handoff=str(VERIFIED),verified_handoff_sha256=sha(VERIFIED.read_bytes()),source_ROM_sha256=d['source_ROM_sha256'],counterparts=found,other_route_English_bodies_unread=True,no_fresh_other_route_context_name_native_orrelease_approval=True,no_duplicate_credit=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VERIFIED,Path(__file__)]},full_goal_complete=False));print([(r['file_path'],r['block'],r['previously_completed_unique_positions']) for r in found])
