"""Read the entire sake exchange and conditional excited interjection before old English."""
from pathlib import Path
from copy import deepcopy
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B194_clean_context_v5488')
SOURCE=Path('work/analysis/lil_B194_clean_inventory_v5487/all_clean_B194_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('The other day,I drank a liquor called sake.','Selector9C/156 introduces a recent drinking experience and names清酒. Bind approved commodity and actual role/voice before localized English;do not specify a brand,origin,date,quantity or preparation process.'),
    10:('I drank it too.','Selector75/117 shares the experience. It need not have happened at the same time/place or together;no recurring drinking relationship or employment is established.'),
    14:('It is pretty good,is it not?','156 gives a casual approving taste judgment and seeks agreement. Do not convert いける into a measured alcoholic strength,medical effect or narrator quality certification.'),
    18:('Apparently it is made from rice.','117 reports the rice ingredient with らしい. Keep that hearsay rather than a technical recipe or narrator proof;no fermentation,distillation,origin or ingredient proportions are supplied.'),
    22:('Oh,so that is what they make it from.','156 reacts with surprise to the ingredient. Preserve the referent rice and interested response without adding disdain,a new ingredient,recipe step or historical claim.'),
    26:('Hmm. Talking about it has made me want a drink. How about one now?','117 links the conversation to a personal desire and invites156 for a drink now. 一杯 is a natural a-drink invitation;do not invent a measured serving,venue,price,purchase,completed visit or intoxication.'),
    30:('Oh,that sounds good.','156 warmly accepts the invitation. No purchase,actual drinking or finished movement occurs.'),
    34:('Then let us hurry and go.','117 urges prompt departure once agreed. Keep the enthusiastic decision and urgency without narrating completed movement or a destination not in the source.'),
    46:('W-what!! That must surely be the legendary liquor!! Admiral FI,did you hear that!?','Conditional selector06 reacts with emphatic excited certainty and addresses the runtime FI name using source-explicit 提督. The belief belongs to this speaker,not the narrator. Bind the complete low-byte preamble,voice,relationship and FI expansion before authoring. Do not invent age,kinship,a new rank,an item award or proven legendary status.'),
    49:('Hmm! I cannot stand around like this! I am going to buy this sake right away!','06 is roused into an immediate first-person buying intention in an old-fashioned emphatic register. Preserve urgency and the named drink without inventing a completed purchase,amount,price,benefit,reward,venue or transport. Bind actual voice/persona before choosing English idiom.'),
    56:('Sake may become popular in 杭州.','Separate prospective FE. Bind source 清酒 and杭州 to approved current commodity/city names before comparison. No earlier location,earned fashion,completed purchase,price rise or guaranteed profit is proved.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex'])
    assert d['read_no_predecessor_English'] and len(d['records'])==11 and len(d['commands'])==21
    assert len(b)==8+struct.unpack_from('<H',b,4)[0]==540
    nontext=[(c['offset'],c['word']) for c in d['commands'] if c['word']!=0x4000]
    assert nontext==[(8,0xA000),(312,0x8000),(320,0x200),(324,0x300),(328,0x100),(406,0x632A),(494,0xC200),(496,0x100),(534,0xC200),(536,0)]
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert {m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']}==dict(FI=1,FA=0,FO=0)
    rows=[]
    for original in d['records']:
        row=deepcopy(original);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[row['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all11_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=194,records=rows,physical_speech_objects=11,source_commands=21,source_stored_bytes=540,source_logical_end=540,source_alignment_tailzeros=0,
        source_selectors_hex=['9C','75','06','FE'],source_selectors_decimal=[156,117,6,254],source_FI_macros=1,source_FA_macros=0,source_FO_macros=0,
        complete_exchange_progression='156 introduces recently drinking sake;117 shares the experience;156 praises it;117 reports rice as the ingredient;156 reacts;117 becomes thirsty while talking and invites a drink now;156 agrees;117 urges departure. A conditional06 excitedly identifies the drink as a possible legendary liquor,addressing runtime FI with source 提督,and intends to buy sake immediately. A separate prospective sake/杭州 notice follows.',
        source_fact_boundaries=[
            'Bind selectors0x9C/0x75/0x06(decimal156/117/6),complete preambles,voices and progressive/catalogue names before authoring. Familiar speech does not prove kinship,rank,employment or shared prior drinking.',
            'Preserve the whole social progression and conditional enthusiastic reaction,both speakers’ already-completed drinking experiences and the later distinct invitation and buying intentions.',
            'Rice is reported withらしい;legendary liquor is06’s excited inference. Do not upgrade either character claim to narrator fact,recipe,origin,health effect or earned item state.',
            'Source 提督 and runtime FI are explicit in the conditional address. Preserve the macro and bind its actual name/byte parity and source-supported title rather than inventing a new relationship or rank.',
            'A drink now and hurry-and-go are invitations/intentions. The later purchase is also intention;no amount,price,venue,completed purchase,intoxication or benefit is supplied.',
            'Bind actual approved清酒 and杭州 names. The FE is prospective and does not establish the prior scene location,earned fashion,scarcity,price increase or profit.',
            'Preserve all21 native commands/11 speeches,one FI,A0008 raw00a0ffff012536a1,8000at312 raw0080ffff06fe0030,four relative sites320/324/328/496,opaque632A406,two C200494/534 and single end536. Source540 stored/logical bytes has no trailing alignment zeros. Do not inherit B193 linear/no-macro/no-branch assumptions or infer the8000/632A semantics before native investigation.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B194:11 clean-only whole-exchange glosses;conditional06 interjection,one FI,four relatives,two C200 and opaque632A remain unreviewed. No old English or credit.')
