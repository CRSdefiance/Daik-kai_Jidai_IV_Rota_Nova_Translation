"""Freshly gloss the complete B166 exchange before predecessor English is exposed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_clean_context_v4053')
SOURCE=Path('work/analysis/lil_B166_clean_v4052/complete_clean42_speeches_two_choice_labels_before_English.json')
CONTEXT='''A man studies Lil's ship and wonders whether its sail placement is wrong. Lil challenges the stranger. He recognizes her as the owner but becomes absorbed in possible improvements:additional sails,changing the basic sail type,more gun batteries oranother cannon type. Lil's attempts to interrupt escalate from puzzled hesitation to an irritated demand for his name. He apologizes for becoming engrossed in someone else's ship,introduces himself as Manuel andsays he used to be a navigator. Seeing ships brings back habits fromhis time atsea. He apologizes again but cannot resist saying the ship is crying andneeds more care. The crying is an affectionate personification,not literal damage diagnosed by narration. He starts to leave;Lil calls him strange.
Camille admires him andwants someone like him aboard. Lil asks why. Camille tells FI she neglects the ship andechoes the crying metaphor. Actor20 can add a complaint about her working people hard;its membership/path andnative name must be bound before authoring. Lil admits she does not understand machinery andshrugs this off. Camille rebukes her defensiveness andsuggests hiring someone who will love the ship in FI's place. This continues the ship-care joke,not a proposal to replace Lil as admiral. Lil reluctantly consents because Camille wants him. Camille respectfully asks the man to look after their ship. Familiar older-man address establishes no kinship. The man wonders whether this means returning as a navigator andhesitates about how long he has been away. No numeric duration,age,nationality,naval rank orsource port is supplied. Camille reassures him that his love of ships means he cannot have forgotten the sea;this is Camille's confidence,not a tested certification. Camille asks him to cherish the ship because they seem to make it cry. The man thanks him,agrees andgives his full name,source Manuel Almeida. Verify the original actor23 progressive/full-catalogue spellings before choosing the established English form.
He now respectfully addresses the admiral andoffers advice on refitting the flagship's duty rooms. The two choices request the advice orpolitely decline it. His spoken agreement/introduction precede the menu;this alone does not prove where the runtime recruitment effect executes. Native command andend-path ownership must be checked. Yes leads to instruction focused on rooms forlong voyages;No has a separate brief response that leaves the decision to the admiral. Preserve each path andthe later source controls without flattening branches orinventing an earned recruitment event.
The advice distinguishes seven room groups:persuasive crew assigned to副官室 or礼拝室 ease sailors' dissatisfaction;staff in調理室 and飼育室 reduce the fleet's water/food consumption;a ship's doctor in診察室 treats companions' andsailors' fatigue,epidemic illness andinjuries;sick/injured navigators recover faster in個室 or娯楽室;a carpenter like Manuel repairs damaged ships in材木室 while sailing andalso helps refitting/repairs atshipyards. Preserve the source grouping,actors,conditions andlocations without inventing which individual room reduces which individual resource orclaiming instant/full recovery. Bind every room,role,stat andshipyard term to the reviewed UI/help before authoring. He calls the explanation brisk,asks if it helped,andwarns that the fleet's fate depends on the admiral's decisions,so refitting deserves care. Preserve his tactful expertise,ship affection,apologetic absorption andnew professional respect,Lil's impatient irreverence andfrank technical ignorance,andCamille's enthusiastic but gently scolding mediation. No new family relationship,rank,retirement status,exact elapsed time ormedical assurance is implied. Whole-exchange/native/control/actual/release coverage remain separate;all44 objects are uncredited until their required checks pass. The wider editorial goal,graphics separation andlater older-record technical re-audit remain open.'''
MEANINGS={
5:'The man wonders whether the sail position is wrong,then trails off considering another possibility. Keep his absorbed uncertainty andunfinished thought.',
8:'Lil calls out impatiently andasks whether he has some business with this ship. She has not invited him to inspect orrefit it.',
12:'He asks whether she owns the ship andsays a little more work would improve it greatly. Preserve possibility rather than a confirmed damage assessment.',
16:'Lil gives a puzzled double-question reaction. Preserve her confusion without inventing a spoken question ornew fact.',
20:'He thinks of fitting additional sails orchanging the basic sail type. Keep the two alternatives andbind both sail terms to reviewed UI.',
23:'Lil hesitantly tries to interrupt. Preserve her unsuccessful attempt to get his attention,without supplying a new question.',
27:'He considers increasing the number of gun batteries to make the ship stronger,then wonders whether changing cannon type would be better. Keep the self-correction andtwo distinct proposals.',
30:'Lil loses patience,tells him to stop anddemands to know who he is. Preserve her irritation without adding an insult absent fromthe source.',
33:'He apologizes for getting absorbed even though the ship is not his. Preserve the courteous embarrassment andownership distinction.',
37:'He introduces himself as Manuel andsays he used to be a navigator. Bind the established actor23 spelling;do not add a military rank orformal retirement.',
40:'Lil gives an unimpressed acknowledgment that he was a navigator. Preserve the skeptical ornoncommittal response rather than enthusiastic recruitment.',
44:'He says seeing a ship makes him think about allsorts of things,andhe cannot shake habits fromhis time atsea. Do not invent a duration away fromthe sea.',
48:'He acknowledges she probably finds him presumptuous,apologizes andasks permission forone more remark. Keep his tactful apology andinability to stop advising.',
52:'He qualifies this as possibly unwanted advice,personifies the ship as crying,andurges a little more care. Preserve the metaphor without diagnosing a literal condition.',
56:'Lil calls after him to wait. Preserve the short interruption as he prepares to leave.',
60:'He apologizes for speaking so freely,asks her not to take offense andsays goodbye. Preserve his considerate departure rather than hostility.',
64:'Lil privately orquietly calls him strange. The source supplies no more specific insult ordiagnosis.',
68:'Camille challenges her dismissal,says the man is impressive,andasks FI whether they could use someone like him aboard. Preserve FI andCamille\'s admiration.',
71:'Lil asks why. Keep the brief direct question that invites Camille\'s explanation.',
75:'Camille tells FI she does not take care of the ship atall,andthat this is why the ship is crying. Preserve FI andthe quoted personification,without asserting an actual supernatural voice.',
87:'Optional actor20 adds that she works people hard too. Preserve the teasing complaint;bind actor identity andbranch ownership before authoring.',
94:'Lil says there is little she can do because she knows absolutely nothing about machinery. Preserve her candid ignorance andshrugging defensiveness,not a narrator claim of incapacity.',
98:'Camille tells her not to get defensive andexplains that someone else can love the ship in FI\'s place. Preserve FI andthe ship-care context,not replacing the admiral.',
102:'Camille confidently says the ship will stop crying that way,then asks whether they may invite the man onto their ship. Keep the prediction as his hope andthe request forLil\'s consent.',
106:'Lil hesitates,then agrees ifCamille wants it. Preserve reluctant consent andthe established Camille name.',
109:'Camille respectfully asks the older man whether he would look after their ship. Familiar address creates no family relationship.',
112:'The man asks whether this means becoming a navigator,then hesitates over how many years have passed since he left the sea. No number orformal retirement is given.',
116:'Camille says he should be as capable as those still active,andthat someone who loves ships so much cannot have forgotten the sea. Preserve encouragement as Camille\'s belief,not independently proved ability.',
119:'The man admits that is true butstill hesitates. Keep the lingering uncertainty rather than turning this into full acceptance.',
123:'Camille asks him to cherish that ship because they seem to make it cry. Preserve the affectionate care metaphor andself-deprecating persuasion.',
127:'The man thanks Camille andsays that,given such kind words,he will accept. This is his spoken agreement,not proof of a completed runtime effect.',
130:'He formally introduces himself again by his full name,source Manuel Almeida,andasks for a good relationship going forward. Bind the established native actor23 full name.',
134:'He respectfully addresses the admiral andoffers a little advice on refitting the flagship\'s duty rooms. Preserve flagship scope andthe optional nature ofthe advice.',
149:'On the advice path,he begins an explanation ofduty rooms,especially those that prepare the fleet forlong voyages. Keep this focus rather than a complete-room catalogue claim.',
153:'Assigning people withhigh persuasion to副官室 and礼拝室 helps relieve sailors\' dissatisfaction. Preserve the stat condition,both rooms andeffect without numerical guarantees.',
157:'People assigned to調理室 and飼育室 reduce the fleet\'s water andfood consumption. Preserve both rooms andresources without inventing an individual room-to-resource mapping.',
161:'A ship\'s doctor in診察室 treats fatigue,epidemic illness andinjuries amongcompanions andsailors. Preserve the role,room,three conditions andboth groups without promising instant/full cures.',
165:'Navigators whoare sick orinjured recover faster ifassigned to個室 or娯楽室. Preserve the assignment condition,both rooms andfaster recovery without conflating this withthe doctor\'s treatment.',
169:'Carpenters like him repair damaged ships in材木室 while sailing,andalso assist withrefitting andrepairs atshipyards. Preserve his explicit carpenter role,the room,at-sea timing andshipyard help.',
172:'He says this was a brisk explanation andasks whether it was helpful. Preserve his courteous check-in rather than a new instruction.',
175:'He says the fleet\'s fate depends on the admiral\'s decisions,andurges careful refitting without neglecting it. Preserve the responsibility warning andpractical care.',
181:'On the decline path,he acknowledges the answer andleaves it to the admiral. Do not turn declining advice into refusing recruitment.'
}
CHOICE_MEANINGS={140:'The player asks him to give the offered advice. This accepts the explanation,not a separately offered hiring decision.',142:'The player politely declines the offered advice. Do not imply dismissing orrefusing to recruit him.'}
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);rows=deepcopy(v['block']['records']);choices=deepcopy(v['typed_choice_records'])
    assert len(rows)==len(MEANINGS)==42 and {r['source_record_index'] for r in rows}==set(MEANINGS)
    assert len(choices)==2 and {r['source_record_index'] for r in choices}==set(CHOICE_MEANINGS)
    for r in [*rows,*choices]:r.update(fresh_source_gloss=(CHOICE_MEANINGS if r.get('kind')=='typed-choice-label' else MEANINGS)[r['source_record_index']],whole_exchange_context=CONTEXT,clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'all44_complete_B166_exchange_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),whole_exchange_context=CONTEXT,records=rows,typed_choice_records=choices,all44_clean_first_glosses_before_predecessor_English=True,source_macro_counts=v['source_macro_counts'],room_role_stat_UI_binding_pending=True,source_actor23_and_optional20_native_names_pending=True,source_menu_paths_predicates_effect_end_and_source_entry_pending=True,source_native_fonts_actual_registered_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(v['source_transcript']),Path(__file__)]},full_goal_complete=False))
    print('B166:42 speech+2 choice clean-first glosses recorded;all44 uncredited;predecessor English unexposed.')
