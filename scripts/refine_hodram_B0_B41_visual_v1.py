"""Preserve the initial389-page review and source-bound follow-up changes."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OLD=Path('translations/hodram_B0_B41_contextual_review_v2.json')
NEW=Path('translations/hodram_B0_B41_contextual_review_v3.json')

def main():
    assert not NEW.exists()
    prose=load(OLD); original=deepcopy(prose)
    ident='DK4_MES_B3_R0006'
    row=next(r for r in prose['records'] if r['id']==ident)
    assert row['source_Japanese']=="あれを見な！\nあの艦隊こそ、アタシらの縄張りを\n荒らしている\nFOだ！"
    assert row['english']=="Look there! That's {MACRO:FO}'s fleet, the ones who've been muscling in on our waters!"
    english="Look there! That's {MACRO:FO}, the fleet that's been muscling in on our waters!"
    finding=("The native FO sample expands to Bergstrom Fleet. The draft adds a redundant possessive fleet. "
             "Japanese identifies the encroaching fleet as FO; use an appositive that remains natural with the full faction label. "
             "Aziza's confident colloquial voice and the original one FO substitution remain.")
    for key in ['english','logical_English']: row[key]=english
    for key in ['editorial_finding','localization_note']: row[key]=finding
    row['source_meaning']='Aziza identifies the encroaching fleet as FO, not as a second fleet belonging to FO.'
    row['visual_substitution_followup']=dict(previous_English=next(r for r in original['records'] if r['id']==ident)['english'],
        observed_sheet=str(ROOT/'body_contact_sheets_v1/sheets/sheet_1.png'),finding=finding)
    assert all(a==b for a,b in zip(original['records'],prose['records']) if a['id']!=ident)
    prose.update(previous_contextual_manuscript=str(OLD),previous_contextual_manuscript_sha256=sha(OLD.read_bytes()),
        visual_followup_changed_prose_ids=[ident],other393_decisions_exact=True,
        all32_tutorial_editorial_decisions_unchanged=True,only_one_English_city_spelling_refined=False)
    save(NEW,prose)
    old_input=ROOT/'formatting_v1/formatting_input_v2.json'; doc=load(old_input)
    target=next(r for r in doc['records'] if r['id']==ident)
    for key in ['english','logical_English','editorial_logical_English']: target[key]=english
    for key in ['source_meaning','editorial_finding','localization_note','visual_substitution_followup']: target[key]=deepcopy(row[key])
    target['planned_English_markup']='{SPEAKER:1B}'+english
    doc.update(source_full_manuscript=str(NEW),source_full_manuscript_sha256=sha(NEW.read_bytes()),
        previous_formatting_input=str(old_input),previous_formatting_input_sha256=sha(old_input.read_bytes()),
        no_editorial_wording_or_decision_changes=False,visual_followup_changed_prose_ids=[ident])
    save(ROOT/'formatting_v1/formatting_input_v3.json',doc)
    prefs=load(ROOT/'formatting_v1/preferences_v3.json'); rows={r['id']:r for r in doc['records']}
    changes={
        'DK4_MES_B17_R0236':dict(required_pairs=[['like','him']],reason='Keep the father comparison like him together; the initial sheet10 splits its object from like.'),
        'DK4_MES_B29_R0074':dict(page_clause='Then bring our broadside to bear and finish them with a volley!',reason='Initial sheet14 strands them with a volley on page2. Keep the complete closing tactical instruction on one page without changing prose.'),
        'DK4_MES_B30_R0013':dict(required_pairs=[['the','man']],reason='Keep the short noun phrase the man together, rather than ending the opening line on its article.'),
        'SC1_B30_STYLE_662_100':dict(required_pairs=[["shouldn't",'we']],reason='Keep the opening of the retreat question together; the initial sheet15 separates its auxiliary and subject.'),
        'DK4_MES_B32_R0055':dict(required_pairs=[['all','hands']],reason='Keep the established battle command All hands together; sheet16 splits it across rows.'),
    }
    for key,change in changes.items():
        change['bindings']={k:sha(rows[key][k].encode('utf-8')) for k in ['source_hex','current_hex','english']}
        prefs['records'][key]=change
    previous=ROOT/'formatting_v1/preferences_v3.json'
    prefs.update(previous_preferences=str(previous),previous_preferences_sha256=sha(previous.read_bytes()))
    save(ROOT/'formatting_v1/preferences_v4.json',prefs)
    manifest=ROOT/'body_contact_sheets_v1/contact_manifest.json'
    save(ROOT/'body_initial_visual_review_v1.json',dict(contact_manifest=str(manifest),contact_manifest_sha256=sha(manifest.read_bytes()),
        sheets=[dict(path=str(p),sha256=sha(p.read_bytes()),directly_viewed=True) for p in sorted((ROOT/'body_contact_sheets_v1/sheets').glob('sheet_*.png'))],
        all389_initial_pages_directly_viewed=True,view_mode='one readable native2x sheet per tool call',
        followup_layout_preferences=changes,prose_followup=ident,unchanged_pages_retain_readable_native_layout=True,
        retention_reason='Complete phrases and glyphs fit the validated width. Short reports, deliberate pauses, source-defined poem utterances, anonymous labels and opaque cries retain their distinct source intent.',
        intentional_empty_source_record='DK4_MES_B15_R0080',
        tutorial_FE_B29_R0112='Four complete rows with no inserted blank; directly viewed on sheet14.',
        revised_pages_require_fresh_native_and_direct_visual_review=True,actual_gameplay=False,new_credit=0))
    print('Saved389-page initial visual review, five scoped wrap preferences and one full-FO prose correction. No new credit.')

if __name__=='__main__':main()
