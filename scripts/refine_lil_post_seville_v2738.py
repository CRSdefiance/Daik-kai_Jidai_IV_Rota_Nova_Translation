"""Resolve four visual phrase-flow findings with natural unwrapped prose."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_post_seville_profile import profile_for
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.qa import audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_phrase_review_v2738')
OLD=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v2.json')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v3.json')
CHANGES={
    'DK4_MES_B31_R0059':('Is this what that warning meant...?',
        'The earlier about-only final row is resolved by the more direct recalled question what that warning meant. English does not need quotation marks around a remembered warning. Meaning,uncertainty andB132attribution are unchanged;no manual break orlayout waiver is added.'),
    'DK4_MES_B31_R0078':("The Pirate King...? S-scary, {MACRO:FI}. Let's just heed the warning.",
        'Use a natural frightened stammered fragment,then the complete cautious proposal. This preserves kowai/otonashiku/shitagau intent,the exact FI name address andJanus fear without the earlier isolated final predicate were warned. The native formatter places both complete utterances;there is no authored break orpredicate exemption.'),
    'DK4_MES_B132_R0034':("I've warned you, you hear me? Remember that!",
        'Use the equally natural completed warning,attention check andpositive Remember that directive for dont forget. This keeps the barkeeps force andavoids separating Dont from forget it. Ojisan remains first-person I with no invented kinship;no manual break orweak-ending waiver is added.'),
    'DK4_MES_B132_R0051':('Avoid the southern Mediterranean... What does that mean...?',
        'Avoid is a natural recollection ofthe injunction not to go there. Keep the full region andLil puzzled complete question. This removes the earlier subject/verb split What does / he mean while preserving uncertainty. No danger,person oroutcome is added andno manual layout control is authored.')
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');bs=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    previous=read('work/analysis/lil_post_Seville_fonts_v2737/current_macro_QA_and_progressive_font_proof.json');assert previous['manuscript_sha256']==sha(OLD.read_bytes())
    reports=[];notes=[];changes=[]
    for row in doc['records']:
        prior_reason=row.pop('qa_waiver_reason',None);row.pop('qa_waivers',None)
        if prior_reason:row['localization_note']=row['localization_note'].replace(' '+prior_reason,'')
        if row['id'] in CHANGES:
            value,reason=CHANGES[row['id']];before=row['english'];row['english']='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+value
            row['localization_note']+=' '+reason;changes.append(dict(id=row['id'],previous_english=before,english=row['english'],reason=reason))
        result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,bs[row['block']]))
        warning=[d.code for d in result.diagnostics if d.severity=='warning'];assert set(warning)<={'line-break-count'}
        if warning:
            reason='The ordinary Japanese physical wrapping is not a separate English dramatic pause. Full source meaning andspoken punctuation are retained in one logical paragraph;the calibrated formatter owns new pair-safe rows. Only the physical line-count difference is accepted. No overflow,orphan,predicate,weak-ending,control,missing-glyph orblank-page exemption is granted.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);row['localization_note']+=' '+reason
            notes.append(dict(id=row['id'],reason=reason))
        qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,bs[row['block']]))
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in row.get('qa_waivers',[])]
        reports.append(dict(id=row['id'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,qa=qa))
    assert len(changes)==4 and sum(a['english']!=b['english'] for a,b in zip(read(OLD)['records'],doc['records'],strict=True))==4
    ROOT.mkdir(parents=True);layout=ROOT/'all34_refined_layout_and_QA.json';save(layout,dict(records=reports,waivers=notes,failures=[],changed_paragraphs=changes,
        all5_predecessor_sheets_viewed=True,predecessor_current_native_proof='work/analysis/lil_post_Seville_fonts_v2737/current_macro_QA_and_progressive_font_proof.json',
        no_authored_breaks_or_new_layout_exemptions=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),layout_QA_proof=str(layout),no_English_or_source_control_change=False,
        phrase_flow_refinements=changes,status='source-prose-refined-layout-planned;four-current-native-font-updates-and-reference-release-pending')
    save(DOC,doc)
    save(ROOT/'refinement_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changed_paragraphs=4,unchanged_paragraphs=30,
        revised=22,retained=12,narrow_line_count_notes=len(notes),formatting_review_still_pending=True,no_ROM_registry_or_completion_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'4phrase-flow refinements;30paragraphs unchanged;{len(notes)}line-count-only notes. Current four-font/macro updates pending;no predicate waiver.')
