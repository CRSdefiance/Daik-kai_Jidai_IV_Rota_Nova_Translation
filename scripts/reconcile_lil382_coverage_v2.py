"""Keep exact credited context when a remaining exchange is only partly unreviewed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/reconcile_lil382_coverage_v1.py').read_text(encoding='utf-8'), {
    "            assert all(not r['covered'] for r in rows),'Next intake must account for a partially credited exchange'\n            groups.append({**g,'records':rows,'missing_source_objects':len(rows)})":
        """            remaining=[r for r in rows if not r['covered']]
            context=[r for r in rows if r['covered']]
            assert all(r['exact_credited_source_bindings'] and all((r['file_path'],b['id']) in keys for b in r['exact_credited_source_bindings']) for r in context)
            groups.append({**g,'records':remaining,'missing_source_objects':len(remaining),
                'complete_clean_context_records':rows,'preserved_credited_context_records':context,
                'covered_context_not_new_review_scope':True})""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-exact-source-position-census-explicit-credited-context','exec'),globals())
