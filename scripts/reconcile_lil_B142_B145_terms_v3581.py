"""Bind the lamp/cloth/map catalogue to clean/current native C strings."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_terms_v3581')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
ITEMS={175:('模様入りの布','Patterned Cloth'),182:('真鍮のランプ','Brass Lamp'),156:('クレオブロスの布地図','Cleobulus Cloth Map')}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);catalog=read(CATALOG);versions=[]
    for version,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        items=[]
        for ident,(jp,en) in ITEMS.items():
            row=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{ident:03d}');assert row['english']==en;ptr=struct.unpack_from('<I',arm,row['offset'])[0];hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1;base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(b'\0');name=tail[:end].decode('cp932');assert name==(jp if version=='clean' else en)
            items.append(dict(item_ID=ident,catalog_record_ID=row['id'],pointer_file_offset=row['offset'],pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=name))
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=items))
    old=Path('work/analysis/lil_B139_B140_terms_v3466/clean_current_items_polder_names_entries_and_copy_census.json');terms=read(old);assert terms['Proof']=='Proof of Supremacy;source-short Proof stays Proof where clear'
    ledger=read('translations/editorial_review_current_v1.json');ROOT.mkdir(parents=True)
    save(ROOT/'three_native_item_names_and_Mediterranean_Proof_context.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),complete_item_pointer_versions=versions,approved_item_names={str(k):v[1] for k,v in ITEMS.items()},approved_Proof_term=terms['Proof'],approved_prior_context=str(old),approved_prior_context_sha256=sha(old.read_bytes()),B145_dialogue_describes_Mediterranean_Proof_map_not_earned_Proof=True,source_does_not_name_Cleobulus_in_spoken_lines_no_insertion=True,source482x_operands=[175,182,156],item_control_effects_not_inferred_from_catalogue=True,whole_goal_Proof_consistency_lead=ledger['Proof_terminology_consistency_lead_v3286'],whole_goal_Proof_consistency_reconciliation_remains_open=True,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Native clean/current175Patterned Cloth,182Brass Lamp,156Cleobulus Cloth Map bound. Spoken geographic Proof wording preserved.')
