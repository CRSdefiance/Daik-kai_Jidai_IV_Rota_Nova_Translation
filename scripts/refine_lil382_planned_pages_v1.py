"""Revisit premature pages and split clauses without changing reviewed prose or width."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    before = ROOT/'formatting_v1/challenge_phrase_preferences_v2.json'
    out = ROOT/'formatting_v1/page_coherence_preferences_v3.json'
    assert not out.exists()
    manuscript = ROOT/'formatting_v1/formatting_input.json'
    rows = {r['id']:r for r in load(manuscript)['records']}
    planpath = ROOT/'plan_v2/automatic_plans.json'
    plans = {r['id']:r for r in load(planpath)['records']}
    prefs = load(before)
    onepage = {
        'DK4_MES_B12_R0196': 'Keep Lil’s full Basra explanation together rather than stranding the comparison with an ordinary pirate.',
        'DK4_MES_B12_R0247': 'Keep Aziza’s complete recognition of her crew’s anger together rather than stranding for being angry.',
        'DK4_MES_B17_R0012': 'Keep Lil’s capture/destination/cargo question together without leaving its cargo contrast on a second page.',
        'DK4_MES_B115_R0099': 'Keep Maria’s full distinction between slave traders and pillaging soldiers together.',
        'DK4_MES_B115_R0102': 'Keep Maria’s whole indiscriminate-hatred warning and guilt conclusion together.',
        'DK4_MES_B115_R0134': 'Attach or better to Maria’s complete qualified confidence statement.',
        'DK4_MES_B237_R0025': 'Keep Cesare’s arrow explanation and fussy Yes indeed together.',
        'DK4_MES_B237_R0039': 'Keep Cesare’s complete nearby-treasure argument together.',
        'DK4_MES_B239_R0110': 'Attach or crystal to the complete friend-of-a-friend swindler lead.',
    }
    for ident, reason in onepage.items():
        row = rows[ident]
        assert plans[ident]['expected_native_pages']==2 and len(row['english'])<=137
        assert ident not in prefs['records']
        prefs['records'][ident] = dict(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},
            one_page=True, reason='Fresh plan boundary review: '+reason+' Try the unchanged paragraph at full native width; reject if it cannot fit.')
    clauses = {
        'DK4_MES_B115_R0128': ('to justify their claims.', 'Keep the purpose of seeking the Proofs coherent across the native page boundary.'),
        'DK4_MES_B235_R0035': ('only a matter of time', 'Keep the impending-destruction idiom together across the reported chase’s page boundary.'),
        'DK4_MES_B235_R0044': ('the merchant fleet narrowly escaped disaster', 'Keep the merchant fleet and its escape together across the reported rescue’s page boundary.'),
        'DK4_MES_B240_R0120': ("I'll hand him over to the governor's office!", 'Keep the future handover statement together instead of stranding the destination on the next page.'),
    }
    for ident, (clause, reason) in clauses.items():
        row = rows[ident]
        assert plans[ident]['expected_native_pages']==2 and clause in row['english']
        assert ident not in prefs['records']
        prefs['records'][ident] = dict(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},
            page_clause=clause, reason='Fresh plan boundary review: '+reason+' Preserve all words, physical width and native page capacity.')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        reviewed_plan=str(planpath),reviewed_plan_sha256=digest(planpath),
        no_prose_font_viewport_control_or_runtime_change=True,new_credit=0)
    save(out,prefs)
    print('Prepared nine full-paragraph fit attempts and four source-bound page-clause preferences.')


if __name__ == '__main__':
    main()
