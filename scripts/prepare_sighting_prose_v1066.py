"""Review both bearing/faction sighting families; native and actual gates stay open."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reinforcement_sniping_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_editorial_v1066')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
SOURCE=Path('work/analysis/sighting_editorial_v1065/source_context_packet.json')
TEXT={
614:"Fleet spotted in the %s! It belongs to %s. Battle stations!",
615:"Spotted a fleet in the %s! It's from %s! Battle stations!",
616:"There's a fleet in the %s! It's from %s! Get ready for battle!",
617:"There's a fleet in the %s! It's from %s! Battle stations!",
618:"We've got company in the %s! A fleet from %s! Battle stations!",
619:"Spotted a fleet in the %s! It's from %s! Battle stations!",
620:"I found a fleet in the %s! It's from %s! Time to fight!",
621:"Fleet spotted in the %s! It belongs to %s! Battle stations!",
622:"Fleet spotted in the %s! It's from %s, and they're attacking us!",
623:"There's a fleet in the %s! It's from %s, and they're attacking us!",
624:"Look! A fleet in the %s! It's from %s, and they're attacking us!",
625:"Fleet in the %s! It's from %s, and they've picked a fight with us!",
626:"A fleet in the %s! It's from %s, and they've launched an attack!",
627:"Whoa! We're under attack from the %s! It's a fleet from %s!",
628:"A fleet in the %s! It's from %s, and they've launched an attack!"}
GLOSS={
614:'Politely reports spotting the named factions fleet at the relative bearing,then announces battle readiness.',
615:'Directly reports spotting the named factions fleet at the relative bearing,then announces battle readiness.',
616:'Casually says the named factions fleet is at the relative bearing,then announces getting ready for battle.',
617:'A feminine voice reports the named factions fleet at the relative bearing,then announces battle readiness.',
618:'Roughly and disparagingly says the named factions fleet is at the relative bearing,then announces battle readiness.',
619:'An older voice reports spotting the named factions fleet at the relative bearing,then announces battle readiness.',
620:'Excited youthful voice says they found the named factions fleet at the relative bearing,and calls out that it is battle time.',
621:'Politely emphatic older voice reports spotting the named factions fleet at the relative bearing,then announces battle readiness.',
622:'Reports spotting the named factions fleet at the relative bearing,and that it has launched an attack.',
623:'Casually reports spotting the named factions fleet at the relative bearing,and that it is attacking us.',
624:'Exclaims on seeing the named factions fleet at the relative bearing,and reports that it is attacking us.',
625:'Roughly reports spotting the named factions fleet at the relative bearing,and complains that it has attacked us.',
626:'An older voice identifies the named factions fleet at the relative bearing,and reports that it has launched an attack.',
627:'A startled youthful voice reports that the named factions fleet is attacking from the relative bearing.',
628:'A politely emphatic older voice identifies the named factions fleet at the relative bearing,and reports that it has launched an attack.'}
BASE=0x02000000


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    assert not set(TEXT)&set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    context=read(SOURCE);assert len(context['all208_original_actor_voice_selections'])==208
    assert sha(ROM.read_bytes())==context['candidate_sha256']
    rom,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    arm,clean_arm=[r.read_file('/__arm9__.bin') for r in (rom,clean)]
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean_arm)
    current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    raw=Path(context['source_snapshot']).read_bytes();assert sha(raw)==context['source_snapshot_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);hero=get(0x7F244)
    attacked_table=0x02118540;ids=(622,-1,623,624,625,626,627,628)
    assert struct.unpack_from('<8i',arm,attacked_table-BASE)==ids
    assert arm[attacked_table-BASE:attacked_table-BASE+32]==clean_arm[attacked_table-BASE:attacked_table-BASE+32]
    attacked=[]
    for actor in range(208):
        obj=actors+0x19E4 if actor==hero else actors+4+actor*32
        voice=get(0x7E988,obj);number=get(0x53F4C,obj,attacked_table)
        assert number==(622 if ids[voice]==-1 else ids[voice])
        attacked.append({'actor_ID':actor,'original_voice_class':voice,'message_ID':number})
    callers=[]
    for at in range(0,len(arm)-3,4):
        word=struct.unpack_from('<I',arm,at)[0]
        if word>>24!=0xEB:continue
        displacement=word&0xFFFFFF
        if displacement&0x800000:displacement-=1<<24
        if at+8+displacement*4==0x6567C:callers.append(BASE+at)
    assert callers==[0x020778A8,0x02077B9C]
    close=context['original_bearing_getter_cases'][0];at=close['argument_address']-BASE
    assert arm[at:at+9]==bytes.fromhex(close['hex'])+b'\0'
    assert len(b'vicinity\0')==9
    ROOT.mkdir(parents=True)
    supplement=ROOT/'attacked_family_and_provider_supplement.json'
    save(supplement,{'source_context':str(SOURCE),'source_context_sha256':sha(SOURCE.read_bytes()),
        'attacked_table':attacked_table,'source_voice_IDs':list(ids),'all208_original_attacked_voice_selections':attacked,
        'direct_ARM9_bearing_calls':callers,'direct_scan_does_not_claim_complete_indirect_or_overlay_coverage':True,
        'close_range_provider':{**close,'source_allocation_including_NUL_bytes':9,'proposed_English':'vicinity',
            'proposed_hex':b'vicinity\0'.hex(),'reason':'in the vicinity preserves the original very-close-range meaning and remains grammatical alongside in the N/NE/etc. The new prose must never ship while this argument remains Japanese.',
            'integration_and_all_provider_users_verification_pending':True},
        'preparing_and_already_attacked_families_have_different_meanings':True,
        'no_ROM_or_live_state_change':True,'no_editorial_completion_credit':True})
    records=[]
    for n,text in TEXT.items():
        assert text.count('%s')==2 and '\n' not in text and '  ' not in text
        family='fleet-sighting-battle-preparation' if n<622 else 'fleet-sighting-under-attack'
        voice_ids=list(range(614,622)) if n<622 else list(ids)
        voices=[v for v,i in enumerate(voice_ids) if (voice_ids[0] if i==-1 else i)==n]
        note=('Express the sighting as a spoken report,retaining its two original argument positions:relative bearing first,complete faction label second. In the N/NW/etc uses ordinary nautical compass abbreviations;in the vicinity requires the separately tracked faithful close-range provider repair. Never add an admiral address,kinship,or new hostility fact. ')
        note+=('Keep preparation for combat;do not turn this report into a claim that the opponent has already attacked.' if n<622 else 'Keep the opponents initiated attack;do not replace it with a mere battle-readiness call.')
        if n==618:note+=' We have got company conveys the rough unwelcome-fleet reaction without adding profanity.'
        if n==625:note+=' Picked a fight conveys the disparaging complaint about the opponents initiated attack.'
        if n in (620,627):note+=' Keep the youthful excitement/startle in full natural sentences.'
        records.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':family,
            'consumer':'native-speech-announcement','speaker':'Player First Mate or original native fallback;voice classes '+','.join(map(str,voices)),
            'source_speaker_role':1,'source_voice_classes_including_native_fallback':voices,
            'context':'Original first-sighting flow775E8/778D0/77DDC supplies relative bearing then complete faction label. These are independent voice alternatives,not consecutive dialogue. Preparation precedes reinforcement/battle entry;under-attack variants report the opponents actual initiative. Preserve original scan/seen flags/relations/captain identities. See exact original source fragments and adjacent message families.',
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'canonical_source_hex':accepted[n].text.hex(),'current_reference':reference(current[n]),
            'current_text_hex':current[n].text.hex(),'current_English':current[n].text.decode('cp932'),
            'source_meaning':GLOSS[n],'english':text,'localization_note':note,'editorial_decision':'revise',
            'native_argument_count':2,'native_argument_kinds':['relative-bearing-label','complete-faction-label'],
            'source_native_macros':[],'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'sighting-post-expansion-native-review-pending',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'15-source-context-prose-reviewed-native-provider-layout-release-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'native_context_proof':str(SOURCE),'native_context_proof_sha256':sha(SOURCE.read_bytes()),
        'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':records})
    save(ROOT/'editorial_ledger_before_prose.json',ledger)
    ledger['records_with_source_and_prose_pass']+=15;ledger['records_with_source_prose_drafts']+=15
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=15
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(set(ledger['reviewed_but_incomplete_COMMON_IDs'])|set(TEXT))
    ledger['active_source_prose_drafts']['native_message_IDs']=ledger['reviewed_but_incomplete_COMMON_IDs'][:]
    ledger['active_source_prose_drafts']['manuscripts'].append(str(MANUSCRIPT))
    ledger['active_source_prose_drafts']['status']='three-older-context-pending;20-reinforcement-shot-actual-pending;15-sighting-provider-native-release-actual-pending'
    ledger['newly_observed_sighting_followup'].update(native_message_IDs=list(TEXT),status='source-context-and-natural-English-drafts-reviewed;native-provider-layout-release-actual-pending',
        source_context=str(SOURCE),supplement=str(supplement),manuscript=str(MANUSCRIPT),source_prose_reviews_added=15,completed_entries_added=0,
        close_range_Japanese_provider_remains_open=True)
    checkpoint='V1066 source/prose-reviews15 original fleet-sighting variants614-628. All416 native actor selections across two tables and nine actual bearing-getter cases bind preparation versus already-attacked meanings. Full natural-English sentences replace At NW fragments and preserve direction/faction argument order and voice. The current close-range argument still contains Japanese 至近距離;an exact-nine-byte vicinity provider draft is recorded but not integrated. Complete provider-user coverage,native expansion/wrap/font,registered integration and actual scenes remain pending.1196 entries complete,1234 source/prose reviewed. V997 remains current fully scene-verified;V1034 still awaits the successful-shot actual event. Full shared/routes/player-prose/raw coverage and separate graphics audit remain open.'
    ledger['sighting_v1066']={'native_message_IDs':list(TEXT),'source_prose_reviews_added':15,'completed_entries_added':0,
        'manuscript':str(MANUSCRIPT),'source_context':str(SOURCE),'supplement':str(supplement)}
    ledger['latest_checkpoint']=checkpoint
    save(ledger_path,ledger)
    for name in ('docs/translation_progress.md','docs/todo.md'):
        with Path(name).open('a',encoding='utf-8') as f:f.write('\n\n## V1066: sighting dialogue source and prose review\n\n'+checkpoint+'\n')
    Path('docs/sighting_v1066_source_review.md').write_text('# V1066: fleet-sighting editorial review\n\n'+checkpoint+'\n\nThe close-range provider is a genuine runtime argument,not text inferred from an image. Its original9-byte NUL-terminated allocation can hold vicinity exactly. No provider bytes,dialogue bytes,ROM,patch,seen flags,RNG or outcome were changed in this checkpoint. All15 formatting gates remain false. Direct ARM9 bearing-call discovery is bounded evidence;other code/indirect/overlay consumers still need classification before provider integration.\n',encoding='utf8')
    print('15 source/prose reviews added;1196 complete,1234 source/prose. Native/provider/gameplay gates remain open.',flush=True)


if __name__=='__main__':main()
