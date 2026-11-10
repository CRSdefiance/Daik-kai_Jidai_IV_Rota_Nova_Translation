"""Revise the two observed company-substitution sentence boundaries from clean context."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

LOGICAL=Path('translations/rafael_B141_B160_contextual_review_v3.json')
FORMATTING=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
PREFERENCES=Path('translations/rafael_B141_B160_visual_preferences_v10.json')
ACTUAL=Path('work/analysis/Rafael557_story_actual_pixels_v1_20261105/focused_actual_pixels.json')
STORED=Path('work/analysis/Rafael557_stored_native_v1_20261105/stored_native_verification.json')
ROOT=Path('work/analysis/Rafael557_company_punctuation_v1_20261105')
REVISIONS={
    'DK4_MES_B154_R0084':("Since you're with FO, I'll tell you straight: everyone around here hates Maldonado.",
        'The local speaks candidly because Rafael represents the named company. Keep the sole reason and the residents’ hostility; the introductory clause leaves the company’s native abbreviation inside the sentence.'),
    'DK4_MES_B154_R0114':("I've heard about FO before. At least you wouldn't mistreat the people here, would you?",
        'The local cites the company’s reputation in reply to Claudio’s warning, then tests a minimum expectation with a question. “Before” makes the already heard reputation explicit in idiomatic speech and keeps the native abbreviation away from the sentence stop.'),
}

if __name__=='__main__':
    logical_out=LOGICAL.with_name(LOGICAL.name.replace('_v3','_v4'))
    formatting_out=FORMATTING.with_name(FORMATTING.name.replace('_v3','_v4'))
    preference_out=PREFERENCES.with_name(PREFERENCES.name.replace('_v10','_v11'))
    assert not any(p.exists() for p in [logical_out,formatting_out,preference_out,ROOT])
    logical,formatting,prefs,actual,stored=map(load,[LOGICAL,FORMATTING,PREFERENCES,ACTUAL,STORED])
    assert actual['all_complete_native_body_andheader_planes_andblank_guards_match']
    ids=set(REVISIONS);rows={r['id']:r for r in formatting['records']}
    assert {r['id'] for r in rows.values() if '{MACRO:FO}.' in r['english']}==ids
    assert sum(r['english'].count('{MACRO:FO}') for r in rows.values())==10
    stored_by_id={r['id']:r for r in stored['records']}
    findings=[]
    for ident,(text,reason) in REVISIONS.items():
        row=rows[ident];prior=next(r for r in logical['records'] if r['id']==ident)
        before=next(r for r in actual['body_pages'] if r['id']==ident)
        assert b'Castor Co..' in bytes.fromhex(stored_by_id[ident]['expanded_hex'])
        assert sha(Path(before['capture']['path']).read_bytes())==before['capture']['PNG_sha256']
        assert prior['english']==row['editorial_logical_English'] and prior['decision']==row['decision']=='revision'
        assert row['source_macros']==prior['source_macros'] and row['native_literal_token_counts']=={'FO':1}
        findings.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],
            clean_Japanese=row['source_Japanese'],previous_logical_English=prior['english'],revised_logical_English=text,
            retention_of_source_intent=reason,retired_capture=before['capture'],retired_native_plane_sha256=before['native_plane_sha256']))
        note=reason+' The former authored stop duplicated the full stop already in “Castor Co.” in actual gameplay. Preserve the exact FO token and speaker control.'
        marked=text.replace('FO','{MACRO:FO}');assert marked.count('{MACRO:FO}')==1
        assert row['planned_English_markup'].endswith(row['english'])
        row['planned_English_markup']=row['planned_English_markup'].removesuffix(row['english'])+marked
        row.update(english=marked,editorial_logical_English=text,finding=note,localization_note=note)
        prior.update(english=text,finding=note,localization_note=note)
    assert not any('Castor Co..' in r['english'].replace('{MACRO:FO}','Castor Co.') for r in formatting['records'])
    assert all(not r['review']['formatting'] for r in formatting['records'])
    for doc,parent,path in [(logical,LOGICAL,logical_out),(formatting,FORMATTING,formatting_out)]:
        doc.update(previous_punctuation_pass_manuscript=str(parent),previous_punctuation_pass_manuscript_sha256=sha(parent.read_bytes()),
            observed_runtime_punctuation_corrections=sorted(ids),all_other_records_exact=True,source_current_controls_macros_counts_anddecisions_unchanged=True,
            fresh_formatting_stored_andfocused_checks_pending_for_two_changed_rows=True,new_credit=0)
        save(path,doc)
    prefs.update(manuscript=str(formatting_out),manuscript_sha256=sha(formatting_out.read_bytes()),
        previous_preferences=str(PREFERENCES),previous_preferences_sha256=sha(PREFERENCES.read_bytes()),
        existing_source_bound_preferences_exact=True,no_preference_changes_for_revised_rows=True)
    save(preference_out,prefs)
    ROOT.mkdir(parents=True)
    save(ROOT/'observed_punctuation_andprose_revision.json',dict(findings=findings,all10_company_macros_checked=True,
        other8_retain_approved_wording_andnormal_punctuation=True,proposed_revisions=235,justified_retentions=322,
        new_credit=0,fresh_formatting_stored_andfocused_checks_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [LOGICAL,FORMATTING,PREFERENCES,ACTUAL,STORED,logical_out,formatting_out,preference_out,Path(__file__)]}))
    print('Two contextual revisions remove the live doubled period;555 other manuscript records, all controls and all decisions are unchanged.')
