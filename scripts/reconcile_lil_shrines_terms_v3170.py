"""Read clean/current item pointers and exact registered catalog names;no edits."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_terms_v3170')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
IDS=[25,27,77,81,87,108,174,182]
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
        assert len(rows)==8
        results.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),rows=rows))
    site=read('translations/historic_site_names_v2.json');row=next(r for r in site['records']if r['id']=='HISTORIC_SITE_NAME_05');assert row['japanese']=='サンチャゴ大聖堂' and row['english']=='Santiago Cathedral'
    versions=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');pointer=struct.unpack_from('<I',arm,row['pointer_field'])[0];text=arm[pointer-0x02000000:].split(bytes([0]))[0].decode('cp932');assert text==(row['japanese']if label=='clean'else row['english']);versions.append(dict(version=label,pointer_field=row['pointer_field'],pointer=pointer,text=text))
    voices=read('work/analysis/lil_Shrines_Temples_voices_v3167/current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json');names={k:v['current_catalog_name']for k,v in voices['selected_static_source_selectors'].items()}
    assert all(names[k]==v for k,v in {'139':'Priest','151':'Retainer','160':'Villager','177':'Sect Leader','178':'Ｆollower','191':'Donna'}.items())
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_items_cathedral_and_source_roles.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),eight_item_pointer_versions=results,cathedral_native_versions=versions,cathedral_config='translations/historic_site_names_v2.json',cathedral_config_sha256=sha(Path('translations/historic_site_names_v2.json').read_bytes()),
        approved_terms=dict(Proof_full='Proof of Conquest',Proof_source_abbreviation='Proof',map_keys='Map Keys',cathedral='Santiago Cathedral',prayer='Father,Son,Holy Spirit;Amen',Sphinx='Sphinx'),
        Proof_term_reason='Retain established current B101Proof ofConquest andpriorIndia/Polder wording. Native item category isProof;other historical Supremacy wording doesnot triggera globalrename orolder-record audit inthis newbatch.',
        approved_item_names={str(r['item_ID']):r['text']for r in results[1]['rows']},source_item_names_are_not_inserted_into_spoken_lines_that_only_say_sword_cross_lamp_or_this=True,
        important_source_distinctions=['B103commemorativecross dialogue andunusuallyoldcross/AncientCross UIitem preserve their irony withoutinventedreligiousprovenance.','B104item87BoastfulBeak lends power fordebate;do notinvent a goddess orstone speaker label.','B106OldParchment source UIidentity doesnot licenseinvented destruction ornew lore.','B108BrassLamp retains localfaith/community entrustinglamp,not inventedfamilyinheritance.','B110StarlightGlobe isthereward;thejar-shaped tablet remains thepuzzle,not renamed astheglobe.'],
        exact_current_catalog_names=names,source_role_reconciliation={'139':'Priest;Father isreligiousaddress,notkinship','151':'Retainer;genericcrew fallback,notnewnobilityrank','160':'Villager;reusedNPCactor acrossdifferent localexchanges,notproofofsameperson','177':'Sect Leader;sourcefictionalmegalithic researchsociety head','178':'Follower;sourcechantinggroup','191':'Donna;currentregisteredname,noinventedrelationship'},
        registered_name_asset_spellings_not_modified=True,approved_dialogue_names=['Rafael','Hodram','Joakim','Maria','Camille','Lil','Fernando'],no_new_graphics_or_UI_display_claim=True,no_ROM_registry_ledger_or_completed_prose_change=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('8clean/currentitempointers,SantiagoCathedral actualnativepointer andPriest/Retainer/Villager/SectLeader/Follower/Donna roles bound. SourceProofofConquest retained;no globalrename ornewdisplaycredit.')
