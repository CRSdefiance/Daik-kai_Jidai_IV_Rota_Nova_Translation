"""Prepare seven current names and the complete67-speech clean-only context."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    def make(old,new,changes):
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append((a,b))
    shared=[('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json','work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')]
    make('scripts/reconcile_lil_B138_voices_v3425.py','scripts/reconcile_lil_B139_B140_voices_v3460.py',shared+[
        ('lil_B138_voices_v3425','lil_B139_B140_voices_v3460'),('chosen==[2,14,20,21,22,23,92]','chosen==[2,4,9,16,20,21,171]'),('selected44','selected67'),('all44','all67')])
    make('scripts/prepare_lil_B138_clean_review_v3427.py','scripts/prepare_lil_B139_B140_clean_review_v3463.py',shared+[
        ('lil_B138_clean_transcripts_v3427','lil_B139_B140_clean_transcripts_v3463'),('lil_B138_branches_v3427b','lil_B139_B140_branches_v3463b'),('full_commands=111,source_speeches=44','full_commands=146,source_speeches=67'),('all44_complete_source_preambles','all67_complete_source_preambles'),('complete_clean_transcript_blocks=[138],source_speeches=44,labels=0,commands=111','complete_clean_transcript_blocks=[139,140],source_speeches=67,labels=0,commands=146')])
    root=Path('work/analysis/lil_B139_B140_native_tools_v3460');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],all_earlier_sources_and_translations_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
