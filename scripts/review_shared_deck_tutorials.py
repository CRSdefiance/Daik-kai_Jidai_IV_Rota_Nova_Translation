"""Review all four complete clean Deck panels and preserve the earlier one-panel draft."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.probe_deck_explanation_sources import ROWS

ROOT=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104')
PRIOR=Path('translations/deck_explanations_manuscript_v1.json')
RELEASE=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')
TUTORIAL=Path('translations/rafael_B42_B43_contextual_final_review_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0);clean_path=Path('work/clean.nds')
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=NdsImage.open(clean_path).read_file('/__arm9__.bin');original=load(PRIOR)
    tutorial={r['id']:r for r in load(TUTORIAL)['records']}
    assert 'people like us' in tutorial['DK4_MES_B43_R0007']['english'] and 'First Mate' in tutorial['DK4_MES_B43_R0030']['english']
    notes={
        'LOOKOUT':('Having a lookout makes towns and similar places easier to discover while at sea.',
            'Retain the natural complete explanation. It preserves the lookout condition,greater ease of discovery,towns andother locations,andthe at-sea setting without promising automatic discovery.'),
        'CAPTAIN':('Having a ship captain makes sailor fatigue rise less readily.',
            'Retain the concise source-faithful wording. Slows the rise expresses the rate effect without claiming fatigue decreases. Sailor remains distinct from the named navigators;captain names the ship assignment,not a newly invented personal rank.'),
        'ADJUTANT':('Having a first mate enables sending negotiation documents at the guild.',
            'Use the established First Mate assignment name,matching the visible selector andJulio tutorial. Retain the existing lets-you-send sentence andguild/document facts;A First Mate parallels A lookout andA captain in the adjacent complete panels. This replaces the earlier equally faithful With-clause draft through justified retention of wording that already works,with no omitted meaning.'),
        'OARS':('This is the room where sailors row the oars;the named navigators cannot be assigned here.',
            'Retain both complete sentences andthe assignment prohibition. Source 航海士 denotes the named companions here,contrasted with 水夫;same class isexplicitly explained as navigators--people like us in Julio’s reviewed tutorial. Keep current cross-screen terminology rather than invent an officer rank ormistake this for a restriction on just the navigation-duty role.')}
    records=[]
    for room,source_offset,field,label,_,_ in ROWS:
        old=next(r for r in original['records'] if r['id']=='DECK_EXPLANATION_'+label)
        assert clean[source_offset:source_offset+old['capacity']]==bytes.fromhex(old['source_hex'])
        assert struct.unpack_from('<I',clean,field)[0]==BASE+source_offset
        pointer=struct.unpack_from('<I',ctx.arm,field)[0];at=pointer-BASE
        raw=ctx.arm[at:ctx.arm.index(0,at)];paragraph=' '.join(raw.decode('cp932').split())
        assert paragraph==old['english'].removesuffix('{PAD}')
        row=deepcopy(old);meaning,note=notes[label]
        english='A First Mate lets you send negotiation documents from the guild.' if label=='ADJUTANT' else paragraph
        row.update(file_path='/__arm9__.bin',english=english+'{PAD}',source_meaning=meaning,localization_note=note,
            context='Complete shared Deck tooltip,reviewed with all four special Deck panels andJulio’s source-defined companion/assignment tutorial. These independent panels are not a fabricated conversation.',
            source_reference=dict(file_path='/__arm9__.bin',offset=source_offset,capacity=old['capacity'],pointer_field=field,room=room),
            current_reference=dict(file_path='/__arm9__.bin',offset=at,pointer_field=field,pointer=pointer,length=len(raw)),
            current_hex=raw.hex(),current_stored_text=raw.decode('cp932'),current_comparison_paragraph=paragraph,
            decision='revision' if label=='ADJUTANT' else 'retention',finding='Align adjutant with visible First Mate assignment.' if label=='ADJUTANT' else 'Existing wording preserves the complete source function andreads naturally.',
            retention_reason='' if label=='ADJUTANT' else note,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        records.append(row)
    ROOT.mkdir()
    save(ROOT/'four_panel_contextual_review_v1.json',dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-fixed-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=records,proposed_revisions=1,wording_retentions=3,
        all_four_prose_gates_pass=True,all_formatting_gates_false=True,current_wording_previously_known=True,
        earlier_First_Mate_With_clause_draft_preserved='work/analysis/First_Mate_shared_tutorial_20261104/contextual_tooltip_review_v1.json',
        duplicate_pending_First_Mate_record_must_not_receive_second_credit=True,runtime=ctx.receipt(),no_ROM_modified=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,TUTORIAL,RELEASE,STARTUP,Path(__file__)]}))
    print('Four complete shared Deck panels reviewed:one First Mate terminology revision,three justified retentions;formatting/integration pending.')
