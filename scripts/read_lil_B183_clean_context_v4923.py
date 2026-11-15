"""Record the complete art-collectors exchange and fresh glosses before old prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B183_clean_context_v4923')
SOURCE=Path('work/analysis/lil_B183_clean_inventory_v4922/all_clean_B183_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:'Hm?',
    10:'It really is wonderful!',
    14:'You think so?',
    18:'Yes. He will become an artist whose name is remembered by future generations.',
    21:'Oh. / I see. A restrained,unconvinced acknowledgment in this exchange;do not turn it into enthusiastic agreement.',
    25:'You would do well to acquire one of his works now,too.',
    28:'I think this one is better!',
    32:'That one is not bad either,but it cannot compare with his work.',
    35:'What are you two talking about? That one over there is obviously a better work.',
    39:'Whatever anyone says,I am buying his painting!',
    42:'I will take something by the painter who painted this one!',
    45:'I will take this one!',
    49:'Thank you for your business,as always.',
    53:'A forceful closing or impact sound:bang/slam. The following remark establishes that the customers have left;the text does not name the object making the sound.',
    57:'They have finally left. I wish they would stop arguing in the shop every single time.',
    61:'Shopkeeper,what was all that commotion just now?',
    65:'That is a pastime of the rich.',
    69:'A pastime of the rich?',
    73:'Yes. Collecting paintings has become fashionable lately.',
    76:'Oh? That is a refined hobby.',
    80:'Well,not many of them really have an eye for it,though.',
    83:'Ha ha ha... You certainly speak your mind,shopkeeper.',
    87:'Oops,please keep that a secret.',
    91:'Of course. / I know. An easy assurance in response to the request for discretion.',
    95:'Paintings seem likely to become fashionable in Basra. Bind the approved city and commodity/category terminology before final English.'
}
CONTEXT=(
    'Read all25 speeches as one two-part shop exchange. The source selector99 opens with a puzzled reaction. '
    'Selector94 enthusiastically praises an unnamed male artist and predicts lasting fame;selector6E is unconvinced and prefers another work. '
    'The first recommends acquiring the admired artist\'s work now,then dismisses the alternative as unable to compare. '
    'Selector84 joins the dispute with a more formal,confident claim that a different work is obviously better. '
    'Each declares a choice:94 will buy the admired artist\'s painting regardless of objections,6E wants a work by the painter of the piece being indicated,and84 chooses the other indicated work. '
    'Keep the demonstratives and disagreement without inventing painting titles,artist names,physical left/right directions or inventory identities. '
    'The source-explicit male pronoun refers to the artist,not proof of the patrons\' genders,relationships or ranks. '
    'Source 私/俺 and 君たち/決まっておる suggest different levels of polish and bluntness,but approved native roles,names and voices remain to be bound. '
    'Do not assume a player character or transfer the previous scene\'s Lady roles.\n\n'
    'The shopkeeper55 gives a conventional polite thanks to the departing customers. An impersonal FE impact/closing sound follows. '
    'The shopkeeper then drops the sales manner and complains that the customers argue in the shop every time. '
    'Selector99 asks what the fuss was about;the shopkeeper calls it a rich person\'s pastime. '
    'The listener repeats that phrase as a question. The shopkeeper explains that collecting paintings is fashionable lately. '
    'The listener calls it a refined hobby,then the shopkeeper dryly adds that few of the collectors really have an eye for art. '
    'The listener laughs at the shopkeeper\'s candor;the shopkeeper catches the indiscretion and asks for secrecy,and the listener casually reassures him. '
    'The humor comes from the collectors\' dogmatic competing tastes and the contrast between the shopkeeper\'s polite service and private skepticism. '
    'Do not make the art objectively worthless,call the collectors frauds,or invent counterfeit works,investment profits,social relationships or artist biographies. '
    'The initial praise is a character judgment,and future fame is a prediction. The buying declarations and service thanks occur in the source,but no price,currency or exact transaction mechanic is given.\n\n'
    'The closing impersonal FE forecasts 絵画 becoming fashionable in バスラ. Bind exact current native names and goods/category terminology before final prose. '
    'The shopkeeper\'s observation of a recent collecting fashion is character speech;the city-specific closing forecast remains tentative. '
    'Basra is named only in the closing notice and does not prove the earlier shop location. '
    'No shortage,price rise,guaranteed profit or already earned game boom follows from the forecast. '
    'Preserve the FE sound as a sound,not narration identifying an unmentioned object or speaker. '
    'This clean-only packet gives no source/prose completion credit,native approval,actual gameplay coverage or natural eligibility claim. '
    'Bind all28 source commands and complete source preambles without importing a conditional layout or number of effects from B182.')

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['read_no_predecessor_English'] and len(source['records'])==25
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    rows=[]
    for r in source['records']:
        row=deepcopy(r);row['fresh_source_gloss']=GLOSSES[r['source_record_index']];rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'all25_clean_exchange_and_fresh_glosses.json',dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        whole_exchange_context=CONTEXT,records=rows,read_no_predecessor_English=True,new_review_credit=0,
        native_name_voice_entry_and_control_binding_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B183 full clean exchange and25 fresh glosses preserved;native names/voices/terms and comparison pending. Zero credit.')
