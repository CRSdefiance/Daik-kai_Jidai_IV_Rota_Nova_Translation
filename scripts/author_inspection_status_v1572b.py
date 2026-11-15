"""Source/context and natural prose for the two original inspection status boxes."""
import struct
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.sea_responses_editorial import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/inspection_status_source_v1572')
OUT=Path('translations/inspection_status_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v1563_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    release=read('work/analysis/sea_responses_release_v1562/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    rom,clean,canonical=map(NdsImage.open,[ROM,Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds')])
    arm,original=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    common=rom.read_file('/COMMON/MESFILE.DK4')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original)
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    en=current_entries(common,arm)
    assert jp[306].text.decode('cp932')=='情報を見ることはできません！'
    assert jp[307].text.decode('cp932')=='見張りがいません'
    spans=[(0x6F5D4,0x6F680),(0x6F78C,0x6F7A4),(0x705F8,0x706A4),(0x8205C,0x820DC),
        (0x546B8,0x546F8),(0x54774,0x548A8),(0x53914,0x53AC0)]
    # Three registered inherited hooks are expected;restore only these for the clean comparison.
    from scripts.probe_common_display_name_hook import branch_link
    assert struct.unpack_from('<I',arm,0x54798)[0]==branch_link(0x02054798,0x01FFC828)
    literal=read(ROM.with_suffix('.manifest.json'))['relocations']['/__arm9__.bin']['common_literal_prefix']
    restored=bytearray(arm)
    for at,prefix in [(0x5397C,'F'),(0x53A44,'I')]:
        row=next(r for r in literal['changes'] if r['offset']==at)
        assert struct.unpack_from('<I',arm,at)[0]==row['after']
        assert struct.unpack_from('<I',original,at)[0]==row['before']
        restored[at:at+4]=original[at:at+4]
    restored[0x54798:0x5479C]=original[0x54798:0x5479C]
    assert all(restored[a:b]==original[a:b] for a,b in spans)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata=True
    source=[{'span':[0x2000000+a,0x2000000+b],'sha256':sha(original[a:b]),'current_with_three_registered_inherited_hooks_sha256':sha(arm[a:b]),
        'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[a:b],0x2000000+a)]} for a,b in spans]
    neighbors=[{'message_ID':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
        'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
        'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),
        'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'}} for n in range(303,310)]
    context=('Original Info Mode inspection6F4D4 calls546B8 with307 at6F604/6F608 when an unidentified target is selected and the original lookout-state condition is unsatisfied. If the active lookout condition yields7,the alternative306 is selected at6F5F8/6F5FC. Identified creature/ghost targets execute the independent role7 fear/awe response at6F66C/6F674,then306 at6F678/6F67C. These two messages are speakerless system status boxes,not shop dialogue or trade-good descriptions.306 says information cannot be viewed;307 says no lookout is present. Neither source supplies printf arguments,speech macros,presentation prefixes or a follow-up sentence to concatenate. The original546B8 loader and54774 varargs formatting lead through the registered modal wrapper and53914 macro expander with its existing literal F/I guards. The initial1572 clean-code assertion correctly caught these three inherited hooks;1572b verifies their registry/manifest provenance,then restores only those words for the exact clean-span comparison. No existing hook is removed or changed. New prose fits one native35-cell line,so no wrap/layout code or hand-positioned breaks are needed. Retain all other messages,including the separately unreviewed fatigue308,exactly.')
    ROOT.mkdir(parents=True);packet=ROOT/'source_and_original_modal_context.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'records_and_neighbors':neighbors,'original_code':source,
        'context':context,'actual_no_lookout_proof':'work/analysis/sea_registration_pilot_verified_v1552j/original_registration_and_no_lookout_verified.json',
        'actual_following306_proof':'work/analysis/sea_inspection_verified_v1568b/original_inspection_complete_pixels_and_transition.json',
        'source_308_fatigue_suffix_is_separate_unreviewed_lead':True,'no_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    prose={306:("You can't view that information!",'Information cannot be viewed;the emphatic system message denies this inspection.',
        'Use a direct,natural American English system message and retain the emphatic exclamation. No claim that information was lost,trade goods are being described or a new feature is unlocked.'),
        307:("No lookout is assigned.",'There is no lookout present for the inspection.',
        'State the missing assignment naturally in the crew-station context established by the original predicate and actual empty lookout3. Do not confuse the speech fallback actor with an occupied lookout station.')}
    rows=[]
    for n,(english,meaning,note) in prose.items():
        neighbor=next(r for r in neighbors if r['message_ID']==n)
        assert len(english)<=35 and english==' '.join(english.split()) and b'%' not in jp[n].text
        rows.append({**neighbor,'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':'inspection-status-system2',
            'speaker':'Speakerless original system modal546B8','context':context,'consumer':'original546B8-loader-54774-varargs-53914-macro-system-modal',
            'english':english,'source_meaning':meaning,'localization_note':note,'editorial_decision':'revise',
            'canonical_source_hex':base[n].text.hex(),'native_argument_count':0,'source_native_macros':[],
            'compiled_hex':english.encode('ascii').hex(),'authored_as_one_unwrapped_paragraph':True,
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-context-naturalness-reviewed;native-font-release-actual-modal-pending'})
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'inspection-status-original-single-line-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),
        'source_context':str(packet),'source_context_sha256':sha(packet.read_bytes()),'records':rows,'revised':2,'retained':0,
        'no_authored_line_breaks_or_alignment':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(OUT,doc)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not {306,307}&(done|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    assert ledger['records_with_source_and_prose_pass']==1490
    ledger['records_with_source_and_prose_pass']+=2
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=2
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],306,307])
    ledger['coverage_units'].append({'id':'Shared-inspection-status2-source-prose','native_message_IDs':[306,307],'status':'source-context-prose-reviewed;native-release-actual-pending','manuscript':str(OUT),'source_context':str(packet)})
    ledger['active_source_prose_drafts']['native_message_IDs']=sorted(set(ledger['active_source_prose_drafts']['native_message_IDs'])|{306,307})
    ledger['active_source_prose_drafts']['manuscripts'].append(str(OUT))
    ledger['formatting_watchlist']['inspection_status2']={'native_message_IDs':[306,307],'manuscript':str(OUT),'source_context':str(packet),
        'native_font_release_actual_followup_and_no_lookout_pending':True}
    ledger['research_checkpoints'].append({'id':'V1572-inspection-status2-source-prose','manuscript':str(OUT),'proof':str(packet),'source_prose_reviews_added':2,'completed_entries_added':0,'full_goal_complete':False})
    assert ledger['records_editorially_completed']==1338 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==154
    save(ledger_path,ledger)
    Path('docs/inspection_status_v1572_source_review.md').write_text('# V1572 inspection status source review\n\n'+context+'\n\n306: '+rows[0]['english']+'\n\n307: '+rows[1]['english']+'\n\n1338 complete;1492 source/prose reviewed;154 reviewed-incomplete COMMON. Native,release and actual modal verification pending;full goal active.\n',encoding='utf-8')
    print('Source/context and natural prose2 reviewed;1338 complete/1492 source-prose/154 pending.Native fonts/release/actual paths next.')
