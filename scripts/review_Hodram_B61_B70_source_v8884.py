"""Record direct source/name views, linked-context findings and scoped retentions.

This records the completed clean-first review. It does not compare story English,
grant formatting/actual-scene/release approval, modify a ROM, or add credit.
"""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_source_review_v8884')
GLOSS=Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
CONTROL=Path('work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json')
NAMES=Path('work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json')
CLEAN_NAMES=Path('work/analysis/Hodram_B61_B70_clean_names_v8880/thirtytwo_clean_full_andprogressive_compositions_current_binding.json')
DISPLAY=Path('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
CONTEXT=Path('work/analysis/Hodram_B61_B70_clean_context_v8882/complete_clean_linked_38_44_context_before_B61_B70_English.json')
PATHS=Path('work/analysis/Hodram_B61_B70_source_paths_v8883/all224_source_memberships_original_branch_cases.json')
NAME_DOC=Path('translations/hodram_B61_B70_speaker_name_review_v1.json')

REASONS={
 1:'Retain approved Hodram Bergstrom and the approved Joakim middle component in its full consumer. FI uses the current captain given name, FA his surname. This is no new rank, historical-name, custom-name or catalogue-UI approval.',
 2:'Lil Argot is the approved proper name. Her sharp warning and later relieved, teasing welcome retain one identity; Argot is a surname, not a word to translate. The renewed working relationship with Camille does not establish a marriage or romance.',
 3:'Retain approved Maria Li in the short nameplate and Maria Huamei Li when the clean introduction supplies the full name. The clean native full getter actually composes Huamei. Li family/group wording does not license an invented personal relationship, crime organization or baptism story.',
 9:'Retain user-approved Camille Overijssel. The source itself uses the Camille nickname, including the port recognition and reunion. The native full getter also composes Marinus; that observed field is not a reason to rewrite his introductions or replace the approved name. Keep the separately documented nickname/true-name context distinct.',
 10:'Retain established Xien Yan for シエン・ヤン. This speaker courteously arranges a meeting with Maria; the name follows the source components and reads as a proper name. No new rank, kinship, nationality or historical identity follows from that role.',
 16:'Retain Gerhard Adernkatz, including the already validated complete surname and first glyph. The source selectors bind the same crew speaker here. The earlier registered surname correction remains intact; this batch does not reinterpret its spelling from scratch or add a title.',
 17:'Retain Al Shin for the source progressive アル・シン. The clean full getter separately composes フェリド, matching the current full Al Ferid Shin. Preserve those consumers rather than silently expanding every short label; the broader full-name/other-consumer review stays open.',
 18:'Retain Charles Rochefort for シャルル・ロシュフォール. Charles is a readable established Latin form of the source given name; Rochefort preserves the surname. Jean belongs to the distinct full getter. His conditional crew interjection does not add a military rank or family relation.',
 20:'Retain Fernando Dias for フェルナンド・ディアス. The current first F is stored full-width but the complete native visible name is intact. Preserve its qualified bytes and glyph behavior rather than normalize its storage merely for appearance. This supplies no global full-width-name rule.',
 23:'Retain Manuel Almeida for マヌエル・アルメイダ. The clean selectors preserve the established crew identity and his brief conditional farewell reaction. No new relationship or office is added from that reaction.',
 24:'Retain Sera Shahrbaraz for セラ・シャルバラーズ, with Altos confined to the separate full-name consumer. Her respectful learner speech and the farewell concern the same character. Do not turn language learning, trust or reunion hopes into an invented romance or family relationship.',
 38:'Retain established Zamorin Nagarpur for ザモリン・ナガルプル. Both source native name getters bind the components, including Ahmad only in the full getter. The boastful wealthy trader scene does not authorize treating the name component as a newly established royal rank or inventing a historical biography.',
 78:'Retain Sirwood Eme for シルウド・エメ as the established readable proper name. Sirwood is one name, not an English Sir title. Sera calls him a compatriot/companion from her country; no brother, father, husband or officer relationship is established.',
 105:'Retain Trader for 交易所の親父 in the gift exchange. This naturally identifies his trade-house function without translating familiar 親父 as Father, inventing kinship or asserting an age. Regional surname metadata is not composed by the original role-label getter.',
 116:'Retain Port Worker for 出港所の兄貴. The port warning uses rough familiar address, not actual brotherhood; the plain occupational label avoids inventing an official rank or age. Regional surname metadata remains separate from the actual label.',
 154:'Retain Sailor for this progressive speaker consumer: the original clean getter explicitly returns 水夫 for actor154. Its different full getter returns 配下, currently Retainer. Preserve both observed meanings; the Nagarpur entourage context does not justify replacing the source progressive label globally.'
}

if __name__=='__main__':
    assert not ROOT.exists() and not NAME_DOC.exists()
    gloss,controls,names,clean_names,display,context,paths=map(read,[GLOSS,CONTROL,NAMES,CLEAN_NAMES,DISPLAY,CONTEXT,PATHS])
    protected=[Path(p) for p in ['translations/editorial_review_current_v1.json','translations/release_stack.json',
        'scripts/build_integrated_release.py','out/all_routes_combined_v8865_candidate.nds',
        'out/all_routes_combined_v8865_candidate.xdelta','out/raphael_natural_v2_accepted_base.nds','work/clean.nds']]
    before={str(p):sha(p.read_bytes()) for p in protected}
    assert gloss['all224_complete_clean_first_meanings_before_current_English']
    assert controls['current_B61_B70_English_dialogue_bodies_still_unconsulted'] and names['current_B61_B70_English_dialogue_bodies_unconsulted']
    assert len(display['records'])==display['complete_native_source_page_count']==224 and display['source_FE_count']==0
    assert display['source_macro_counts']=={'FI':15,'FA':3,'FO':0}
    assert sum(len(r['original_four_alignments']['cases']) for r in display['records'])==896
    viewed_names=['B61_source_part1.png',*[f'B62_source_part{i}.png' for i in range(1,4)],
        *[f'B63_source_part{i}.png' for i in range(1,4)],*[f'B64_source_part{i}.png' for i in range(1,3)],
        *[f'B65_source_part{i}.png' for i in range(1,5)],*[f'B66_source_part{i}.png' for i in range(1,3)],
        *[f'B67_source_part{i}.png' for i in range(1,6)],'B68_source_part1.png','B69_source_part1.png','B70_source_part1.png']
    assert len(viewed_names)==23 and viewed_names==[Path(s['path']).name for s in display['review_sheets']]
    assert sum(s['source_page_count'] for s in display['review_sheets'])==224
    for s in display['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert sha(Path(names['review_sheet']['path']).read_bytes())==names['review_sheet']['sha256']
    assert len(names['native_name_planes'])==24
    assert len(clean_names['clean_current_consumer_bindings'])==32
    assert sum(len(g['utterance_membership']) for g in paths['groups'])==224
    assert sum(g['conditional_utterances'] for g in paths['groups'])==48
    assert [g['block'] for g in context['groups']]==[38,44]
    assert [len(g['records']) for g in context['groups']]==[18,27]
    assert [g['completed_coverage_overlap'] for g in context['groups']]==[0,27]
    for g in context['groups']:assert all(r['source_Japanese'] is not None and r['current_English_body_unread'] for r in g['records'])
    current=NdsImage.open(controls['candidate']);clean=NdsImage.open('work/clean.nds')
    referenced=[]
    for ident,japanese,english in [(39,'ペレイラ','Pereira'),(40,'クーン','Kuhn')]:
        versions={}
        for label,image in [('clean',clean),('current',current)]:
            arm=image.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000;at=table+32*ident+4
            versions[label]=dict(table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,struct.unpack_from('<I',arm,at)[0]))
        assert versions['clean']['text']==japanese and versions['current']['text']==english
        occurrences=[dict(id=r['id'],source_reference=r['source_reference'],source_hex=r['source_hex']) for g in gloss['groups'] for r in g['records'] if japanese in r['source_Japanese']]
        assert occurrences
        referenced.append(dict(actor_ID=ident,source_token=japanese,prose_term=english,exact_surname_fields=versions,
            source_occurrences=occurrences,decision='retain established source-bound surname spelling',
            reason='Preserve the fictional character identity and established readable project spelling. Do not replace it with a historical-person name or import biography. These are static surname references for prose, not new native header/full-name/biography approval.'))
    bindings=clean_names['clean_current_consumer_bindings'];records=[]
    for ident,reason in REASONS.items():
        binding=next(r for r in bindings if r['actor_ID']==ident and r['consumer']=='progressive-nameplate')
        occurrences=[dict(id=r['id'],source_reference=r['source_reference'],source_hex=r['source_hex'],source_complete_preamble_hex=r['source_complete_preamble_hex']) for g in gloss['groups'] for r in g['records'] if r['source_selector']==ident]
        assert occurrences
        records.append(dict(actor_ID=ident,consumer_scope='progressive-nameplate-in-clean-B61-B70-exchanges',
            source_display=binding['clean_text'],current_display=binding['current_text'],decision='retention',
            source_andcurrent_native_references=deepcopy(binding),source_dialogue_occurrences=occurrences,
            context=reason,retention_reason=reason,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            formatting_actual_representative_andbatch_release_scope_pending=True,
            actual_B61_B70_headers_fullcatalogue_UI_all207_andcustomnames_not_approved=True))
    assert len(records)==16
    ROOT.mkdir(parents=True)
    save(NAME_DOC,dict(format='dk4-scoped-speaker-name-editorial-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=records,referenced_prose_surnames=referenced,
        source_given_middle_surname_components_androle_metadata_kept_separate=True,
        all16_progressive_wordings_editorially_retained_withindividual_context_reasons=True,
        full_name_open_findings=['Camille nickname and distinct full-getter Marinus composition are preserved; no new true-name/cross-consumer approval.',
            'Al Shin/Al Ferid Shin remains consumer-specific; global name consistency and full catalogue/custom names stay open.',
            'All prior Geronimo/Alonso shared デ ownership, deployment and full-consumer leads remain open.'],
        formatting_actual_andregistered_gates_still_pending=True,
        no_dialogue_retention_source_prose_orcompletion_credit_added=True,new_credit=0,full_goal_complete=False))
    save(ROOT/'source_context_names_display_review_before_current_English.json',dict(
        candidate=controls['candidate'],candidate_sha256=controls['candidate_sha256'],
        all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English=True,
        viewed_sheets=display['review_sheets'],sixteen_actor24_current_nameplanes_sheet_directly_viewed=names['review_sheet'],
        native_dispatches=224,macro_alignment_cases=896,complete_native_source_pages=224,
        FI_given_Hodram6_FA_surname_Bergstrom9_proven_on_all18_source_macro_occurrences=True,
        FO_zero_occurrences_no_new_FO_semantics_orcustom_name_coverage=True,
        clean_linked_context_utterances_read=45,linked_context_B44_27_already_completed_no_duplicate_credit=True,
        context_findings=[
            'B38 is the explicit source event required by B69 and follows event68. Its complete18 speeches expose Kuhn false-flag fleet tactics: Camille says Maria detected and reported the plan. This explains Lil nearly doubting Maria; do not claim she actually betrayed Maria.',
            'B38 directly supplies the present ship name/faction macro FO in linked context, but its body/selectorD8/opaque controls are not newly localized or approved here. This source-only reading adds no completion credit for its18 uncredited speeches.',
            'Completed B44 supplies the prior Lil/Camille/Hodram encounter for B66 recognition. Familiar 兄ちゃん and 君 are forms of address; neither creates brotherhood, an age or military rank.',
            'B64 all23 speeches are conditional. Trader gift and Sera introduction occupy alternative first-query branches; the later leaf/legend segment has a separate query site. Repeated descriptors are not proof of constant results through intervening opaque effects.',
            'B65 crew pauses are alternatives, not consecutive repeated silences by every crew member. Exact source circle/cross strings remain opaque speech, not diagnostic placeholders or a decoded confession.',
            'B66 twelve later speeches need both structural tests; the first original8100 operand is event44. Its unforced opening query is0. This is no natural activation or universal current-game condition claim.',
            'B67 source replies yes/Kuhn?/Pereira?/no are four alternative familiarity paths; the full introduction and secrecy lines are conditional. Do not read them as one consecutive conversation.',
            'B69 元の鞘 describes restored relations/situation here; no literal scabbard, marriage or romantic reunion is established. Warm relief and teasing work demands remain.',
            'B70 distributes all concealed wealth to people harmed by Kuhn; the mixed-in object stays unnamed until separately established.'],
        source_branch_membership_totals=dict(unconditional_within_offline_models=176,conditional=48),
        branch_models_not_actual_eligibility_progression_orattainable_combinations=True,
        current_story_English_dialogue_bodies_still_unconsulted=True,
        source_only_no_final_English_localization_formatting_actual_scene_orregistered_release_approval=True,
        next_required=['compare all224 exact current English predecessors as complete exchanges',
            'individual source/context/localization/naturalness decisions and justified retentions',
            'automatic full-width native English wrapping and complete stored references/inverses',
            'representative initialized/natural gameplay and focused distinct behavior tests',
            'production and registered cumulative release/exact clean-input patch/own startup before once-only completion credit'],
        protected_files=before,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,NAMES,CLEAN_NAMES,DISPLAY,CONTEXT,PATHS,NAME_DOC,
            Path('docs/glossary.md'),Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]}))
    assert all(sha(Path(p).read_bytes())==digest for p,digest in before.items())
    print('Viewed23 source sheets/224pages and24current nameplanes;16scoped name retentions/2prose surname bindings/45linked clean context speeches recorded. No current storyEnglish,ROM,ledger orcredit change.')
