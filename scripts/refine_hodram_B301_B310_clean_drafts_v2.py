"""Refine source-first diction and one directional gloss before any current-story comparison."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B301_B310_clean_v1 import ROOT,OUT as PREVIOUS_MEANINGS
from scripts.draft_hodram_B301_B310_clean_v1 import OUT as PREVIOUS_DRAFTS

MEANINGS=ROOT/'all234_clean_meanings_before_English_v2.json'
OUT=Path('translations/hodram_B301_B310_clean_drafts_v2.json')

def main():
    assert not MEANINGS.exists() and not OUT.exists()
    meanings=deepcopy(load(PREVIOUS_MEANINGS));drafts=deepcopy(load(PREVIOUS_DRAFTS))
    assert meanings['records_count']==drafts['records_count']==234 and drafts['current_English_comparisons']==0
    target=next(r for r in meanings['records'] if r['block']==308 and r.get('source_style_indices')==[2])
    assert 'northeastern-China village' in target['source_meaning']
    corrected=target['source_meaning'].replace('northeastern-China village','village far northeast of China')
    target['source_meaning']=corrected
    target['personality_voice_notes'][0]['register']=corrected
    meanings.update(previous_meanings=str(PREVIOUS_MEANINGS),previous_meanings_sha256=digest(PREVIOUS_MEANINGS),
        one_source_direction_gloss_clarified_not_northeastern_China=True,
        refinement_before_eligible_current_English=True)
    save(MEANINGS,meanings)
    rows={r['id']:r for r in drafts['records']};findings=[]
    def revise(row,text,reason):
        before=row['english'];assert before!=text
        row['english']=text;row['localization_note']+=' '+reason
        findings.append(dict(id=row['id'],source_reference=row['source_reference'],before=before,after=text,reason=reason))
    revise(rows['DK4_MES_B303_R0012'],'Let me give you a tip to say thanks.',
        'Make Safia’s friendly thanks a natural spoken offer without adding a specific prior lesson or relationship.')
    revise(rows['DK4_MES_B304_R0129'],'That should have been quite a shortcut.',
        'A considerable shortcut reduces the journey; it does not save the entire journey from occurring.')
    def style(b,c,i):return next(r for r in drafts['records'] if r['block']==b and r.get('source_command_offset')==c and i in r.get('source_style_indices',[]))
    revise(style(302,392,4),"It's so hot out here!",'Keep the rough, emphatic heat complaint without adding profanity absent from this source alternative.')
    revise(style(302,596,4),"That's one fierce sandstorm. We could get lost in it... Still going?",
        'Keep the blunt warning/question without an added expletive.')
    for row in drafts['records']:
        if row['block']!=309 or row.get('source_command_offset')!=2364:continue
        i=row['source_style_indices'][0]
        suffix={0:'We should be safe here.',2:'Are we safe here now?',3:"We should be safe here now, shouldn't we?",
            4:"We're safe here now, right?",5:"W-we're safe now...",6:"We've run far enough to be safe, right?",7:'We should be safe here now.'}[i]
        breath='Haah... Haah... Haah...' if i==5 else ('Hah... Hah...' if i==6 else 'Hah... Hah... Hah...')
        revise(row,breath+' '+suffix,'Represent the source’s breathless panting as nonlexical breaths, preserving the tentative safety statement; do not make Wheeze a spoken stage direction or a laugh.')
    rows[target['id']]['source_meaning']=corrected
    rows[target['id']]['personality_voice_notes']=deepcopy(target['personality_voice_notes'])
    rows[target['id']]['localization_note']=rows[target['id']]['localization_note'].replace('northeastern-China village','village far northeast of China')
    assert len(findings)==11
    drafts.update(source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        previous_drafts=str(PREVIOUS_DRAFTS),previous_drafts_sha256=digest(PREVIOUS_DRAFTS),
        source_first_refined_records=11,all234_logical_drafts_written_before_current_ROM_story_English_intake=True)
    save(OUT,drafts)
    save(ROOT/'source_first_refinement_v2.json',dict(findings=findings,prose_refinements=11,
        directional_gloss_record=target['id'],directional_gloss_meaning=corrected,
        all_source_bytes_preambles_aliases_runtime_macros_andcontexts_preserved=True,
        eligible_current_story_English_still_unconsulted=True,
        evidence={str(p):digest(p) for p in [PREVIOUS_MEANINGS,PREVIOUS_DRAFTS,MEANINGS,OUT,Path(__file__)]},new_credit=0))
    print('Refined11 logical drafts and one direction gloss; all234 remain source-first and uncredited.')

if __name__=='__main__':main()
