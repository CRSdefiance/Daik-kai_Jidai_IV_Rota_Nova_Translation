"""Derive meaningful B50 source/prose/name/macro/waiver/profile policy challenges."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_policy_test_tools_v8163')
SEMANTIC=[
 ('invented-kinship',6,'Wait!','Wait, my sister!'),
 ('invented-rank',10,'Lil','Admiral Lil'),
 ('invented-completed-alliance',14,'you got the better of us','we signed an alliance'),
 ('invented-apology',18,'thanks','sorry'),
 ('lost-deciphering-key',23,'the key to deciphering the treasure map','the treasure itself'),
 ('reversed-gift',23,"It's yours.","I'm keeping it."),
 ('lost-rueful-defeat',31,'Did I really lose to this guy?','I knew I would win.'),
 ('invented-wedding-preparations',37,'getting ready','getting ready for our wedding'),
 ('swapped-first-surname',40,'{MACRO:FA}','{MACRO:FI}'),
 ('unapproved-Camille',44,'Camille','Camilla'),
 ('lost-long-time-no-see',49,"it's been a while",'we have never met'),
 ('reversed-rebuke',53,"You aren't being rude again, are you?","You're being perfectly polite."),
 ('wrong-dye-object',57,'that dye','a new treasure map'),
 ('wrong-recipient',57,'gave him','gave her'),
 ('lost-future-nonuse',57,"I won't need it anymore","We never used it before"),
 ('world-dominance',61,'the North Sea','the whole world'),
 ('swapped-second-surname',61,'{MACRO:FA}','{MACRO:FO}'),
 ('reversed-dense-insult',69,'Still so dense','Such a genius'),
 ('lost-personal-new-life',73,"I've found there's more to life than making money","we have found a more profitable business"),
 ('removed-private-bluff',86,'No idea, but play along.','I know all about the wedding.'),
 ('invented-certain-gift-occasion',99,'present','wedding present'),
 ('lost-private-confusion',103,'I have no idea what she means','I know exactly what she means'),
 ('swapped-farewell-given-name',108,'{MACRO:FI}','{MACRO:FA}'),
 ('invented-farewell-rank',108,'Take care,','Take care, Commander'),
 ('invented-parenthood',111,'for us too','for our child too'),
 ('guaranteed-effort',114,"I'll do my best",'I guarantee'),
 ('lost-final-unnamed-joke',119,'What were we celebrating, anyway?','Our wedding celebration was wonderful.'),
]
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/validate_Rafael_B49_policy_v8113.py').read_text('utf8')
    semantic=source[source.index('SEMANTIC='):source.index("\n\nif __name__",source.index('SEMANTIC='))]
    receipt=derive('scripts/validate_Rafael_B49_policy_v8113.py','scripts/validate_Rafael_B50_policy_v8163.py',{
        semantic:'SEMANTIC='+repr(SEMANTIC),
        'Rafael_B49_policy_validation_v8113':'Rafael_B50_policy_validation_v8163',
        'Rafael_B49_relocation_v8096/SC0_block49_RESEARCH_ONLY.bin':'Rafael_B50_relocation_v8146/SC0_block50_RESEARCH_ONLY.bin',
        'blocks[49]':'blocks[50]','B49':'B50',
        "r['source_record_index']==15":"r['source_record_index']==40",
        'len(positive)==61':'len(positive)==28',
        "sum(x['qa']['native_page_count'] for x in positive)==61":"sum(x['qa']['native_page_count'] for x in positive)==28",
        "sum(i['severity']=='warning' for x in positive for i in x['qa']['issues'])==3":"sum(i['severity']=='warning' for x in positive for i in x['qa']['issues'])==2",
        "sum(i['code']=='line-break-count' for x in positive for i in x['qa']['issues'])==22":"sum(i['code']=='line-break-count' for x in positive for i in x['qa']['issues'])==18",
        '61_speech61_page_positives_actual_changing_expected_guard_rejections.json':'28_speech28_page_positives_actual_changing_expected_guard_rejections.json',
        'all_original_QA_diagnostics_preserved_22_infos_three_exact_warning_exceptions':'all_original_QA_diagnostics_preserved_18_infos_two_exact_warning_exceptions',
        'all61_single_pages_andallseven_source_selectors_source00_body_guard_preserved':'all28_single_pages_allthree_source_selectors_FA2_FI1_source00_body_guard_preserved',
        'eleven_native_only_speeches_andall_actual_measured_limits_retained':'all28_actual_speeches_andall_bounded_later_measured_limits_retained',
        'B49:61 exact speech positives/61 pages;':'B50:28 exact speech positives/28 pages;',
        '22 infos/3 narrow warning exceptions unchanged.':'18 infos/2 narrow warning exceptions unchanged.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared B50 actual-changing policy positives andsemantic/source/macro/waiver/profile challenges.')
