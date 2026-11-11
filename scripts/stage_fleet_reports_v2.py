"""Keep fleet and captain names together and use matching amount glyphs."""

from collections import Counter
from hashlib import sha256
from inspect import getsource

from dk4tool.patch.fleet_report_amount_glyphs_v1 import AMOUNT_TABLES, amount_assembly
from scripts import stage_fleet_reports_v1 as first
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = first.ROOT.with_name('fleet_reports_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('fleet_reports_context_v2.json')
AMENDMENTS = {
    2533: ("%s in sight. We're moving in!",
           'Put the spotted fleet and imminent attack in separate beats and keep the original company label whole.'),
    2534: ("%s in sight! Here we go!",
           'Keep the excited report and immediate attack, with the company name in one phrase.'),
    2535: ("%s spotted! Let's go after 'em!",
           'Keep the decisive call to attack and the full company label.'),
    2537: ("It's %s! We're under attack!",
           'Identify the attacking faction with a complete name and keep the immediate danger explicit.'),
    2539: ("%s is attacking us!",
           'Keep the warning direct and place the full company name together.'),
    2541: ("%s %s's fleet is beaten! Victory is ours!",
           'Keep the formal announcement and both beats of the source. Lead with the intact opposing captain name.'),
    2547: ("%s %s's fleet is beaten! We really won!",
           'Put the opposing name first so the younger speaker’s delighted realization can follow as its own thought.'),
    2553: ("%s %s's fleet has defeated us...",
           'Preserve the formal, disappointed admission and keep the opposing captain name on one row.'),
    2554: ("%s %s's fleet beat us...",
           'Preserve the first-person plural and deflated tone while keeping the opposing name intact.'),
    2558: ("%s %s's fleet beat us...",
           'Use a short, rueful admission. The opposing name stays together for the longer surname.'),
    2561: ("%s %s's fleet was too strong. We pulled back...",
           'Keep the strength judgment and retreat in separate thoughts.'),
    2563: ("%s %s's fleet proved stronger than expected. We withdrew...",
           'Keep the measured comparison and make the retreat its own thought.'),
    2575: ("Cash on hand won't cover the loss. The balance goes into next month's expenses.",
           'Keep the formal report of a shortfall and the balance carried into next month’s expenses.'),
    2576: ("We don't have the cash to cover the loss. We'll carry the rest over to next month's expenses.",
           'Keep the explanation and first-person commitment. A complete phrase opens the first row.'),
    2578: ("We haven't enough to cover the loss. Best carry the balance over to next month's expenses.",
           'Keep the older voice’s reflection and the accounting decision in separate thoughts.'),
}
PHRASES = first.PHRASES | {
    2575: ("Cash on hand won't cover the loss.", "into next month's expenses."),
    2576: ("We don't have the cash", 'to cover the loss.', "We'll carry the rest over", "to next month's expenses."),
    2578: ("We haven't enough", 'to cover the loss.', 'Best carry the balance over', "to next month's expenses."),
}


def install_in_scoped_assembly(assembly, environment):
    source = checked_text(getsource(assembly), {
        "'cmp r3, ip', 'beq dynamic_wrap'":
            "'cmp r3, ip', 'beq amount_wrap' if key in AMOUNT_TABLES else 'beq dynamic_wrap'",
        "f'b {LITERAL_PARAGRAPH:#x}', 'static_dispatch:'))":
            "f'b {LITERAL_PARAGRAPH:#x}'))\n"
            "    out.extend(AMOUNT_ASSEMBLY.splitlines())\n"
            "    out.append('static_dispatch:')",
    })
    env = environment | {'AMOUNT_TABLES': AMOUNT_TABLES, 'AMOUNT_ASSEMBLY': amount_assembly()}
    exec(compile(source, __file__ + '::finance-only-glyph-dispatch', 'exec'), env)
    return env['assembly']


def stage(runtime, release, rows, groups, verified=None):
    def selector_checks(arm, execute):
        if verified is None:
            return execute(arm)
        assert sha256(arm).hexdigest() == verified['research_ARM9_sha256']
        return verified['ownership']['selector_checks']

    source = checked_text(getsource(first.prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [27]",
        'assemble = FunctionType(selector.assembly.__code__, vars(selector) | parameters)':
            'assemble = install_in_scoped_assembly(selector.assembly, vars(selector) | parameters)',
        "checks = env['verify_scope'](arm)": "checks = check_exact_selector(arm, env['verify_scope'])",
        "'literal_scopes': list(static.items()), 'dynamic_scopes': list(dynamic.items()), 'selector_checks': checks,":
            "'literal_scopes': list(static.items()), 'dynamic_scopes': list(dynamic.items()), 'selector_checks': checks,\n"
            "        'ascii_digit_tables': list(AMOUNT_TABLES), 'original_numeric_getter_unchanged': True,",
    })
    env = vars(first.prior) | {'review': first.review, 'PHRASES': PHRASES,
                              'install_in_scoped_assembly': install_in_scoped_assembly, 'AMOUNT_TABLES': AMOUNT_TABLES,
                              'check_exact_selector': selector_checks}
    exec(compile(source, __file__ + '::finance-glyph-and-storage-scope', 'exec'), env)
    return env['stage'](runtime, release, rows, groups)


def stage_environment():
    return vars(first) | globals()


def main():
    base = first.review.prior
    assert not ROOT.exists()
    if not OUTPUT.exists():
        draft = base.load(first.OUTPUT)
        for row in draft['records']:
            number = row['message_ID']
            if number in AMENDMENTS:
                english, note = AMENDMENTS[number]
                assert english.count('%s') == row['original_substitution_count']
                row.update(english=english, localization_note=note, decision='revision')
        draft['counts'] = dict(Counter(row['decision'] for row in draft['records']))
        draft['visual_amendments'] = sorted(AMENDMENTS)
        draft['previous_proof_sha256'] = base.digest(first.PROOF)
        base.save(OUTPUT, draft)
    source = checked_text(getsource(first.main), {
        "            assert b' '.join(display.split()) == expected, (number, display, expected)":
            "            original_expanded = expected\n"
            "            if group['argument_kind'] == 'gold':\n"
            "                expected = template % (str(sample['value']).encode('ascii'),)\n"
            "            assert b' '.join(display.split()) == expected, (number, display, expected)",
        "            assert all(any(phrase in line for line in lines)":
            "            if group['argument_kind'] in ('company', 'captain'):\n"
            "                name = b' '.join(arguments).decode('cp932')\n"
            "                assert any(name in line for line in lines), (number, name, lines)\n"
            "            assert all(any(phrase in line for line in lines)",
        'expanded_hex=expected.hex(),': 'expanded_hex=original_expanded.hex(), normalized_visible_hex=expected.hex(),',
    })
    env = stage_environment()
    exec(compile(source, __file__ + '::format-verified-fleet-report', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
