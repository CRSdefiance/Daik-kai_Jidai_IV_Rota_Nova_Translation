"""Fresh clean-only sweetness exchange,source emphasis and reported-role limits."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B186_clean_context_v5131')
SOURCE=Path('work/analysis/lil_B186_clean_inventory_v5130/all_clean_B186_speeches_before_predecessor_comparison.json')
GLOSSES={
    5:('Hmm... Something is missing. That is it,something sweet! I want sweetness.',
        'AE identifies missing sweetness. The following taste/customer discussion supplies food or flavor context,but no specific dish,recipe,ingredient or business is named. Bind the speaker before choosing a role;do not turn preparation/taste into a trading tip.'),
    9:('Sweetness?',
        'AF questions/echoes the requested sweetness. Preserve the small questioning reply rather than turning it into agreement or a request for a specific ingredient.'),
    13:('Yes! With such a light/refreshing taste,the customers or guests will not be satisfied. Sweet is what matters. Sweet!',
        'AE emphatically insists on sweetness for customer/guest satisfaction. さっぱり describes light/clean taste;do not declare the food objectively bad or invent a dish. The conspicuously pronounced English-loan sweet and its repetition carry comic emphasis. Bind roles/context before choosing customers versus guests;no noble rank is proved by polished speech alone.'),
    16:('Uh... Is that so?',
        'AF gives a hesitant or mildly doubtful response. Preserve the contrast with AE\'s certainty without inventing an argument,threat or objective judgment of customer preferences.'),
    20:('Because I say so,it is absolutely so!',
        'AE bases her certainty on her own say-so. This is a comic character assertion,not narrator confirmation or proof of rank,ownership or authority beyond the exchange.'),
    23:('Uh... What should I do to make it sweeter?',
        'AF asks for a practical way to increase sweetness. Do not invent sugar,honey,an ingredient quantity,a recipe step or a completed change.'),
    26:('Thinking of that is your job,is it not?',
        'AE returns responsibility to AF. The source explicitly says job,but does not by itself establish a named profession,formal contract,personal relationship or a master/servant title.'),
    29:('... Yeah,yeah.',
        'AF\'s muttered perfunctory acknowledgment contrasts with his earlier more formal hesitant replies. Bind the voice before localizing the exact dismissive register. Do not turn it into enthusiastic compliance or a newly invented insult.'),
    33:('In any case,it is certain that sweet things will become fashionable.',
        'AE speaks confidently about future popularity. Preserve her certainty as character speech;do not flatten it into the tentative system notice or claim narrator-verified demand,prices,profit or earned fashion.'),
    36:('Yeah,yeah.',
        'Preserve the second distinct perfunctory acknowledgment. Its repetition matters to the comic rhythm and must not be merged away as redundant prose.'),
    40:('In any case,sweet! Do your best,will you? Oh-hohohoho!',
        'AE repeats the conspicuous sweet emphasis,urges effort and gives a stylized self-assured laugh. Preserve the comic voice without inventing nobility,physical departure,an action or a finished product.'),
    63:('Sweet things may become popular in Alexandria.',
        'The separate null-actor FE predicts possible popularity in Alexandria. Bind approved city and trade category before selecting terminology. Do not guess Sugar from the taste discussion or infer the earlier scene location,an earned boom,a price change or guaranteed profit.')
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE)
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==12 and len(source['commands'])==24
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    rows=[]
    for original in source['records']:
        r=deepcopy(original);gloss,note=GLOSSES[r['source_record_index']];r.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(r)
    leaves=[r for r in source['commands'] if r['word']!=0x4000]
    assert [(r['offset'],r['word']) for r in leaves]==[(540,0x8000),(548,0x200),(552,0x300),(556,0x400),(560,0xA000),(568,0x100),(572,0xA000),(580,0x100),(584,0xA000),(592,0x100),(644,0xC200),(646,0)]
    ROOT.mkdir(parents=True);save(ROOT/'all12_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=186,records=rows,physical_speech_objects=12,source_commands=24,
        complete_exchange_progression='AE notices missing sweetness;AF asks;AE insists on sweet taste and customer/guest satisfaction;AF doubts;AE asserts her own certainty;AF asks how;AE says figuring it out is his job;AF mutters;AE confidently predicts popularity;AF repeats perfunctory agreement;AE repeats sweet,urges effort and laughs;a separate tentative Alexandria notice follows conditional effects.',
        source_fact_boundaries=['Food/flavor preparation context must not become a trading-tip rewrite. No specific dish or ingredient is named.',
            'AE\'s certainty and comic self-authority stay character speech;the impersonal closing notice is tentative.',
            'Bind source AE174/AF175 identities,voices and approved sweet-goods/Alexandria terms before predecessor English. Do not infer rank,profession,kinship or ownership.',
            'This block has24 commands,one raw700 RNG predicate540,six relative commands,three alternative A000 effects,C200644,end646 and652 stored/650 logical bytes. Preserve its own conditional structure and two trailing zeros;do not inherit B185 linear/no-predicate/no-tail-padding assumptions.'],
        read_no_predecessor_English=True,all_native_bindings_comparison_localization_formatting_actual_and_release_gates_pending=True,
        new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Twelve clean-only B186 glosses recorded;comic sweetness exchange and character certainty remain distinct from tentative Alexandria notice. Preserve24 commands and raw700 conditional effects. No old English or credit.')
