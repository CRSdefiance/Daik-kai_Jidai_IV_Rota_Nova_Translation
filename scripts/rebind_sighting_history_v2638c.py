"""Strengthen argument negatives to executed native pipelines and RGB rejection."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_sighting_history_v2638.py').read_text();source=source.replace("shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']","shots={r.get('frame',returned):r for r in report['read_only_capture_RAM_snapshots']")
 old="negative.append(dict(run=run,message_id=n,kind=label+'-argument-byte',rejected=True))"
 new="wrong_arguments=[b'X'+bearing[1:]if label=='bearing'else bearing,b'X'+faction[1:]if label=='full-faction'else faction];wrong_native=ctx.execute(speech,1,table,wrong_arguments);wrong_pixels=ctx.raster(arm,bytes.fromhex(wrong_native['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000);negative.append(dict(run=run,message_id=n,kind=label+'-argument-byte',rejected=not masks_match(screen,wrong_pixels),current_original_CPU_pipeline_executed=True))"
 assert source.count(old)==1;source=source.replace(old,new).replace('sighting_history_v2638','sighting_history_v2638c')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
