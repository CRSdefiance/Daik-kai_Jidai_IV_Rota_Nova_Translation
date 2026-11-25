"""Supply exact current record-index metadata to the unchanged complete-block rebuilder."""
from dk4tool.patch import rafael_story_b121_b140_release_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

qualify_evidence = previous.qualify_evidence
source = checked_text(previous.source, {
    "        rows = [r for r in speech if r['block'] == number and r.get('native_object_kind') != '4100-style-alternative']":
        """        rows = [deepcopy(r) for r in speech if r['block'] == number and r.get('native_object_kind') != '4100-style-alternative']
        for row in rows:
            index=row['current_reference']['record_index']
            require(row.get('current_record_index',index)==index,'exact current reference index')
            row['current_record_index']=index""",
})
env = {**previous.plan_release.__globals__, 'qualify_evidence': qualify_evidence}
exec(compile(source, __file__+'::unchanged-rebuild-exact-current-reference-index-adapter', 'exec'), env)
plan_release = env['plan_release']
