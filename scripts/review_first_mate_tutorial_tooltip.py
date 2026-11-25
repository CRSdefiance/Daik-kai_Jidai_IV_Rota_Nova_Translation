"""Review the queued shared tutorial terminology against the complete clean panel."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.crew_role_labels import BASE,FIELD,ENGLISH,LABELS,JAPANESE
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.probe_deck_explanation_sources import ROWS

ROOT=Path('work/analysis/First_Mate_shared_tutorial_20261104')
RELEASE=Path('work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json')
STARTUP=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')
PRIOR=Path('translations/deck_explanations_manuscript_v1.json')
TUTORIAL=Path('translations/rafael_B42_B43_contextual_final_review_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0)
    clean_path=Path('work/clean.nds')
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=NdsImage.open(clean_path).read_file('/__arm9__.bin')
    old=next(r for r in load(PRIOR)['records'] if r['id']=='DECK_EXPLANATION_ADJUTANT')
    room,source_offset,field,_,_,_=next(r for r in ROWS if r[3]=='ADJUTANT')
    assert source_offset==old['offset'] and clean[source_offset:source_offset+old['capacity']]==bytes.fromhex(old['source_hex'])
    assert struct.unpack_from('<I',clean,field)[0]==BASE+source_offset
    pointer=struct.unpack_from('<I',ctx.arm,field)[0]
    offset=pointer-BASE
    current=ctx.arm[offset:ctx.arm.index(0,offset)]
    paragraph=' '.join(current.decode('cp932').split())
    assert paragraph==old['english'].removesuffix('{PAD}')
    assert struct.unpack_from('<I',ctx.arm,FIELD)[0]==ENGLISH
    role_pointer=struct.unpack_from('<I',ctx.raw,ENGLISH-BASE+4)[0]
    role_at=role_pointer-BASE;role=ctx.raw[role_at:ctx.raw.index(0,role_at)].decode('ascii').strip()
    assert role==LABELS[1]=='First Mate' and JAPANESE[1]=='副官'
    tutorial=next(r for r in load(TUTORIAL)['records'] if r['id']=='DK4_MES_B43_R0030')
    assert 'First Mate' in tutorial['english'] and all(tutorial['review'].values())
    record=deepcopy(old)
    record.update(file_path='/__arm9__.bin',
        source_reference=dict(file_path='/__arm9__.bin',offset=source_offset,capacity=old['capacity'],pointer_field=field,room=room),
        current_reference=dict(file_path='/__arm9__.bin',offset=offset,pointer_field=field,pointer=pointer,length=len(current)),
        current_hex=current.hex(),current_stored_text=current.decode('cp932'),current_comparison_paragraph=paragraph,
        english='With a First Mate, you can send negotiation documents from the guild.{PAD}',
        source_meaning='If a first mate is present, sending negotiation documents can be performed at the guild.',
        context='Complete shared Deck explanation for the First Mate assignment; compare the visible duty selector and Julio\'s complete duties explanation, not an isolated dictionary equivalent.',
        localization_note='Replace adjutant with the established visible First Mate role so tutorial terminology agrees with the screen. Retain the source-enabled action, negotiation documents and guild location. The natural With clause changes no condition or capability. No new rank is invented: this is the same source 副官 assignment already localized in the role selector. Existing historical wording and evidence remain unchanged.',
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
        finding='Shared tooltip says adjutant while the role selector and Julio tutorial say First Mate.',
        retained_elements_reason='The existing explanation correctly preserves the enabled action, document type and guild location; keep those facts.',
        remaining_display_checks=['Consumer-specific paragraph formatting','Complete native panel glyphs/bounds/allocation','Representative Deck panel observation','Registered owned static-data integration'],
        no_new_glyph_orformatting_oractual_gameplay_approval=True)
    ROOT.mkdir()
    save(ROOT/'contextual_tooltip_review_v1.json',dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-fixed-v1',review_gates=['source','context','localization','naturalness','formatting'],
        records=[record],proposed_revisions=1,wording_retentions=0,formatting_andintegration_pending=True,
        current_wording_was_already_known_from_prior_queued_finding=True,no_claim_of_English_unconsulted_intake=True,
        runtime=ctx.receipt(),visible_role=dict(source=JAPANESE[1],current=role,pointer=role_pointer),
        related_complete_tutorial=dict(path=str(TUTORIAL),id=tutorial['id'],english=tutorial['english']),
        no_ROM_modified=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,TUTORIAL,RELEASE,STARTUP,Path(__file__)]}))
    print('Complete clean First Mate panel andcurrent role bound;one contextual terminology revision saved,display/integration pending.')
