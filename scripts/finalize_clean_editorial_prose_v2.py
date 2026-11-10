"""Retain all prose/name guards and bind the configured source archive explicitly."""
import inspect
from scripts import finalize_clean_editorial_prose_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "    proposals,names,terms,roles,objects=map(load,paths);runtime=proposals['runtime']":
        "    proposals,names,terms,roles,objects=map(load,paths);runtime=proposals['runtime']\n"
        "    assert cfg['file_path'] in ['/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4']\n"
        "    assert {r['file_path'] for r in proposals['records']}=={cfg['file_path']}",
    "review_gates=GATES,file_path='/data/SC3.DK4',blocks=":
        "review_gates=GATES,file_path=cfg['file_path'],blocks=",
    "        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())":
        """        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        row.update(source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=runtime['candidate'],candidate_sha256=runtime['candidate_sha256'],actor_ID=actor,original_consumers=row['current_consumers']))""",
})
env = {**vars(previous), '__file__': __file__}
exec(compile(source, __file__+'::same-individual-prose-andrejection-guards-explicit-source-archive', 'exec'), env)
if __name__ == '__main__':
    env['main']()
