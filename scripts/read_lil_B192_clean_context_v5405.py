"""Read the complete tobacco-curiosity exchange before previous English."""
from pathlib import Path
from copy import deepcopy
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B192_clean_context_v5405')
SOURCE=Path('work/analysis/lil_B192_clean_inventory_v5404/all_clean_B192_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('Hey,have you ever smoked tobacco?','Selector0x99/153 asks about the companion’s experience. Preserve tobacco/smoking without specifying a pipe,cigar,cigarette,brand,ingredient or date. Bind original names/roles/voices before assigning age,profession,kinship or status.'),
    10:('Do you mean you have not smoked it yet?','Selector0x73/115 responds with surprise and turns the question back on153. Keep the reversal and familiar rough address without inventing bullying,rank,age,insult or prior smoking history.'),
    13:('That is right. I have not really had the chance,so I still have not tried it.','153 admits lack of experience and explains the missing opportunity. Do not turn the explanation into a refusal,poverty,illness,prohibition or health judgment.'),
    16:('Really! Even though it is so popular! You are probably about the only person in this town who has never smoked it.','115 expresses astonishment,claims current popularity,and uses probable colloquial hyperbole to pressure153. Preserve きっと/about the only person as character rhetoric,not narrator-certified universal smoking,a statistical fact,an earned fashion flag or an established date/location.'),
    20:('I-is that so? I would like to try smoking it too.','153 stammers in uncertainty and expresses curiosity/desire to try. Preserve both nervousness and willingness without inventing age,dependence,a completed smoke,coercion or narrator endorsement.'),
    23:('Yes. All right,I will let you try smoking some. Follow me.','115 affirms the popularity claim,offers to give153 the chance to smoke and tells the companion to follow. This is a proposed next action,not a completed purchase,gift,preparation or actual smoking. No smoking instructions,equipment,price or specific destination are supplied. The familiar tone does not establish hierarchy or employment.'),
    26:('Y-yeah.','153 gives a hesitant assent. Preserve the nervous/uncertain delivery after the offer rather than inventing refusal,complete confidence,age or a finished action.'),
    30:('Tobacco may become popular in Istanbul.','Separate impersonal FE is prospective. Bind the actual approved tobacco/category/commodity and Istanbul names before comparison. The notice does not certify the earlier this-town location,the speaker’s popularity hyperbole,earned fashion,health claims,purchases or actual smoking.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex'])
    assert d['read_no_predecessor_English'] and len(d['records'])==8 and len(d['commands'])==11
    assert len(b)==404 and 8+struct.unpack_from('<H',b,4)[0]==402 and b[402:]==bytes(2)
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in d['commands'] if c['word']!=0x4000]==[(8,0xA000,'00a0ffff012116a1'),(396,0xC200,'00c2'),(398,0,'00000000')]
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    rows=[]
    for original in d['records']:
        row=deepcopy(original);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[row['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all8_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=192,records=rows,physical_speech_objects=8,source_commands=11,
        source_stored_bytes=404,source_logical_end=402,source_alignment_tailzeros=2,source_selectors_hex=['99','73','FE'],source_selectors_decimal=[153,115,254],
        complete_exchange_progression='153 asks whether115 has smoked tobacco;115 is surprised153 has not;153 admits lacking the chance;115 claims current popularity and probable near-universal experience in this town;153 nervously expresses interest;115 offers the chance and says to follow;153 hesitantly agrees;a separate prospective tobacco/Istanbul notice follows.',
        source_fact_boundaries=[
            'Bind exact0x99153/0x73115 source names,roles and voices before authoring English. Familiar rough address and stammering do not prove kinship,rank,age,employment or a recurring relationship.',
            'Preserve the question reversal,lack-of-opportunity explanation,astonishment,popularity claim,probably-only-person hyperbole,nervous curiosity,offer and hesitant agreement as one exchange.',
            'Tobacco and smoking are explicit. No pipe,cigar,cigarette,brand,recipe,preparation,equipment,price,quantity,medical or health claim is supplied.',
            'Popularity and probable universal experience belong to115’s rhetoric. Do not erase source facts or convert them to narrator-certified town statistics,an earned boom or reader advice.',
            'The offer and assent are intentions. No purchase,gift,actual smoking,dependence,recovery,coercion or specific destination is established.',
            'Bind actual approved Tobacco/Istanbul identities;the FE stays prospective and does not establish the earlier this-town location.',
            'Preserve all11 linear commands,eight speeches,A0008 raw00a0ffff012116a1,C200396,end398,404 stored/402 logical bytes and2 tailzeros. No source predicate or relative branch exists;do not inherit B191 mixed/no-effect conditional structure.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B192:8 clean-only glosses preserve tobacco curiosity,popularity hyperbole,stammering,offer and intentions. Linear11commands;no old English or credit.')
