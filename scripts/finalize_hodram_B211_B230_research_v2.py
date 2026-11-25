"""Add the required public-name schema without changing any scoped editorial decision."""
import inspect
from pathlib import Path
from scripts import finalize_hodram_B211_B230_research_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "    for row in names['records']:\n        row['review']['formatting']=True":
        """    for row in names['records']:
        row.update(id=f'ACTOR_NAME_{row["actor_ID"]:03d}',speaker='Speaker name or role',
            context='Source-qualified speaker in complete Hodram B211–B230 exchanges; exact contextual record IDs remain listed on this record.',
            source_meaning=' '.join(f['text'] for column in (0,8,4) for f in row['clean_fields'] if f['column']==column).strip())
        row['review']['formatting']=True""",
    "names.update(encoder='dialogue-relocatable-v1',all_five_gates_pass_in_scoped_context=True,":
        "names.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],all_five_gates_pass_in_scoped_context=True,",
    "for p in (*paths,Path(__file__))}":"for p in (*paths,Path(__file__),Path(previous.__file__))}",
})
env={**vars(previous),'previous':previous,'__file__':__file__,'OUT':previous.ROOT/'research_final_v2','READY':previous.ROOT/'research_final_v2/research_completion.json'}
exec(compile(source,__file__+'::same-five-gate-seal-with-complete-public-name-schema','exec'),env)
if __name__=='__main__':env['main']()
