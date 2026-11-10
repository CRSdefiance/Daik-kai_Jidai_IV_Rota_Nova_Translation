"""Fresh whole-exchange clean glosses before any B185 predecessor English."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B185_clean_context_v5086')
SOURCE=Path('work/analysis/lil_B185_clean_inventory_v5085/all_clean_B185_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('It is cold. It really is chilly.',
        'A5 complains about the felt cold with emphasis. Bind the source speaker before choosing an English role label;no temperature,date or region is supplied in this utterance.'),
    10:('Yes,it has been a long time since it was this cold.',
        'A4 agrees and compares this cold with past experience. Do not invent a particular number of years or a previous journey.'),
    13:('Ah,I want a fur coat. When it is this cold,I feel as if I could freeze.',
        'A5 desires a fur coat and uses personal freezing hyperbole. No purchase,coat ownership,death,medical state or survival mechanic is established.'),
    16:('I hear fur is selling well because of this cold,and prices are going up too,is that not so?',
        'A4 introduces reported current fur sales and rising prices caused by the cold. These economic details are explicit in the source and must not be removed under a blanket no-price rule. The hearsay/confirming stance remains;do not invent numbers,scarcity,profit guarantees,a specific transaction or narrator-verified market state.'),
    19:('That is what I hear too. Ah,it is cold.',
        'A5 confirms the reported information and returns to personal discomfort. Preserve both hearsay agreement and the cold refrain;do not turn this into an independent verified price report.'),
    22:('I hope it gets warm soon.',
        'A4 wishes for warmer weather. This is a wish,not a forecast,date promise or source of a gameplay weather change.'),
    26:('Yes. But while it is cold,I still want fur,after all.',
        'A5 agrees with the wish yet returns to the desire for fur during cold weather. The earlier coat provides the conversational context. Do not add a request for the companion to buy one,marriage,wealth,gendered shopping stereotypes or an actual purchase.'),
    29:('Fur may become popular in Stockholm.',
        'The separate impersonal FE notice predicts possible fashion in Stockholm. Bind the approved city and commodity. The preceding character hearsay about sales/prices does not turn this notice into an already earned boom,guaranteed profit or proof of the earlier conversation location.')
}

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE)
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==8 and len(source['commands'])==11
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    rows=[]
    for original in source['records']:
        r=deepcopy(original);gloss,note=GLOSSES[r['source_record_index']]
        r.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(r)
    ROOT.mkdir(parents=True)
    save(ROOT/'all8_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=185,records=rows,physical_speech_objects=8,source_commands=11,
        complete_exchange_progression='Two people complain about unusually severe cold;one wishes for a fur coat and feels frozen;the other reports fur selling well and rising prices due to the cold;the first confirms hearsay and complains again;the other wishes for warmth;the first agrees but still wants fur while it stays cold;a separate tentative Stockholm fur-fashion notice closes.',
        source_fact_boundaries=['Cold and reported current fur sales/rising prices are explicit source facts within character speech. Preserve reportedness.',
            'The final Stockholm fashion notice remains prospective. No earned boom or guaranteed trading outcome.',
            'No marriage,kinship,date,temperature,price amount,scarcity,completed purchase,medical effect or previous scene location is established.'],
        read_no_predecessor_English=True,all_native_bindings_comparison_localization_formatting_actual_and_release_gates_pending=True,
        new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Eight clean-only B185 glosses recorded. Preserve reported fur sales/rising prices and distinguish the separate prospective Stockholm notice. No old English or review credit.')
