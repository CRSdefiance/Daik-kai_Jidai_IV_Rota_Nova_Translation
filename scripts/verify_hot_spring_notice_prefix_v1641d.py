"""Map the prior terminal capture to the same-frame live navigation capture."""
import inspect
from scripts import verify_hot_spring_notice_prefix_v1641c as previous
if __name__=='__main__':
    source=inspect.getsource(previous)
    old='new=NEW/old.name'
    new="new=NEW/(f\"frame_{row['frame']:06d}_navigation.png\" if old.name.endswith('_final.png') else old.name)"
    assert source.count(old)==1;source=source.replace(old,new)
    source=source.replace('work/analysis/hot_spring_notice_prefix_v1641c','work/analysis/hot_spring_notice_prefix_v1641d')
    source=source.replace("'prefix_through13600_including_discovery_recovery_returns_and_rats_exact':True", "'prior_terminal_final_capture_compared_to_same_frame_current_navigation_capture':True,'prefix_through13600_including_discovery_recovery_returns_and_rats_exact':True")
    env={**previous.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
