"""Read the complete dye-buying sales pitch from clean Japanese before older English."""
from pathlib import Path
from copy import deepcopy
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_clean_context_v5355')
SOURCE=Path('work/analysis/lil_B191_clean_inventory_v5354/all_clean_B191_speeches_before_predecessor_comparison.json')
GLOSSES={
    53:('After all,only that dye can produce this color.','Selector0x56/86 recognizes the particular color obtainable from the dye. Preserve the character’s exclusivity claim without inventing a named pigment,cloth,recipe,origin or objective trade mechanic. Bind the actual role/name and voice before identifying a profession.'),
    56:('Exactly,is it not? If you do not buy it now,the people from other shops will buy it all up.','Selector0x9A/154 agrees and urges immediate purchase,warning that competitors will buy everything. This pressure is an explicit speaker claim;do not erase it or turn it into a narrator-verified shortage,already completed buyout or universal price rule.'),
    60:('But...','86 hesitates despite liking the color. Keep the interruption/reluctance rather than inventing the reason,an inability to pay or a rejected purchase.'),
    64:('What are you being so leisurely about? It will be too late once it sells out.','154 challenges the hesitation and repeats urgency. 悠長 criticizes the other person’s relaxed pace;do not invent an insult,command rank or actual sold-out state.'),
    68:('Even if we do not rush out and buy it right now,it is not going to sell out,is it?','86 explicitly questions the scarcity prediction. Preserve the rhetorical doubt and immediate-buying context rather than confirming a shortage or replacing it with price speculation.'),
    72:('That is not so! It is incredibly popular,so it will be gone in no time.','154 rejects the doubt and claims strong popularity plus imminent unavailability. These source-explicit assertions belong to the persuasive speaker;retain them without narrator endorsement or invented numerical stock/sales.'),
    76:('I wonder if that is really so.','86 remains doubtful. This first そうかなあ should retain the hesitant questioning tone and remain distinct from154’s emphatic answer.'),
    80:('It is!','154 emphatically insists. The reply is character confidence,not independent evidence that the prediction or mechanic is true.'),
    84:('All right,I understand. Then I will leave it to you.','86 yields and entrusts the matter to154. Keep the delegated decision without inventing a quantity,price,finished purchase,completed delivery,employment relation or rank.'),
    88:('Please do not sulk. As long as we secure this color,we are sure to make money.','154 addresses86 familiarly as親父さん,asks the other person not to sulk,and promises profit conditional on securing this color. Bind original names/roles before choosing address;親父さん does not by itself prove fatherhood or kinship. Preserve the explicit strong profit pitch as a speaker claim rather than erasing it or certifying a guaranteed game outcome. 色 stays this color;do not invent a garment,quantity,price or named dye.'),
    92:('I wonder if that is really so.','86 repeats the earlier doubt after the profit assurance. Preserve the deliberate repetition and unresolved skepticism rather than declaring agreement or adding a completed transaction.'),
    96:('I am telling you,it is!','154 insistently repeats the assurance. The endingって adds insistence to the previous answer;retain its conversational effect without additional facts.'),
    100:('Dyes may become popular in Calicut.','Separate impersonal FE is prospective. Bind approved city and dye/category/commodity terminology before localization. The notice does not prove earlier scene location,natural activation,earned fashion,stock scarcity,profit or a completed purchase.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex'])
    assert d['read_no_predecessor_English'] and len(d['records'])==13 and len(d['commands'])==38
    assert len(b)==736 and 8+struct.unpack_from('<H',b,4)[0]==734 and b[734:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    predicates=[c for c in d['commands'] if c['word']==0x8000]
    assert [(c['offset'],int.from_bytes(bytes.fromhex(c['whole_command_hex'])[4:8],'little')) for c in predicates]==[(8,500),(28,700),(76,500)]
    assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in d['commands'])==16
    assert [c['offset'] for c in d['commands'] if c['word']==0xA000]==[48,60,96,108]
    rows=[]
    for source in d['records']:
        r=deepcopy(source);r.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(r)
    ROOT.mkdir(parents=True);save(ROOT/'all13_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=191,records=rows,physical_speech_objects=13,source_commands=38,
        source_stored_bytes=736,source_logical_end=734,source_alignment_tailzeros=2,
        source_selectors_hex=['56','9A','FE'],source_selectors_decimal=[86,154,254],
        complete_exchange_progression='86 admires the specific color;154 urges immediate dye buying before competitors buy it up;86 hesitates and questions selling out;154 insists it is popular and will disappear;86 doubts,then entrusts the matter;154 asks86 not to sulk and promises profit if they secure the color;86 repeats doubt and154 repeats assurance;a separate prospective dye/Calicut notice follows.',
        source_fact_boundaries=[
            'Read persuasion,doubt,reluctant delegation,sulking interpretation and repeated skeptical/insistent replies as one exchange. No settled reconciliation or completed purchase is stated.',
            'Bind exact0x5686/0x9A154 roles,names and voices before address. Familiar親父さん does not establish fatherhood,kinship,employment,master or rank.',
            'Preserve explicit competing-shop buyout warning,popularity,imminent sellout and strong conditional profit assurance as character claims. The FE does not independently certify them.',
            'No pigment,ingredient,recipe,garment,quantity,price,price rise,purchase,delivery or outcome is supplied. This color is not automatically a named good.',
            'Bind actual approved dye and Calicut terms;no second alias or category-versus-commodity identity may be assumed.',
            'Preserve all38 commands/13 speeches/three predicates500at8,700at28,500at76/16relative sites/four alternativeA000s48,60,96,108/nested ancestors/C200728/end730/two tailzeros. Do not inherit B190 one-predicate/six-branch structure or flatten conditional paths.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B191:13 clean-only whole-exchange glosses;explicit urgency/profit claims and repeated doubt preserved. Three predicates/16branches/four effects remain unreviewed;zero credit.')
