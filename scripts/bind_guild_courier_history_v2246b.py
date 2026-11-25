"""Use each historical build's registered parser; preserve failed2246."""
from pathlib import Path
from dk4tool.patch import item_diplomacy_editorial,arrival_notices_editorial
source=Path('scripts/bind_guild_courier_history_v2246.py').read_text(encoding='utf-8')
source=source.replace("guild_courier_history_v2246'","guild_courier_history_v2246b'")
old="common_message_entries(prior.read_file('/COMMON/MESFILE.DK4'),prior.read_file('/__arm9__.bin'),clean=False)"
new="(item_diplomacy_editorial if group<2 else arrival_notices_editorial).current_entries(prior.read_file('/COMMON/MESFILE.DK4'),prior.read_file('/__arm9__.bin'))"
assert source.count(old)==1
source=source.replace(old,new)
exec(compile(source,__file__,'exec'),globals())
