"""Save individual whole-exchange comparison findings with exact current/source bindings."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_hodram_B171_B190_drafts import ROOT

CURRENT = Path('work/analysis/Hodram_B171_B190_current_20261102/current_effective.json')
OBJECTS = Path('work/analysis/Hodram_B171_B190_current_objects_20261102/current_objects.json')
DRAFTS = ROOT / 'all435_clean_English_drafts_v2.json'


def normalized_current(row):
    text = row['current_comparison_paragraph']
    if text and all(c in '.…?!！？ ' for c in text):
        text = ('...' if any(c in text for c in '.…') else '') + ('?' if any(c in text for c in '?？') else '') + ('!' if any(c in text for c in '!！') else '')
    for macro in ['FI', 'FA', 'FO']:
        text = re.sub(r'(?<![A-Za-z])' + macro + r'(?![A-Za-z])', '{MACRO:' + macro + '}', text)
    return text


def save_comparison_part(label, decisions, overrides, producer):
    output = ROOT / (label + '_whole_exchange_comparison_v1.json')
    assert not output.exists()
    current, objects, drafts = map(load, [CURRENT, OBJECTS, DRAFTS])
    prior = {r['id']: r for g in current['groups'] for r in g['records']}
    prior.update({r['id']: r for r in objects['choice_records']})
    by_block = {b: [r for r in drafts['records'] if r['block'] == b and 'source_selector' in r] for b in decisions}
    rows = []
    for block, findings in decisions.items():
        assert len(findings) == len(by_block[block]), (block, len(findings), len(by_block[block]))
        for draft, entry in zip(by_block[block], findings, strict=True):
            code, finding = entry.split(' | ', 1)
            assert code in ['R', 'K'] and finding.strip()
            old = prior[draft['id']]
            assert all(old[k] == draft[k] for k in ['source_hex', 'source_reference', 'source_selector', 'source_complete_preamble_hex'])
            row = deepcopy(draft)
            for key in ['current_hex', 'current_reference', 'current_record_index', 'current_stored_text',
                'current_effective_hex', 'current_effective_text', 'current_comparison_paragraph',
                'current_catalogue_selected', 'selected_native_pointer']:
                if key in old:
                    row[key] = old[key]
            normalized = normalized_current(old)
            english = normalized if code == 'K' else overrides.get(draft['id'], draft['english'])
            assert not any(t in english for t in ['\n', '{LB', '{ALIGN', '{PAD}', '  '])
            source = bytes.fromhex(row['source_hex'])[1:]
            assert all(english.count('{MACRO:' + m + '}') == source.count(m.encode('ascii')) for m in ['FI', 'FA', 'FO']), row['id']
            english.encode('cp932')
            row.update(english=english, logical_English=english, decision='retention' if code == 'K' else 'revision',
                finding=finding, retention_reason=finding if code == 'K' else None,
                source_first_draft_English=draft['english'], source_first_draft_reference=dict(path=str(DRAFTS), sha256=sha(DRAFTS.read_bytes()), id=row['id']),
                current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
                current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,
                clean_source_current_anddraft_considered_in_complete_exchange=True,
                punctuation_only_glyph_normalization=(code == 'K' and normalized != old['current_comparison_paragraph']
                    and not any('{MACRO:' + m + '}' in normalized for m in ['FI', 'FA', 'FO'])),
                all_fifth_formatting_gates_still_pending=True,
                prose_comparison_review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
            if code == 'R' and english != draft['english']:
                row['comparison_refinement'] = dict(previous_draft=draft['english'], English=english, reason=finding)
            rows.append(row)
    save(output, dict(records=rows, blocks=list(decisions), compared=len(rows),
        proposed_revisions=sum(r['decision'] == 'revision' for r in rows), justified_retentions=sum(r['decision'] == 'retention' for r in rows),
        all_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'], new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [CURRENT, OBJECTS, DRAFTS, Path(producer), Path(__file__)]}))
    print(dict(compared=len(rows), revised=sum(r['decision'] == 'revision' for r in rows),
        retained=sum(r['decision'] == 'retention' for r in rows), blocks=list(decisions), new_credit=0))
