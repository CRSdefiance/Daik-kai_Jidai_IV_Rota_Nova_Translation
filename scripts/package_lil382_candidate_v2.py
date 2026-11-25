"""Resume the verified package prefix after the out-junction permission boundary."""
from pathlib import Path
import gzip
from scripts import package_lil382_candidate_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def verify_prefix():
    root,out,test=previous.ROOT,previous.OUT,previous.TEST
    assert out.exists() and not test.exists()
    release=load(root/'registered_release_verification.json')
    complete=load(root/'completion_checkpoint.json')
    assert complete['counts']==dict(completed=24475,revised=14600,retained=9875)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(726,114,61)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    registry=Path('translations/release_stack.json');assert digest(registry)==release['registry_sha256']
    assert load(root/'release_stack_before_Lil382.json')['latest_promoted_build']==load(registry)['latest_promoted_build']
    for key in ['candidate','manifest','patch','own_registered_startup','own_registered_name_getters','exact_record_bindings']:
        assert digest(release[key])==release[key+'_sha256']
    assert gzip.decompress((out/'build_manifest.json.gz').read_bytes())==Path(release['manifest']).read_bytes()
    assert gzip.decompress((out/'build_release_stack.json.gz').read_bytes())==registry.read_bytes()
    assert digest(out/'translation.xdelta')==release['patch_sha256']
    code=Path(previous.__file__).read_text(encoding='utf-8')
    # Reconstruct the expected prefix file map from the frozen producer's declarations.
    start=code.index('    proofs=[');end=code.index('    TEST.mkdir()',start)
    prefix=code[start:end]
    namespace={**previous.__dict__,'v':out/'verification','rp':root/'registered_release_verification.json',
        'release':release,'reportpath':Path('work/lil382_repository_qa_v3/pytest.xml')}
    namespace['producers']=sorted(set(Path('scripts').glob('*lil382*.py'))|{Path('dk4tool/patch/lil382_release_v1.py'),Path('dk4tool/script/reviewed_credited_context_rebuild_v1.py')})
    # The original repository receipt remains frozen; verify its recorded producer bytes.
    repository=load(out/'verification/repository_checks.json')
    assert (repository['passing_tests'],repository['terminal_exit_code'])==(27,0)
    for p,h in repository['active_producers_parsed'].items():assert digest(p)==h
    import ast
    node=ast.parse('def prefix():\n'+prefix).body[0]
    expected={}
    for stmt in node.body:
        if isinstance(stmt,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='proofs' for t in stmt.targets):
            exec(compile(ast.Module(body=[stmt],type_ignores=[]),'<frozen-proof-declarations>','exec'),namespace)
    for p in namespace['proofs']:expected['verification/'+p.name]=p
    for p,name in [(previous.EDITORIAL/'registered_semantic_checks_v1/qualification.json','production_scope_rejections.json'),
                   (previous.EDITORIAL/'loaders_v1/verification.json','native_loaders.json'),
                   (previous.EDITORIAL/'stored_catalogue_all_v1/all_stored_effective_body_bindings.json','stored_catalogue.json')]:expected['verification/'+name]=p
    for name,p in expected.items():assert (out/name).read_bytes()==p.read_bytes()
    actual={str(p.relative_to(out)).replace('\\','/') for p in out.rglob('*') if p.is_file()}
    assert actual==set(expected)|{'translation.xdelta','build_manifest.json.gz','build_release_stack.json.gz','verification/repository_checks.json'}
    return release,registry


if __name__=='__main__':
    release,registry=verify_prefix()
    code=Path(previous.__file__).read_text(encoding='utf-8')
    tail=code[code.index('    TEST.mkdir()'):code.index("\n\n\nif __name__")]
    env={**previous.__dict__,'release':release,'registry':registry,'v':previous.OUT/'verification',
         'patch':previous.OUT/'translation.xdelta','rp':previous.ROOT/'registered_release_verification.json','__file__':__file__}
    exec(compile('def resume():\n'+tail,__file__+'::same-package-continuation-after-verified-prefix','exec'),env)
    env['resume']()
