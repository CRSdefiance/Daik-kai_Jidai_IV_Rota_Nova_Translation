"""Record all nine fresh clean-only tea-scene glosses before consulting older English."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B184_clean_context_v5038')
SOURCE=Path('work/analysis/lil_B184_clean_inventory_v5037/all_clean_B184_speeches_before_predecessor_comparison.json')
GLOSSES={
6:('Ah,delicious. It is the best.',"A pleased reaction to the drink opens the exchange. Bind A5 before choosing the exact voice or an English speaker label;do not invent a relationship to the other drinker."),
10:('Yes,tea really is wonderful.',"The other drinker agrees and explicitly names tea. The pleasure is personal conversation,not a trader's instruction or an objective quality grade."),
14:('It is strange that something this delicious had not been popular before now,isn't it?',"Keep the wondering reaction and past lack of popularity as the character's observation. It does not prove the current game has awarded a city fashion event or price change."),
18:('Yes. People have no eye for quality/discernment.',"The reply agrees and dismisses others' judgment. Localize the idiom 見る目 naturally in the complete tea exchange;do not invent a literal visual defect or a new tea variety."),
22:('Oh,our tea at home is almost gone. Would you buy some tomorrow?',"Keep the household supply running low,a polite request and tomorrow. Do not reinterpret this as a city shortage,a fleet stock warning or a commodity-investment tip. No kinship or marriage is explicit."),
26:('Yes,of course I will buy some.',"A simple willing agreement answers the request. Do not invent a purchase price,quantity,delivery or proof that the purchase already happened."),
30:('Tea really is delicious. It puts my heart/mind at ease.',"Personal enjoyment develops into a soothing feeling. Keep the emotional sense without adding a medical treatment,health bonus or cure."),
33:('We cannot live without tea,can we?',"Personal affectionate hyperbole concludes the drinkers' exchange. Do not turn it into a literal biological need or an added family relationship."),
36:('Tea seems likely to become popular in ソファラ.',"A separate impersonal FE future-fashion notice. Bind approved Tea/Sofala terminology and the native consumer before authoring English. Preserve prospective likelihood;no active boom,shortage,profit or prior scene location is proved.")}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['read_no_predecessor_English'] and {r['source_record_index'] for r in source['records']}==set(GLOSSES);rows=[]
    for original in source['records']:
        gloss,note=GLOSSES[original['source_record_index']];rows.append(dict(original,fresh_source_gloss=gloss,whole_exchange_note=note))
    ROOT.mkdir(parents=True);save(ROOT/'all9_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=184,records=rows,physical_speech_objects=9,source_commands=12,complete_exchange_progression='Two drinkers enjoy tea;wonder that it had not caught on before;criticize others\' judgment;mention nearly depleted household supply and request a purchase tomorrow;agree;describe enjoyment and calm;close with personal hyperbole;separate tentative Sofala tea-fashion notice.',source_fact_boundaries=['A4/A5 names,voices and relationship unbound;do not label them spouses or relatives.','The low supply is household tea,not a town shortage or trading recommendation.','The purchase is requested for tomorrow and accepted,not already completed.','The soothing effect is personal speech,not medical advice or an added gameplay bonus.','The FE notice is a future likelihood and does not establish prior scene location,earned boom,prices or profit.'],read_no_predecessor_English=True,all_native_bindings_comparison_localization_formatting_actual_and_release_gates_pending=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Nine clean-first tea-exchange glosses recorded;no predecessor English,credit or ROM change.')
