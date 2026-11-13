"""Clean-source captain/deputy/helm context;no prose or completion credit."""

import struct
from pathlib import Path

from dk4tool.patch.planning_finance_editorial_v2 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_planning_finance_context_v857 import select
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/bridge_duties_v866')
ROM=Path('out/all_routes_combined_v863_candidate.nds')
GROUPS=((5,1471,'Captain',False),(6,1475,'Deputy',True),(4,1487,'Helm',True))


def main():
    assert not (ROOT/'source_context_packet.json').exists();ROOT.mkdir(parents=True,exist_ok=True)
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==756 and ledger['records_with_source_and_prose_pass']==759
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    npc_table=struct.unpack_from('<I',arm,0x12834)[0];hero_table=struct.unpack_from('<I',arm,0x1291C)[0]
    groups=[]
    for role,first,name,has_npc in GROUPS:
        npc=struct.unpack_from('<I',arm,npc_table-0x02000000+role*4)[0]
        hero=struct.unpack_from('<I',arm,hero_table-0x02000000+role*4)[0]
        if has_npc:
            assert struct.unpack_from('<8I',arm,npc-0x02000000)==tuple(range(first,first+8))
            hero_first=first+8
        else:
            assert npc==0;hero_first=first
        assert struct.unpack_from('<4I',arm,hero-0x02000000)==tuple(range(hero_first,hero_first+4))
        groups.append({'role_ID':role,'context_label_provisional_not_translation_approval':name,
            'NPC_pointer':npc,'NPC_IDs':list(range(first,first+8)) if has_npc else [],
            'actual_protagonist_pointer':hero,'protagonist_IDs':list(range(hero_first,hero_first+4))})
    raw,receipt=snapshot('personal_cabin_v840_838_Charles_after',3200);_,get=machine_at(arm,raw);actors=get(0xCB184)
    cases=[]
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        for role,first,name,has_npc in GROUPS:
            if not has_npc:continue
            row=select(arm,raw,actor,role,first+voice);row.update(native_voice_class=voice,source_RAM=receipt);cases.append(row)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'personal_cabin_v840_838_Charles_after',3200),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        hraw,hrec=snapshot(folder,frame);_,hget=machine_at(arm,hraw);assert hget(0x7F244)==actor
        for role,first,name,has_npc in GROUPS:
            row=select(arm,hraw,actor,role,first+(8 if has_npc else 0)+actor)
            row.update(source_RAM=hrec,actual_original_captain_ID_preserved=actor);cases.append(row)
    assert len(cases)==54 and {r['selected_message_ID'] for r in cases}==set(range(1471,1499))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1470,1500):
        records.append({'message_id':n,'selected_review_family':1471<=n<=1498,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    packet={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256':sha(arm),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all54_original_role_helper_selections':cases,'records_with_immediate_storage_neighbors':records,
        'independent_voice_variants_not_consecutive_dialogue':True,'captain_role5_has_no_NPC_table':True,
        'no_Sera_special_override_for_roles4_5_6':True,
        'review_leads_not_final_translations':[
            {'message_id':1472,'issue':'Current possessive fleet claim loses source resolve to make the strongest fleet.'},
            {'message_id':1476,'issue':'Current label fragment omits the duty of supporting the admiral behind the scenes.'},
            {'message_id':1477,'issue':'Source IC marker must be mapped in native macro consumer before deciding name/pronoun English.'},
            {'message_id':1483,'issue':'Source has confident deputy-duty acceptance followed by puzzled realization;current English changes tone.'},
            {'message_id':1489,'issue':'Source combines accepting the helm with hard starboard;current text omits first clause.'},
            {'message_id':1492,'issue':'Current absolute cannot-hit assertion strengthens source confident resolve to evade enemy shells.'},
            {'message_id':1494,'issue':'Source invites the viewer to see skill with the wheel;current assurance omits the demonstration.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'not_manuscript_native_font_or_actual_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'source_context_packet.json',packet)
    ledger['next_bridge_duties_source_packet']={'proof':str(ROOT/'source_context_packet.json'),
        'proof_sha256':sha((ROOT/'source_context_packet.json').read_bytes()),'native_message_IDs':list(range(1471,1499)),
        'status':'54-original-role-selectors-and-clean-current-packet-proved-prose-review-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V866-Bridge-duties-context','proof':str(ROOT/'source_context_packet.json'),
        'original_numeric_helper_cases':54,'scope':'28 independent captain/deputy/helm comments1471-1498,storage neighbors,and IC macro lead. Four genuine captains;two NPC eight-voice groups.',
        'completed_entries_added':0,'source_prose_review_credit_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    print('Next28 captain/deputy/helm comments:54 original selections pass;IC macro lead open,no editorial completion credit.',flush=True)


if __name__=='__main__':main()
