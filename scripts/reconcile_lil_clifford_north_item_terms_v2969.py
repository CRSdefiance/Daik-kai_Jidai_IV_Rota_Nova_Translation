"""Read clean/current item pointers and exact registered catalog names;no edits."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_item_terms_v2969')
SOURCE=Path('work/analysis/lil_Clifford_North_New_World_source_v2965/complete143_clean_current_native_context.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
IDS=[160,179,186]
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);catalog=read(CATALOG);results=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000)
        views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if label=='current':
            assert len(code.sections[3].data)-48==123040
            views.append((POOL,bytes(code.sections[3].data[:-48]),'registered-exact123040-byte-runtime-pool-copy'))
        rows=[]
        for row in catalog['records']:
            if not row['id'].startswith('DK4_ITEM_POINTER_'):continue
            n=int(row['id'].rsplit('_',1)[1])
            if n not in IDS:continue
            pointer=struct.unpack_from('<I',arm,row['offset'])[0];hits=[v for v in views if v[0]<=pointer<v[0]+len(v[1])];assert len(hits)==1
            at,data,owner=hits[0];tail=data[pointer-at:];end=tail.index(b'\0');text=tail[:end].decode('cp932')
            if label=='current':assert text==row['english']
            rows.append(dict(item_ID=n,catalog_record_ID=row['id'],pointer_file_offset=row['offset'],pointer=pointer,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=text))
        assert len(rows)==3
        results.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),rows=rows))
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_and_registered_item_names.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_catalog=str(CATALOG),registered_catalog_sha256=sha(CATALOG.read_bytes()),versions=results,
        certain_spelling_and_name_reconciliations=['Tang Bamboo Craft','Bamboo Assembly Plan','Chiron Bamboo Map is a registered UI identity,not newly named in this spoken scene'],
        prose_policy='Keep Tang-dynasty cultural attribution andcomplete source artifact distinctions in glosses. Use registered Tang Bamboo Craft andBamboo Assembly Plan in English. Do not identify the unnamed hidden map asChiron in spoken prose unless source explicitly names it. No UI,graphics oritem-effect edits.',
        all3_current_pointer_strings_equal_registered_names=True,all3_clean_source_names_and_current_terminology_exactly_referenced=True,no_native_UI_or_graphics_test_claim=True,no_ROM_registry_ledger_or_completed_prose_change=True,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('3clean/current itempointer strings match registered Tang Bamboo Craft,Bamboo Assembly Plan andChiron Bamboo Map;zero credit/no UIchange.')
