"""Bind current actor labels and clean/current approved item-pointer strings."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_terms_v3220')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
VOICES=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
IDS=[114,131,139,176,180]
if __name__=='__main__':
    assert not ROOT.exists()
    source,voices,catalog=map(read,[SOURCE,VOICES,CATALOG])
    assert voices['source_context_sha256']==sha(SOURCE.read_bytes())
    results=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000)
        views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if label=='current':
            assert len(code.sections[3].data)-48==123040
            views.append((POOL,bytes(code.sections[3].data[:-48]),'registered-exact123040-byte-runtime-pool-copy'))
        rows=[]
        for r in catalog['records']:
            if not r['id'].startswith('DK4_ITEM_POINTER_'):continue
            ident=int(r['id'].rsplit('_',1)[1])
            if ident not in IDS:continue
            pointer=struct.unpack_from('<I',arm,r['offset'])[0]
            hits=[v for v in views if v[0]<=pointer<v[0]+len(v[1])];assert len(hits)==1
            base,data,owner=hits[0];tail=data[pointer-base:];end=tail.index(b'\0');text=tail[:end].decode('cp932')
            if label=='current':assert text==r['english']
            rows.append(dict(item_ID=ident,catalog_record_ID=r['id'],pointer_file_offset=r['offset'],
                pointer=pointer,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=text))
        assert len(rows)==5
        results.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),rows=rows))
    names={int(k):v['current_catalog_name'] for k,v in voices['selected_static_source_selectors'].items()}
    assert {k:names[k] for k in [4,19,104,137,163,170,179,198]}=={
        4:'Janus Pasar',19:'Carlo Sinat',104:'Trader',137:'Senior Monk',163:'Boy',170:'Mysterious Old Man',179:'Villager',198:'Benazir'}
    roles={2:'Lil Argot',4:'Janus Pasar',9:'Camille',14:'Emilio',19:'Carlo',20:'Fernando',
        104:'Trader',137:'Senior Monk',163:'Boy;grandchild oftheelder inB112',
        170:'Mysterious Old Man catalogrole;theBoy actualgrandfather,notLil kin',
        179:'Villager catalogrole;do notinvent chief/priest/guide rank',
        198:'Benazir;sourcegift-recipient/tip-giver,notprovenromanticrelationship'}
    ROOT.mkdir(parents=True)
    save(ROOT/'clean_current_items_and_native_actor_role_reconciliation.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        voice_proof=str(VOICES),voice_proof_sha256=sha(VOICES.read_bytes()),
        registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),
        five_item_pointer_versions=results,approved_item_names={str(r['item_ID']):r['text'] for r in results[1]['rows']},
        exact_current_catalog_names={str(k):v for k,v in names.items()},source_speaker_annotation_reconciliation=roles,
        source_context_provisional_Manuel_annotation_for_hex13_corrected_to_native_actor19_Carlo=True,
        only_new_uncredited_context_annotation_corrected_not_older_completed_families=True,
        approved_terms=dict(Proof_full='Proof of Conquest',Proof_source_abbreviation='Proof',Guild='Guild',
            grandfather_relation='elderAAandboyA3only;Lilnotkin',Buddhist_context='Buddha;offering;monasticcourtesy;donation',
            rice_quantity='one cargo hold proposedbyLil',FE_gold_coins=24000,FI='Lil',FA='Argot',FO='Argot Co.'),
        source_generic_object_words_not_replaced_with_UI_item_names=True,
        no_invented_country_sect_rank_kinship_romance_item_origin_or_earned_reward=True,
        important_source_distinctions=[
            'HuizongArt UIidentity doesnotauthorizeaddingartist/emperorname tospoken genericgift.',
            'JadeJewel UIidentity doesnotauthorizeaddingmagicalpower,physicalsize orconfirmedbuildingpurpose.',
            'UpperStoneTablet name remainsseparate fromJanus tentativeforeignorigin/mosque materialinference.',
            'EagleFigurehead name doesnotflattenstyle6couldbemadeintoafigurehead intooriginalownershipcertainty.',
            'CeremonialKnife UIidentity preservesgenericspokenknife andtribalspiritualsignificance.',
            'OnlyoneFE150targetisexact24000goldnotice;unreachablewhispercopy belongs tocanonicalMariafollowup.'],
        native_item_command_operands_remain_unmodified_no_reward_execution_claim=True,
        registered_names_assets_not_modified=True,no_ROM_registry_ledger_or_completed_prose_change=True,
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('5clean/currentitempointer strings bound;native19Carlo/137SeniorMonk/170grandfather/179Villager/198Benazir reconciled. No genericnoun replacedornewrelationship/earnedreward invented.')
