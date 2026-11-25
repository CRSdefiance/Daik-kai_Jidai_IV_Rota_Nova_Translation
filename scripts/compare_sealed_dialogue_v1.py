"""Save explicit individual prose decisions; never grant the fifth display gate."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

def compare(*, draft_path, current_path, output, retain, findings, overrides=None,
            punctuation=None, producer, context, extra=None):
    draft_path, current_path, output, producer = map(Path, [draft_path, current_path, output, producer])
    assert not output.exists()
    draft, current = map(load, [draft_path, current_path])
    byid = {r['id']:r for g in current['groups'] for r in g['records']}
    keys = {(r['block'], r['source_reference']['record_index']) for r in draft['records']}
    assert not (set(retain) & set(findings)) and set(retain) | set(findings) == keys
    records, glyphs = [], []
    for original in draft['records']:
        row = deepcopy(original)
        now = byid[row['id']]
        key = row['block'], row['source_reference']['record_index']
        prior = now['current_comparison_paragraph']
        for macro, count in row['source_macros'].items():
            assert prior.count(macro) == count
            prior = prior.replace(macro, '{MACRO:'+macro+'}')
        corrections = []
        replacements = {'Ｉ':'I', **(punctuation or {}).get(key, {})}
        for old, new in replacements.items():
            count = prior.count(old)
            if count:
                corrections.append(dict(old=old, new=new, count=count))
                prior = prior.replace(old, new)
        keep = key in retain
        english = prior if keep else (overrides or {}).get(key, row['english'])
        assert Counter(re.findall(r'\{MACRO:([A-Z]+)\}', english)) == Counter(row['source_macros'])
        assert english == english.strip() and not any(ord(c)<32 for c in english)
        assert not any(t in english for t in ['{LB', '{ALIGN', '{PAD}'])
        assert not any('Ａ'<=c<='Ｚ' or 'ａ'<=c<='ｚ' for c in english)
        assert keep or english != prior, row['id']
        finding = retain[key] if keep else findings[key]
        for name in ['current_hex', 'current_reference', 'current_record_index', 'current_stored_text',
                     'current_effective_hex', 'current_effective_text', 'current_comparison_paragraph',
                     'current_catalogue_selected', 'selected_native_pointer']:
            row[name] = now[name]
        if corrections:
            glyphs.append(dict(id=row['id'], corrections=corrections, wording_retained=keep))
        row.update(english=english, logical_English=english, decision='retention' if keep else 'revision',
            finding=finding, retention_reason=finding if keep else None, localization_note=finding,
            source_first_draft_English=original['english'],
            source_first_draft_reference=dict(path=str(draft_path), sha256=sha(draft_path.read_bytes()), id=row['id']),
            source_first_context_provenance=original['context'], context=context,
            source_first_draft=False, earlier_English_unconsulted=False, current_English_comparison_pending=False,
            current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
            complete_source_current_anddraft_considered_in_whole_exchange=True,
            four_prose_gates_pass_butformatting_pending=True, glyph_corrections=corrections)
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        records.append(row)
    revisions = sum(r['decision']=='revision' for r in records)
    save(output, dict(format='dk4-whole-exchange-editorial-comparison-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', records=records, proposed_revisions=revisions, justified_retentions=len(records)-revisions,
        glyph_corrections=glyphs, source_first_drafts=str(draft_path), source_first_drafts_sha256=sha(draft_path.read_bytes()),
        current_binding=str(current_path), current_binding_sha256=sha(current_path.read_bytes()),
        all_selected_complete_source_current_anddraft_exchanges_read=True,
        all_first_four_individual_gates_pass=True, all_individual_fifth_gates_still_false=True,
        fresh_formatting_native_visual_stored_actual_andregistered_integration_pending=True,
        new_credit=0, guide_photos=False, producer_sha256=sha(producer.read_bytes()),
        helper_sha256=sha(Path(__file__).read_bytes()), **(extra or {})))
    print(f'{len(records)} contextual comparisons: {revisions} proposed revisions/{len(records)-revisions} justified retentions; display/credit pending.', flush=True)
