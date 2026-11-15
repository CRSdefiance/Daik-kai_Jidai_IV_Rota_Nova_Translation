"""Resume exact partial packaging and bind the completed all-history syntax diagnostic."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/package_maria363_candidate_v1.py').read_text(encoding='utf-8'),{
    'assert not OUT.exists()':"assert OUT.exists() and {p.name for p in OUT.iterdir()} == {'verification','translation.xdelta','build_manifest.json.gz','build_release_stack.json.gz'}",
    "OUT.mkdir();verification=OUT/'verification';verification.mkdir()":"verification=OUT/'verification';assert verification.is_dir()",
    """    syntax_failures=[]
    for p in Path('scripts').glob('*.py'):
        try:ast.parse(p.read_bytes(),filename=str(p))
        except (SyntaxError,UnicodeError) as e:syntax_failures.append(dict(path=str(p),error=str(e)))
    assert len(syntax_failures)==18""":
    """    diagnostic=Path('work/github_candidate_qa_20261110/all_scripts_syntax_v1.json')
    syntax_failures=load(diagnostic)['failures']
    assert len(syntax_failures)==37 and load(diagnostic)['parsed']==16627
    (verification/'all_scripts_syntax_v1.json').write_bytes(diagnostic.read_bytes())""",
    'Eighteen historical failed producer scripts':'Thirty-seven historical failed producer scripts',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-release-gates-resume-partial-package-andexact-diagnostic-scope','exec'),globals())
