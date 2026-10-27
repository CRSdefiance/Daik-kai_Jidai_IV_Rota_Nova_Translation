"""Independently compare staged/applied promotion metadata with full prior objects."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'work/analysis/promotion_v4725b'
PACKAGE = ROOT/'releases/all_routes_unified_v4701'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def audit(applied):
    plan = load(AUDIT/'mutation_plan.json')
    assert len(plan) == 12
    old,new = {},{}
    for i,row in enumerate(plan):
        prior = (AUDIT/f'{i}.before').read_bytes()
        staged = (AUDIT/row['planned']).read_bytes()
        assert sha(prior) == row['before_sha256']
        assert sha(staged) == row['planned_sha256']
        assert (ROOT/row['target']).read_bytes() == (staged if applied else prior)
        old[row['target']],new[row['target']] = prior,staged
    ledger_path = 'translations/editorial_review_current_v1.json'
    a,b = [json.loads(d[ledger_path]) for d in [old,new]]
    additions = {'promoted_main_build_v4725','lil_B179_uncredited_draft_v4725','unfinished_editorial_scope_v4725'}
    assert set(b)-set(a) == additions and set(a)-set(b) == set()
    for key in a:
        if key != 'latest_checkpoint': assert a[key] == b[key], key
    assert b['goal_status'] == 'active' and not b['full_goal_complete']
    assert b['records_editorially_completed'] == 5898
    assert b['records_with_source_and_prose_pass'] == 5901
    assert b['lil_B179_uncredited_draft_v4725']['credit_added'] == 0
    scope = b['unfinished_editorial_scope_v4725']
    previous_scope = load(PACKAGE/'verification/previous_unfinished_editorial_scope_inventory.json')
    assert all(scope[k] == v for k,v in previous_scope.items())
    assert scope['untranslated_Sao_Jorge_alias_lead'] == load(PACKAGE/'verification/untranslated_Sao_Jorge_alias_reference_lead.json')
    reg_path = 'translations/release_stack.json'
    a,b = [json.loads(d[reg_path]) for d in [old,new]]
    assert set(a) == set(b)
    for key in a:
        if key != 'latest_promoted_build': assert a[key] == b[key], key
    assert b['latest_promoted_build']['profile'] == 'all-routes-unified-v4701'
    assert b['profiles']['all-routes-unified-v4701']['status'] == 'experimental'
    assert len(b['accepted_layers']) == 114
    pins_path = 'translations/rom_retention_pins.json'
    a,b = [json.loads(d[pins_path]) for d in [old,new]]
    assert b[:-1] == a and len(b) == len(a)+1
    for path in old:
        if path.startswith('docs/'):
            prior = old[path].decode('utf-8').replace('\r\n','\n')
            staged = new[path].decode('utf-8')
            assert staged.endswith(prior.split('\n',1)[1]), path
            assert staged.count('## V4725: V4701 promoted as main; B179 draft preserved') == 1
            assert 'The full editorial objective remains active.' in staged
            assert 'later older-record technical re-audit/queued0D gap' in staged
    assert new['.gitignore'].decode('utf-8') == old['.gitignore'].decode('utf-8').replace('\r\n','\n')+'!releases/all_routes_unified_v4701/*.xdelta\n'
    text = old['README.md'].decode('utf-8').replace('\r\n','\n')
    text = text.replace('[Unified V4595](releases/all_routes_unified_v4595/README.md)',
        '[Unified V4701](releases/all_routes_unified_v4701/README.md)')
    text = text.replace('Earlier [V4541]','Earlier [V4595](releases/all_routes_unified_v4595/README.md), [V4541]',1)
    assert new['README.md'].decode('utf-8') == text
    assert gzip.decompress((PACKAGE/'build_release_stack.json.gz').read_bytes()) == old[reg_path]
    assert gzip.decompress((PACKAGE/'build_manifest.json.gz').read_bytes()) == (ROOT/'out/all_routes_combined_v4701_candidate.manifest.json').read_bytes()
    promotion = json.loads(new['translations/promoted_build.json'])
    assert promotion == load(PACKAGE/'promotion.json')
    assert promotion == json.loads(new[ledger_path])['promoted_main_build_v4725']
    assert promotion['rom_sha256'] == 'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e'
    assert promotion['construction_baseline_rebased'] is False
    assert (PACKAGE/'translation.xdelta').read_bytes() == (ROOT/'out/all_routes_combined_v4701_candidate.xdelta').read_bytes()
    assert not any(p.suffix.lower() in ['.nds','.rom','.sav','.dsv'] for p in PACKAGE.rglob('*'))
    receipt = dict(checkpoint='V4725',applied=applied,all12_target_hashes_verified=True,
        complete_prior_ledger_root_and_nested_values_preserved=True,all_coverage_unchanged=True,
        immutable_baseline_accepted_layers_all_profiles_preserved=True,old_pins_preserved=True,
        all_historical_doc_sections_preserved=True,previous_scope_preserved_and_city_alias_lead_carried=True,
        B179_draft_outside_ROM_and_uncredited=True,package_contains_no_ROM_or_save=True,
        full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
    path = AUDIT/('independent_postapplication_audit.json' if applied else 'independent_preapplication_audit.json')
    assert not path.exists()
    path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('Independent promotion audit passed:', 'applied' if applied else 'staged', '; full history and coverage preserved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--applied',action='store_true')
    audit(parser.parse_args().applied)
