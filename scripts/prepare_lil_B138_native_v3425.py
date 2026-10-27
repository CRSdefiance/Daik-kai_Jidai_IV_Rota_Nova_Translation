"""Prepare seven current names and complete clean-only B138 branch context."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    def make(a,b,changes):
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    shared=[('work/analysis/lil_remaining_B137_B140_source_v3380b/next48_B137_clean_current_context.json','work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')]
    make('scripts/reconcile_lil_B137_voices_v3383b.py','scripts/reconcile_lil_B138_voices_v3425.py',shared+[
        ('Bind eight current static speakers','Bind seven current static speakers'),('lil_B137_voices_v3383b','lil_B138_voices_v3425'),('chosen==[2,9,14,16,17,20,22,23,38,92,198]','chosen==[2,14,20,21,22,23,92]'),('eleven','seven'),('Eleven','Seven'),('selected48','selected44'),('all48','all44')])
    make('scripts/prepare_lil_B137_clean_review_v3385.py','scripts/prepare_lil_B138_clean_review_v3427.py',shared+[
        ('lil_B137_clean_transcripts_v3385','lil_B138_clean_transcripts_v3427'),('lil_B137_branches_v3385b','lil_B138_branches_v3427b'),('full_commands=117,source_speeches=48','full_commands=111,source_speeches=44'),('all48_complete_source_preambles','all44_complete_source_preambles'),('complete_clean_transcript_blocks=[137],source_speeches=48,labels=0,commands=117','complete_clean_transcript_blocks=[138],source_speeches=44,labels=0,commands=111')])
    root=Path('work/analysis/lil_B138_native_tools_v3425');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],all_previous_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
