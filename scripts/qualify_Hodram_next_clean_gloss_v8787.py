"""Qualify source glosses without assigning unbound actors a gender or FA a personal-name type."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_next_clean_gloss_v8787')
PRIOR=Path('work/analysis/Hodram_next_clean_gloss_v8786/82_first_clean_glosses_context_andcultural_fidelity_before_current_English.json')
CHANGES={
    (54,14):{'do his best':'do their best'},
    (55,6):{'military man called FA':'military person identified as FA'},
    (58,39):{'his father':'the accuser\'s father'},
    (58,42):{'his friend':'the accuser\'s friend'},
    (58,190):{'he very much wants':'the speaker very much wants'},
    (58,217):{'he intends':'the speaker intends'},
    (59,9):{'he says':'the speaker says','he will':'the speaker will'},
    (59,13):{'He respectfully':'The speaker respectfully'},
    (59,26):{'He declares':'The speaker declares'},
    (60,15):{'He says':'The companion says','saved him':'saved the companion','nursed him':'nursed the companion'},
    (60,19):{'He learned':'The companion learned','treated him':'treated the companion','worried about him':'worried about the companion'},
    (60,26):{'made him feel':'made the companion feel','his second home':'the companion\'s second home'},
    (60,29):{'He says he then':'The companion says they then'},
    (60,33):{'He urges':'The companion urges'},
}
if __name__=='__main__':
    assert not ROOT.exists();old=read(PRIOR);new=deepcopy(old);assert old['source_speech_objects']==82 and old['no_new_ROM_emulator_run_current_English_read_orcounter_credit']
    findings=[]
    for g in new['groups']:
        for row in g['records']:
            key=g['block'],row['source_record_index'];before=row['first_clean_source_gloss']
            if key in CHANGES:
                after=before
                for a,b in CHANGES[key].items():assert a in after,(key,a);after=after.replace(a,b)
                assert after!=before;row['prior_first_clean_source_gloss_preserved']=before;row['first_clean_source_gloss']=after
                row['source_gloss_qualification']='Use gender-independent reporting until original actor identity/name consumers are bound. Preserve explicit source male/female and actual kinship where stated. FA stays an unexpanded source identity substitution; its native referent/type remains to be proven.'
                findings.append(dict(id=row['id'],source_reference=deepcopy(row['source_reference']),previous_gloss=before,qualified_gloss=after,reason=row['source_gloss_qualification']))
    assert len(findings)==14
    new.update(prior_source_gloss=str(PRIOR),prior_source_gloss_sha256=sha(PRIOR.read_bytes()),source_gloss_qualifications=findings,
        unbound_actor_genders_andmacro_referent_types_not_invented=True,source_explicit_foreign_girl_male_accused_actual_father_youngerbrother_andfamily_simile_distinctions_preserved=True,
        all82_sources_references_commands_EV1_andolder_English_unread_status_exact=True)
    assert [g['commands'] for g in new['groups']]==[g['commands'] for g in old['groups']]
    for a,b in zip([r for g in old['groups'] for r in g['records']],[r for g in new['groups'] for r in g['records']],strict=True):
        assert all(b[k]==v for k,v in a.items() if k!='first_clean_source_gloss')
    new['evidence']={**old['evidence'],str(PRIOR):sha(PRIOR.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    ROOT.mkdir(parents=True);save(ROOT/'82_qualified_clean_glosses_no_unbound_gender_orFA_type.json',new)
    print('82clean source glosses qualified:14 reporting-pronoun/macro-type refinements;all source bytes/context intact,earlier gloss retained. No prior English,localized approvals,ROM orcredit.',flush=True)
