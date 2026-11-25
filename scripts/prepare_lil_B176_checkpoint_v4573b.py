"""Use the inventory's integer typed-command counts; preserve the initial producer."""
from pathlib import Path
source=Path(__file__).with_name('prepare_lil_B176_checkpoint_v4573.py')
text=source.read_text(encoding='utf-8')
old="len(b['typed_menu_2100_commands'])+len(b['typed_actor_style_4100_commands'])"
assert text.count(old)==1
text=text.replace(old,"b['typed_menu_2100_commands']+b['typed_actor_style_4100_commands']")
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
