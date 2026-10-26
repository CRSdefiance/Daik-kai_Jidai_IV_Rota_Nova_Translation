"""Fresh all-unit incoming-reference audit including relocated ITCM data."""
import inspect
from pathlib import Path
from scripts import audit_item_runtime_storage_v785 as old
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_references_v2087')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');a=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');b=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');target=Path(plan['research_ARM9']).read_bytes();b.rom.arm9=target
 source=inspect.getsource(old.census);needle="rb'(?=(...\\x02))'";assert source.count(needle)==1
 source=source.replace(needle,"rb'(?=(...[\\x01\\x02]))'");env=dict(old.__dict__);exec(compile(source,__file__,'exec'),env);census=env['census']
 spans=plan['private_spans'];before,after=[census(r,spans,spans)for r in(a,b)];external=lambda x:sorted(v for v in x if not v[-1]);assert external(before)==external(after),(external(before),external(after))
 data=[[0x01FF9D18,0x01FF9D30]];da,db=[census(r,data,spans)for r in(a,b)];assert not external(da)and not external(db)
 all_units=old.units(a)+[('ARM7',a.rom.arm7RamAddress,bytes(a.rom.arm7))]
 save(ROOT/'all_units_01_02_absolute_branch_ADR_and_Thumb_references.json',dict(source_ARM9_sha256=sha(a.read_file('/__arm9__.bin')),target_ARM9_sha256=sha(target),units=[dict(name=n,base=base,length=len(raw),sha256=sha(raw))for n,base,raw in all_units],private_spans=spans,before=before,after=after,external_incoming_references_unchanged=external(before),packed_status_before=da,packed_status_after=db,no_external_entry_or_alias_to_relocated_status_data=True,all_byte_offsets_absolute_high01_and02_plus_ARM_branch_ADR_and_Thumb_BL_BLX_scanned=True,effective_census_sha256=sha(source.encode()),historical_census_sha256=sha(Path(old.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(units=len(all_units),external_references=len(external(before)),packed_status_external_aliases=0))
