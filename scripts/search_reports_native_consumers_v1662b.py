"""Record both loaded template and post-printf input for two-amount speech."""
import inspect
from scripts import search_reports_native_consumers_v1662 as previous
assigned_role, loss = previous.assigned_role, previous.loss
source = inspect.getsource(previous.speech)
needle = "    return {**seen, 'role': role"
replacement = "    seen['loaded_template_hex'] = bytes(cpu.mem_read(provider.output, 512)).split(b'\\0')[0].hex()\n" + needle
assert source.count(needle) == 1
source = source.replace(needle, replacement)
env = dict(previous.__dict__)
exec(compile(source, __file__, 'exec'), env)
speech = env['speech']
