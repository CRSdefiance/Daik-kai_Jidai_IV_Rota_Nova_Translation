# V727: original route action tables and script-buffer sources

V726 made progress by binding the numeric CHARA evidence and completing the
current stored-block census. This checkpoint investigates a different remaining
lead: commands generated while original event scripts enter their native buffer.
V712 remains unchanged.

## Original source selection

The original `CEventScriptBuffer` class names four SC archive files. The original
event action selector reads the EV action word, separates its kind/index, and
constructs the script buffer before calling the complete native loader.

| Route | SC blocks referenced | Null action words | Inline script section |
|---|---:|---:|---|
| 0 | 343 | 1 | Empty |
| 1 | 325 | 1 | Empty |
| 2 | 336 | 2 | Empty |
| 3 | 303 | 1 | Empty |
| Total | 1,307 | 5 | All four empty |

All kind-2 action words select the complete sequence of SC block indices exactly
once. The bounded action-table regions contain no kind-1 inline script requests.
Each EV header's inline-script offset equals the end of its body.

## Native checks in clean and V712

Each case supplies the original file-backed EV header/body and the selector
fragment's input registers. The fragment starts at `02023EA4`; it executes the
original pointer arithmetic, kind/index selection and child constructor, stopping
at the actual loader call or null-action continuation. This is supplied input,
not a claimed ordinary trigger or complete enclosing event execution.

The complete original SC-buffer loader then executes through the game's original
ILNK reader. Only SDK Open/Read/Seek/Close are bridged to exact ROM bytes. The
bridge explicitly records the original uppercase request and its resolved ROM
path. It does not replace the archive parser, block selector or buffer copy.

Across both ROMs:

- All 2,624 action-selector cases take the expected branch.
- All 2,614 non-null cases load the entire exact selected SC block.
- All 2,614 repeated cache hits perform no file I/O and preserve the complete
  cached object and neighboring bytes.
- Every whole loader call returns with the original saved registers, SP and PC.
  Source EV bytes, buffer prefix/tail guards and original vtable remain intact.
- Every executed native instruction outside the SDK bridges matches mapped ROM
  code. The relevant selector, constructor, loader, filenames and archive-reader
  ranges are also byte-exact between clean and V712.
- No village-card event-still opcode byte candidate occurs anywhere in any
  returned SC payload, using the original bit-15/low-byte pattern contract.

Returned script streams are exact source blocks. This original buffer-loading
path does not supply different generated command streams. Its source-backed
result complements V589's operand/census work; it does not establish global
non-use, other stream builders, post-load modification or arbitrary indirect
consumers. Those distinctions remain in the active ordinary-context work.

## Research corrections

An initial SDK bridge lookup used host path case literally and rejected the
original uppercase DATA request. The final bridge records its explicit mapping
to the existing ROM path. An initial selector fragment began after the header
offset load; the corrected entry includes that original load. Constructor cache
state is read from the original literal (`00000FFF`), rather than an assumed
all-ones sentinel. These were probe contract errors corrected before the final
complete run, not failures of a ROM candidate.

## Audit and remaining work

This closes the bounded original route script-buffer generation lead. Do not
repeat it to seek an ordinary village card or comic viewer. Normal card
reachability, the raw comic viewer and other legacy/native contexts remain open;
no new GPU image, complete story event or playthrough is credited.

The exact current proof, route/action records and documentation are archived at
`E:/Rota Nova translations/Screenshots/Audit comparisons/V727 Event script sources`.
This archive has evidence records, not new screenshots. All eighteen original
plaque/hint entries remain incomplete and the twenty-two historical objects stay
exact. Exclusions, approved art decisions and the older-record follow-up remain.

V712 ROM, manifest, patch, registry and canonical hashes are unchanged. The full
graphics goal remains active; no new release, promotion, commit or push is made.
