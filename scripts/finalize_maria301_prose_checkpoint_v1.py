"""Seal301 contextual prose decisions after scoped identity/term reconciliation; formatting remains gated."""
from copy import deepcopy
from pathlib import Path
import re
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = Path('translations/maria_B0_B32_contextual_review_v1.json')


def main():
    terms_path = ROOT/'scoped_terms_v1.json'
    names_path = ROOT/'scoped36_name_editorial_review_v2.json'
    assert not any(p.exists() for p in [OUT,terms_path,names_path])
    proposals_path = ROOT/'all301_contextual_proposals_v1.json'
    original_names_path = ROOT/'scoped36_name_editorial_review_v1.json'
    bindings_path = ROOT/'scoped_names_items_macros_reference_v1.json'
    roles_path = ROOT/'dynamic_roles_current_v1.json'
    proposals,names,bindings,roles = map(load,[proposals_path,original_names_path,bindings_path,roles_path])
    ctx = RegisteredRuntime(bindings['runtime']['release_proof'],bindings['runtime']['startup_proof'],captain=3)
    assert all(r['current_reference']['candidate_sha256']==ctx.release['candidate_sha256'] for r in names['records'])
    assert ctx.receipt()==bindings['runtime']==roles['runtime']
    assert proposals['records_count']==301 and (proposals['revised'],proposals['retained'])==(178,123)
    # State only the values actually returned by native dispatch. A strict value
    # outside the static actor range is not by itself a proof of assignment semantics.
    lookout = next(r for r in roles['native_roles']['rows'] if r['source_selector']==214)
    assert (lookout['strict_assignment'],lookout['resolved_actor_ID'])==(208,156)
    refined_names = deepcopy(names)
    row = next(r for r in refined_names['records'] if r['actor_ID']==156)
    reason = ('Retain Sailor/Retainer for the current startup’s dynamic fallback actor. '
        'The strict getter returns208 and original speech dispatch resolves156; this does not prove '
        'an actual B32 lookout assignment or future roster. East-Asian metadata is not a surname.')
    for key in ['finding','retention_reason','localization_note']:
        row[key]=reason
    refined_names.update(previous_name_review=str(original_names_path),previous_name_review_sha256=digest(original_names_path),
        only_actor156_role_rationale_clarified_no_name_gate_orconsumer_change=True)
    refined_names['evidence'].update({str(roles_path):digest(roles_path),str(Path(__file__)):digest(__file__)})
    save(names_path,refined_names)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    wanted = {'Batavia','Calicut','Athens','Veracruz'}
    cities=[]
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in wanted:
            continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        value=ctx.arm[entry.offset:entry.offset+entry.slot_size]
        expected=entry.suggested_english.encode()
        assert value==expected+bytes(entry.slot_size-len(expected))
        cities.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_hex=entry.expected_bytes.hex(),
            source_Japanese=entry.japanese,current_span_hex=value.hex(),current_term=entry.suggested_english))
    assert len(cities)==5 and {r['current_term'] for r in cities}==wanted
    havana_reference=Path('work/analysis/Hodram_B191_B210_clean_20261104/source_current_term_checkpoint_v1.json')
    aliases=next(r for r in load(havana_reference)['cities'] if r['current_term']=='Havana')['source_qualified_typed_aliases']
    havana=[]
    for alias in aliases:
        field=alias['pointer_field']
        sp,tp=[struct.unpack_from('<I',arm,field)[0] for arm in [clean,ctx.arm]]
        source,current=string(clean,sp),string(ctx.raw,tp)
        assert source['text']=='ハバナ' and current['text']=='Havana'
        havana.append(dict(pointer_field=field,source=source,current=current))
    assert havana
    assert {r['token']:r['text'] for r in bindings['default_macro_cases']}==dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    assert {r['source']['text']:r['current']['text'] for r in bindings['registered_item_names']}=={
        '血塗られたシャムシール':'Bloodstained Shamshir','妖刀村正':'Muramasa'}
    save(terms_path,dict(runtime=ctx.receipt(),inline_city_aliases=cities,Havana_aliases=havana,
        registered_items=bindings['registered_item_names'],default_macros=bindings['default_macro_cases'],
        contextual_Muramasa_cursed_blade_descriptor_not_catalogue_rename=True,
        source_soaring_scarlet_orca_reference='docs/name_source_review_v294.md',
        Ming_government_andisolation_are_character_story_statements_not_external_history_claims=True,
        Proof_authenticity_andghost_ship_identity_remain_uncertain=True,
        no_global_city_alias_UI_orname_table_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [bindings_path,havana_reference,Path('docs/name_source_review_v294.md'),Path(__file__)]}))
    name_forms={r['actor_ID']:next(v['text'] for v in r['current_consumers'] if v['consumer']=='progressive-nameplate')
        for r in refined_names['records']}
    records=deepcopy(proposals['records']);refinements=[]
    for row in records:
        english=row['proposed_English']
        if row['id']=='DK4_MES_B3_R0026':
            assert english=="Oh, listen to you. A stiff-necked prig. Just the sort I can't stand."
            refined="Oh, listen to you. So stiff and proper. Just the sort I can't stand."
            refinements.append(dict(id=row['id'],previous=english,revised=refined,
                reason='Use natural American mockery in Kurushima’s rough voice instead of the uncommon prig; preserve his dislike of rigid propriety.'))
            english=refined
            row['localization_note']+=' Naturalness reread replaces prig with stiff and proper.'
            row['finding']=row['localization_note']
        source_kind=row['kind'];selector=row.get('source_selector')
        if source_kind=='typed-menu-caption':
            speaker,kind='Player choice','typed-choice-label'
        elif source_kind=='physical-style-alternative':
            assert selector==214
            speaker='Dynamic lookout selector214; startup fallback Sailor, conditional assignment unvisited'
            kind='progressive'
            row.update(native_object_kind='4100-style-alternative',virtual_formatter_prefix_not_in_stored_body=True)
        else:
            assert source_kind=='ordinary-speech' and selector in name_forms
            speaker,kind=name_forms[selector],'progressive'
        assert not any(row['review'].values())
        assert row['source_meaning'] and row['whole_exchange_context'] and row['localization_note']
        assert english.isascii() and not any(t in english for t in ['\n','\r','\t','{LB','{ALIGN','{PAD}'])
        assert {t:english.count(t) for t in row['source_macros']}==row['source_macros']
        assert set(re.findall(r'F[A-Z]',english))==set(row['source_macros'])
        if row['decision']=='retention':
            assert english==row['current_comparison_paragraph'] and row['retention_reason']
        row.update(english=english,logical_English=english,proposed_English=english,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],
            native_literal_token_counts=row['source_macros'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            source_meaning_pending=False,localized_draft_pending=False,current_English_comparison_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,
            name_term_consumer_review_andfresh_display_still_pending=False,
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    document=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC3.DK4',blocks=sorted({r['block'] for r in records}),records=records,source_objects=301,
        proposed_revisions=178,justified_retentions=123,current_ROM=proposals['current_ROM'],current_ROM_sha256=proposals['current_ROM_sha256'],
        runtime=ctx.receipt(),all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        final_naturalness_refinements=refinements,native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,
        evidence={str(p):digest(p) for p in [proposals_path,names_path,terms_path,roles_path,Path(__file__)]})
    projected=deepcopy(document);projected['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(document)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript bypassed v2 release gate')
    save(OUT,document)
    summary=('Maria301 now has all contextual decisions:178 proposed revisions/123 justified retentions. '
        'All301 four-prose gates pass;formatting remains false andthe v2 release gate correctly rejects the unformatted manuscript. '
        'Thirty-six scoped names/roles retain their source-bound forms;72 native getters,four default Maria macros,two items '
        'andfive spoken ports are reconciled. Twelve glyph targets andfresh wrap/page/storage/gameplay checks remain. '
        'Integrated19,161/registeredf166991f/main andall scope remain unchanged;zero new credit.')
    text='''# Maria301 contextual prose checkpoint — November9,2026

All301 records in32 complete exchanges now have individual contextual decisions: **178 proposed revisions and123 justified retentions**. The source-first meanings/drafts and all original proposal chunks remain preserved. The current manuscript is `translations/maria_B0_B32_contextual_review_v1.json`. Every record passes source/context/localization/naturalness review; every formatting gate remains false. The v2 release validator correctly rejects the unformatted manuscript, while the structural prose projection passes. No completed-review credit or new ROM is claimed.

Concrete findings include Maria speaking of herself as she, Lord Al, Sir addressed to Maria, unsupported empty-purse and family-trade claims, personal motives/apologies changed to we, Kuen/Berrio inconsistencies, tentative ship recognition changed into repeat sightings, certainty in the ghost-ship account, and spoken Screech stage directions. Good existing dialogue, both choice captions, the correct conditional million-gold question and source-qualified epithet are retained with individual reasons. The final naturalness reread replaces prig with stiff and proper in Kurushima’s rough American English voice; all earlier drafts remain evidence.

`work/Maria_B0_B32_clean_20261109/scoped36_name_editorial_review_v2.json` records36 contextual name/role retentions. Their72 native getter bindings include70 exact reuses andtwo supplementary Sailor/Retainer getters. Current nameplate/catalogue forms confirm Hernan Berio, Antony Kuhn, approved Maria Huamei Li andthe other settled names. Dialogue spelling corrections require no name-table patch. The wider207-name audit and Cristina/Christina consumer distinction remain separately open.

Native selector214 resolves to startup fallback actor156/voice4; its strict getter returns208. These are actual native return values, not proof of an assigned B32 lookout or a future roster. The v2 name note replaces the earlier overbroad unassigned-role wording with these precise limits. All seven physical alternatives andeight alias slots remain in scope.

`scoped_terms_v1.json` binds the five spoken ports through five exact inline aliases plus qualified Havana pointers, the two registered weapons andallfour default Maria macros on the current captain3 context. FI=Maria,FA=Li,FO=Li Clan,FU=Maria Huamei Li. Cursed blade describes the source Muramasa epithet in dialogue; it does not rename the registered Muramasa item. The earlier source-qualified Soaring Scarlet Orca inference remains distinct from the Shachihoko item andis not represented as an official English name. These readbacks do not approve every legacy alias or arbitrary custom-name width.

The complete comparison proof is `all301_contextual_proposals_qualification_v1.json`, including12 glyph-consistency targets. This is a target count, not twelve newly verified rendering failures. The full-width I at B14R5 is a concrete mixed-font lead; remaining targets are reaction/silence punctuation. Every final changed or retained paragraph still needs fresh consumer formatting andreadable page review, including phrase continuity, sparse opening lines andpagination. Three native utterances preserve Manuel’s poem as one quotation without authored ordinary line breaks.

Continue with final formatter inputs/profiles, all body/menu/name native pages, stored-script/catalogue/load checks andrepresentative gameplay. Reuse compatible engine proofs andthe current Maria context; expand only for changed dependencies, failures or concrete risks. The31,000-frame opening-to-Hangzhou context is already verified; do not replay it or count it as B0–B32 gameplay. No process is live.

Integrated totals stay **19,161=11,532 revisions+7,629 retentions**; historical counters retain19,164. Remaining native-story objects still total6,737 pending full review/integration, with shared/UI scope separate. Current registered candidate remains `work/hodram_residual_release_v1/all_routes_hodram_residual_candidate.nds`, SHA-256 `f166991f83f18859a7483850ccee07945b76993f1ded491dec3b37b7e4ae01d8`; its manifest/patch, accepted layers andASCII right-bound correction are unchanged. Main remains all-routes-unified-v4701. Preserve all earlier work, ROMs, evidence andfull editorial scope; no guide photos or main promotion. Deferred artwork andthe later older-record technical re-audit remain separate.
'''
    release=load('work/hodram_residual_release_v1/registered_release_verification.json')
    checkpoint(mutation='work/Maria301_all_contextual_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria301:178 revisions/123 retentions,four prose gates pass;fresh display next.',
            new_source_meanings=301,new_independent_drafts=301,new_current_comparisons=301,
            proposed_revisions=178,justified_retentions=123,all_current_batch_five_gates_pending=False,
            all_current_batch_fifth_gates_pending=True,current_batch_not_yet_integrated=True,
            next_action='Format301 final paragraphs;reviewallnewpages,names/menus,glyphs;stored andrepresentative checks,thenregisteredintegration.',guide_photos=False),
        additional_updates={'Maria_SC3_B0_B32_clean_20261109':dict(new_credit=0,current_comparisons=301,
            remaining_current_comparisons=0,proposed_revisions=178,justified_retentions=123,
            contextual_manuscript=str(OUT),contextual_manuscript_sha256=digest(OUT),
            all_five_gates_pending=False,all_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
            scoped_name_retentions=36,scoped_name_review=str(names_path),scoped_name_review_sha256=digest(names_path),
            scoped_terms=str(terms_path),scoped_terms_sha256=digest(terms_path),glyph_targets=12,
            native_display_stored_andrepresentative_gameplay_pending=True,registered_integration_pending=True)},
        summary=summary,document='docs/editorial_Maria301_contextual_20261109.md',document_text=text,
        completed=19161,protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved301 contextual reviews:178 revisions/123 retentions;four prose gates pass;formatting/release safely gated. Integrated19161 unchanged.')


if __name__=='__main__':
    main()
