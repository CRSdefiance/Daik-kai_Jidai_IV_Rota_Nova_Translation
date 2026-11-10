"""Bind unchanged shared name/item fields to Maria source andown-current consumers; no item UI approval."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.draft_Maria_B207_prose_v7687 import CURRENT,CONSUMERS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_shared_fields_v7711')
PRIOR=Path('work/analysis/lil_B234_name_item_v7578/personal_Carlo_shared_Trader_regional_storage_alias_leads_anditem106_scope.json')
NAMES=Path('translations/maria_B207_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,consumers,prior,names=map(read,[CURRENT,CONSUMERS,PRIOR,NAMES])
    old,now,clean=[NdsImage.open(p) for p in [prior['current_ROM'],packet['current_ROM'],'work/clean.nds']]
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']==consumers['candidate_sha256']
    assert sha(Path(prior['current_ROM']).read_bytes())==prior['current_ROM_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert old.read_file(path)==now.read_file(path)
    arm,jp=now.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48])
    assert len(payload)==123264 and arm.find(payload)==1517964 and sha(arm)==packet['current_ARM9_sha256']
    def field(r):
        pointer=r['pointer_field']
        if r.get('source_null'):
            assert r['current_null'] and jp[pointer:pointer+4]==arm[pointer:pointer+4]==bytes(4);return
        for blob,label in [(jp,'source'),(arm,'current')]:
            assert int.from_bytes(blob[pointer:pointer+4],'little')==r[label+'_pointer']
            value=bytes.fromhex(r[label+'_terminated_hex']);at=r[label+'_storage_offset'];assert value[-1]==0 and not 0 in value[:-1] and blob[at:at+len(value)]==value
            if label=='current' and r['current_storage_kind']=='verified-current-staged-payload':
                assert at==1518924==1517964+960 and r['current_pointer']==37256672==0x02387A20+960 and value==b'European\0' and payload[960:960+len(value)]==value
            else:assert r[label+'_pointer']==0x02000000+at
    for row in names['records']:
        assert row['english']=={19:'Carlo Sinat',104:'Trader'}[row['actor_ID']] and all(row['review'].values())
        assert row['source_fields']==next(r['fields'] for r in consumers['source_name_fields'] if r['actor_ID']==row['actor_ID'])
        for f in row['source_fields']:field(f)
    item=deepcopy(prior['source_named_item']);field(item);assert item['record_ID']=='DK4_ITEM_POINTER_106' and item['Japanese']=='グレゴリウスの冠' and item['English']=="Gregory's Crown"
    aliases=[r for r in packet['records'] if r['source_record_index'] in [8,15]]
    assert len(aliases)==2 and all('フィリポ' in r['source_Japanese'] for r in aliases)
    ROOT.mkdir(parents=True);save(ROOT/'Maria_Carlo_Trader_regional_fields_alias_anditem106_unchanged_scope.json',dict(source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),consumer_proof=str(CONSUMERS),consumer_proof_sha256=sha(CONSUMERS.read_bytes()),speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),prior_shared_field_proof=str(PRIOR),prior_shared_field_proof_sha256=sha(PRIOR.read_bytes()),shared_field_data_exact_reuse_bywhole_ARM9_COMMON_FNT_equality_not_other_route_UI_approval=True,actors=deepcopy(consumers['source_name_fields']),actor104_regional_secondary_storage_contract=deepcopy(prior['actor104_regional_secondary_storage_contract']),source_named_item=item,current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(jp),source_dialogue_alias_Japanese='フィリポ',source_dialogue_alias_English='Filippo',source_dialogue_alias_refs=[dict(id=r['id'],reference=r['source_reference'],source_hex=r['source_hex']) for r in aliases],actor104_source_oyaji_role_not_Carlo_father_or_automatic_personal_name=True,regional_European_literal_not_part_of_either_returned_name_no_nationality_surname_orbiography_inferred=True,reported_papal_association_blessing_andconditional_find_not_confirmed_mechanic=True,no_specific_pope_Gregory_biography_ordinal_or_item_title_invented_in_dialogue=True,no_item_or_actor_asset_change_or_duplicate_credit=True,no_inventory_card_orcomplete_item_mechanic_orother_consumer_approval=True,full207_name_role_alias_andearlier_consumer_review_remains_open=True,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,CONSUMERS,PRIOR,NAMES,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Maria own names/aliases bind unchanged Carlo/Trader/regional/item106 fields;physical1518924 andpayload960 remain distinct. No item card/mechanics orglobal name approval.')
