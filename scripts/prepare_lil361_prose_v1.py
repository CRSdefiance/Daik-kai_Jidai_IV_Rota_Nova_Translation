"""Assemble all source-bound comparisons and scoped names without changing sealed inputs."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
NAME_REASONS = {
    2: 'Retain approved Lil Argot and the exact default FI/FA/FO/FU forms. Her fear, bravado, intuitive decisions and royal-vanity teasing establish no new relationship or rank.',
    9: 'Retain approved Camille Overijssel and full Camille Marinus Overijssel, matching the clean components and established consumers. Lil addresses Camille by the approved given name; no relationship is invented.',
    14: 'Retain Emilio Ferog, matching the clean identity and native consumers. The bear scene explicitly names Emilio and reveals his real sleep while playing dead; he is distinct from Fernando.',
    18: 'Retain Charles Rochefort and full Charles Jean Rochefort, faithful to the source components and established consumers. His hesitant unfinished objection in the dark cave adds no invented body part or biography.',
    20: 'Retain Fernando Dias, consistent with the source components and both current consumers. Do not merge his expedition reactions with Emilio or assign him a new naval rank.',
    22: 'Retain Samwell Khan and full Samwell da Khan, preserving the reviewed component order and particle. His advice and warnings add no historical identity or family connection.',
    76: 'Retain Mikhail Letzel and full Mikhail Volk Letzel, faithful to the source components and established consumers. His opportunistic cave joke and apology establish no romantic relationship with Lil.',
    95: 'Retain Patron for the actual tavern-customer archetype. Giving route information does not turn his generic source nameplate into a newly named professional guide; Europe is metadata, not a surname.',
    104: 'Retain Trader for the source trade-house proprietor. Familiar oyaji wording is not fatherhood; his Wine payment and odd-group report establish no additional relationship or title.',
    113: 'Retain Port Worker for the port-office role. The familiar brother-like Japanese label establishes neither kinship nor a naval rank; destination messages remain source-bound.',
    147: 'Retain Guildmaster for the source guild head in the European job exchange. Regional metadata is not a personal name; guild authority establishes no relationship to Lil.',
    148: 'Retain Guildmaster for the source guild head in the Istanbul collection job. Passing on the emperor\'s request does not make him a court officer, a vassal king or a relative. Unconsumed regional/religious metadata remains in the broader review.',
    151: 'Retain progressive Sailor and the existing catalogue alias Retainer for this generic subordinate and the exact startup role fallback. No future conditional assignment, feudal rank or full catalogue UI approval is inferred. Broader catalogue role terminology remains in scope.',
    170: 'Retain Mysterious Old Man for the source mysterious-elder label. The scene identifies him as a nearby village elder, without proving kinship, supernatural identity or a new clerical rank.',
    199: 'Retain Lucia for the source Rushia identity and both current consumers. Malacca is regional metadata rather than an appended surname or an invented nationality.',
}


def main():
    output = ROOT / 'contextual_comparisons_v1.json'
    terms_path = ROOT / 'scoped_terms_reference_v1.json'
    config = ROOT / 'prose_config_v1.json'
    assert not any(p.exists() for p in [output, terms_path, config])
    partpaths = [ROOT / f'contextual_{part}_v1.json' for part in ['B283_B287', 'B288_B292', 'B293_B298']]
    parts = [load(p) for p in partpaths]
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    rows = [deepcopy(r) for p in parts for r in p['records']]
    originals = [r for g in packet['groups'] for r in g['records']]
    assert len(rows) == len(originals) == len({r['id'] for r in rows}) == 361
    assert all(p['runtime'] == parts[0]['runtime'] and p['all_five_gates_still_pending'] for p in parts)
    corrections = []
    for row, original in zip(rows, originals, strict=True):
        assert all(row[k] == original[k] for k in ['id', 'file_path', 'source_hex', 'source_reference', 'source_Japanese'])
        assert not any(row['review'].values())
        if row['block'] == 284:
            before = row['whole_exchange_context']
            after = 'A messenger recognizes the visitor by runtime surname FA (Argot) and relays that London guild was looking for her. FA alone is not a company-affiliation expression; preserve direct name recognition without inventing kinship or a summons.'
            row['sealed_independent_exchange_context'] = before
            row['whole_exchange_context'] = after
            corrections.append(dict(id=row['id'], field='whole_exchange_context', before=before, after=after,
                reason='Native FA expands to the surname Argot; preserve the original independent draft and correct its provisional affiliation assumption.'))
    counts = Counter(r['decision'] for r in rows)
    assert counts == {'revision': 177, 'retention': 184}
    runtime = parts[0]['runtime']
    names_path = ROOT / 'scoped_names_macros_reference_v1.json'
    assert {r['actor_ID'] for r in load(names_path)['records']} == set(NAME_REASONS)
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=2)
    assert ctx.receipt() == runtime
    item_path = ROOT / 'item_terms_reference_v1.json'
    item_terms = load(item_path)
    assert item_terms['runtime'] == runtime and len(item_terms['items']) == 2
    assert {(r['source']['text'], r['current']['text']) for r in item_terms['items']} == {
        ('錬金術の書', 'Alchemy Book'), ('天佑のリストバンド', 'Heavenly Wristband')}
    pointer_path = ROOT / 'town_andProof_pointer_reference_v1.json'
    pointer_terms = load(pointer_path)
    assert pointer_terms['runtime'] == runtime
    assert {(r['field_offset'], r['source']['text'], r['current']['text']) for r in pointer_terms['fields']} == {
        (1191768, 'イスタンブール', 'Istanbul'), (1295216, '覇者の証', 'Proof'), (1503776, '覇者の証', 'Conq Proof')}
    prior_path = Path('translations/maria310_integrated_final_review_v1.json')
    prior = load(prior_path)
    anchor = next(r for r in prior['records'] if r['id'] == 'DK4_MES_B53_R0006')
    assert anchor['english'] == 'That makes all the Proofs of Conquest...' and all(anchor['review'].values())
    assert digest(prior['target_ROM']) == prior['target_ROM_sha256']
    old = NdsImage.open(prior['target_ROM'])
    assert old.read_file('/__arm9__.bin') == ctx.arm and old.read_file('/COMMON/MESFILE.DK4') == ctx.common
    before = IlnkContainer.parse(old.read_file('/data/SC3.DK4')).blocks[53]
    now = IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks[53]
    assert before == now
    ref = anchor['planned_integrated_reference']
    raw = bytes.fromhex(ref['exact_stored_hex'])
    assert now[ref['offset']:ref['offset'] + len(raw) + 1] == raw + b'\0'
    save(terms_path, dict(runtime=runtime, items=item_terms['items'], town_andshort_Proof_UI=pointer_terms['fields'],
        full_Proof_term=dict(singular='Proof of Conquest', plural='Proofs of Conquest', short='Proof',
            approved_integrated_reference=dict(path=str(prior_path), id=anchor['id'], source_reference=anchor['source_reference'],
                current_reference=ref, english=anchor['english'], review=anchor['review'])),
        exact_prior_SC3_B53_ARM9_andCOMMON_reuse=True, only_source_spoken_item_titles_may_be_inserted=True,
        current_market_wording_retained_for_source_trade_house=True, no_new_UI_display_oractual_effect_approval=True,
        new_credit=0, evidence={str(p): digest(p) for p in [item_path, pointer_path, prior_path, Path(__file__)]}))
    evidence = {str(p): digest(p) for p in [*partpaths, packet_path, names_path, terms_path,
        ROOT / 'dynamic_roles_current_v1.json', ROOT / 'current_objects_v1/current_objects.json', ROOT / 'clean_draft_seal_v1.json', Path(__file__)]}
    save(output, dict(records=rows, records_count=361, complete_exchanges=16, blocks=packet['selected_blocks'], runtime=runtime,
        revised=177, retained=184, all_individual_findings_andretention_reasons_saved=True, all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True, contextual_metadata_corrections=corrections,
        sealed_independent_drafts_preserved_not_rewritten=True, evidence=evidence, new_credit=0, full_goal_complete=False))
    amendments = {'DK4_MES_B295_R0008': dict(
        before="His Majesty will host a vassal king soon. He plans to show his collection to the honored guest.",
        after="His Majesty the Emperor will soon host a vassal king. He plans to show his collection to his honored guest.",
        reason='Keep the source\'s explicit Emperor title in the exchange; His Majesty alone leaves that specific rank unstated.')}
    kinds = Counter('typed-choice-label' if r['kind'] == 'typed-menu-caption' else
        'system-FE' if r.get('source_selector') == 254 else 'progressive' for r in rows)
    save(config, dict(proposals=str(output), names=str(names_path), terms=str(terms_path),
        roles=str(ROOT / 'dynamic_roles_current_v1.json'), objects=str(ROOT / 'current_objects_v1/current_objects.json'),
        source_objects=361, proposal_counts=[177, 184], final_counts=[178, 183], item_bindings=2, file_path='/data/SC2.DK4',
        name_reasons=NAME_REASONS, scope_id='LIL_SC2_B283_B298_361',
        name_context='Sixteen complete clean/current Lil exchanges B283-B298; exact scoped progressive/catalogue strings and startup roles only. The earlier credited B294 line is context, not new review credit. Future conditional roles and full catalogue UI remain unvisited.',
        amendments=amendments, FE_contexts={283:'FE injury, fatigue and one-day elapsed notices', 287:'FE Wine payment and London-share notices',
            288:'FE apparent-injury notice', 292:'FE unnamed ancient voice and wordless reaction; no ordinary actor nameplate',
            293:'FE one-day elapsed and crew-decrease notices', 297:'FE wristband-job payment and Istanbul-share notices'},
        kind_counts=dict(kinds), out='translations/lil_B283_B298_contextual_review_v1.json',
        names_out='translations/lil_B283_B298_scoped_names_v1.json', proof_out=str(ROOT / 'prose_gates_v1.json')))
    print('PASS361 comparisons in source order;15 individual name reasons;two items,Istanbul andfull Proof term bound.')


if __name__ == '__main__':
    main()
