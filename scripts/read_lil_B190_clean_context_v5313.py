"""Read the reported unexplained-illness remedy exchange before old English."""
from copy import deepcopy
from pathlib import Path
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_clean_context_v5313')
SOURCE=Path('work/analysis/lil_B190_clean_inventory_v5312/all_clean_B190_speeches_before_predecessor_comparison.json')
GLOSSES={
    24:('Hey,have you heard?','0x9F/159 opens a gossip exchange with an attention-getting question. Bind the actual role/name and voice before assigning occupation,kinship or rank.'),
    28:('Heard what?','0x77/119 asks what the companion means. This brief natural follow-up starts the information gap rather than stating ignorance of every local event.'),
    32:('About the owner of this residence.','159 identifies the head/owner of the residence in the current deictic setting. お屋敷 suggests a substantial residence,but 旦那 does not by itself prove nobility,employer,husband,master,kinship,a personal name or new rank. Bind the source roles before choosing address.'),
    36:('You mean the illness of unknown cause?','119 recognizes the reported topic. Preserve unknown cause rather than inventing a diagnosis,specific symptom or supernatural explanation.'),
    40:('Yes,that is it.','159 confirms the topic. Keep the casual repeated affirmation without adding a new disease claim.'),
    44:('Everyone knows about that.','119 makes a colloquial character claim that the illness is common knowledge. Do not turn this hyperbole into a narrator fact or proof that every NPC has a knowledge flag.'),
    48:('What about what happened afterward?','159 asks whether the companion knows the subsequent development. This sets up new gossip,not a second illness.'),
    52:('Afterward?','119 gives a surprised/questioning echo,inviting the revelation. Do not fill in the answer prematurely.'),
    56:('They say an ordinary commercially available medicine cured that illness in one go.','159 reports the striking claim. Preserve both 市販 available for sale to the public and 一発で治した quick/one-go cure as hearsay. Do not erase source-explicit cure claims or upgrade them to narrator-confirmed efficacy. No brand,dose,recipe,physician,treatment mechanism or source town is supplied.'),
    59:('A commercially available medicine cured an illness of unknown cause?','119 questions the surprising account and repeats its two key details. Preserve the question rather than asserting objective efficacy or a verified diagnosis.'),
    63:('That is right. Amazing,is it not?','159 enthusiastically affirms the account and prompts agreement. The confidence is the character’s;it does not independently verify the cure.'),
    67:('Yes...but is it true?','119 reacts but explicitly doubts the truth of the report. Keep the emotional turn from amazement to skepticism;do not erase the doubt or add hostility.'),
    71:('Apparently,it is true. And the medicine has a reputation for working on every illness.','159 answers with らしい reportedness and adds the panacea reputation. Preserve both claims under apparent/reputed status,not a guaranteed real cure,a verified game mechanic or a real-world recommendation. No ingredient,brand or quantity is given.'),
    74:('Incredible! I would like some medicine like that myself.','119 is persuaded enough to express desire. Preserve the excited reaction and hypothetical condition;no actual purchase,use,recovery or medical expertise is established.'),
    77:('Shall we go try buying some?','159 proposes going to buy the medicine. This is a shopping intention,not a completed transaction or proof of availability in the current scene town.'),
    81:('All right,let us go.','119 agrees to go. Preserve the casual resolve without supplying a destination,price,purchase outcome or use.'),
    85:('Medicine may become popular in Havana.','Separate impersonal FE remains prospective. Bind the project’s actual approved city/commodity names before English comparison. The forecast does not prove the earlier residence location,earned fashion,narrator-confirmed medical claims or completed shopping.'),
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);block=bytes.fromhex(source['clean_block_hex'])
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==17 and len(source['commands'])==29
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    assert sorted({r['source_selector'] for r in source['records']})==[119,159,254]
    assert len(block)==608 and 8+struct.unpack_from('<H',block,4)[0]==606 and block[606:]==bytes(2)
    nontext=[(c['offset'],c['word'],c['native_extent']) for c in source['commands'] if c['word']!=0x4000]
    assert nontext==[(8,0x8000,8),(16,0x200,4),(20,0x300,4),(24,0x400,4),(28,0xA000,8),(36,0x100,28),
        (40,0xA000,8),(48,0x100,16),(52,0xA000,8),(60,0x100,4),(600,0xC200,2),(602,0,4)]
    assert struct.unpack_from('<I',block,12)[0]==500
    rows=[]
    for original in source['records']:
        row=deepcopy(original);gloss,note=GLOSSES[row['source_record_index']]
        row.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all17_clean_exchange_and_fresh_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=190,records=rows,
        physical_speech_objects=17,source_commands=29,source_stored_bytes=608,source_logical_end=606,source_alignment_tailzeros=2,
        source_selectors_hex=['9F','77','FE'],source_selectors_decimal=[159,119,254],
        complete_exchange_progression='159 asks whether119 has heard about the residence owner;119 knows of the unexplained illness;159 asks about later developments and reports an ordinary medicine curing it in one go;119 questions this,then asks whether it is true;159 says apparently so and reports a panacea reputation;119 expresses desire;both agree to go try buying some;a separate tentative medicine/Havana notice follows.',
        source_fact_boundaries=[
            'Bind actual selectors0x9F159/0x77119 names and voices;do not infer kinship,employment,rank or a new personal name from 旦那 or familiar diction.',
            'Preserve the complete gossip progression,information gap,common-knowledge hyperbole,surprised echo,astonishment,explicit skepticism and subsequent willingness.',
            'Keep unknown cause,ordinary commercially available medicine,reported one-go cure,apparent truth and reputed efficacy for every illness. These are source-explicit character claims,not narrator-confirmed cure,recipe,dose or medical advice.',
            'Both final replies express intention to go buy;no transaction,use,recovery,price,brand,ingredient or destination is supplied.',
            'The separate FE is prospective and does not establish the residence location,earned boom or verified efficacy. Bind approved medicine/Havana terms before comparison.',
            'This is a conditional block,not the B189 linear structure. Preserve29 commands,17 speeches,one500 predicate at8,six relative sites16/20/24/36/48/60,three opaque A000 alternatives28/40/52,nested ancestors,C200600,end602 and two tailzeros. Native predicate ownership,skip paths and actual selected effect need distinct checks.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B190:17 clean-only glosses preserve reported remedy claims,skepticism and shopping intentions. One500 predicate/six relative sites/three alternatives require distinct future checks;zero credit.')
