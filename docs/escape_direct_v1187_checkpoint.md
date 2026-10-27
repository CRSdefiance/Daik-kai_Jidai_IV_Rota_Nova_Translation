# Direct escape formatting: V1187 erratum and native correction

Original V1166 gameplay after the isolated low-positive-HP, unarmored test
duel selects COMMON1973. Captures6912/6922 show “Everyone” split across the
physical edge as “Ever” / “yone”. The original formatted buffer at0228E5A8
still contains the unwrapped paragraph. These two real holds contradict the
earlier escape-format approval based on a manually assumed queued frame.

The original53F0C ->54058 prologue proves parent02053F40, voice-table field
+274 and high word0211. The previous53DB8/+27C membership was wrong for
this consumer. The successor removes those two erroneous queued memberships
and adds only direct tables02117500/02117620. All33 English paragraphs,
Japanese glosses, substitutions and compiled COMMON bytes remain unchanged.

The172-byte gate and212-byte public bank remain within their original owned
allocations. A failed regression caught the live PC-relative status suffix
constant in the old gate tail. Its exact pointer is retained in the unused
end of the44-byte status-tail allocation; both the load and its literal are
source locked. Incoming branch/absolute/PC-relative accesses are audited.
The failed1184 probe and successors are retained; it was never a ROM release.

Corrected native evidence:122324 exact dispatch/register/stack cases,
3668 modal outputs plus238 wrong-parent and5 boundary controls,140 complete
status-memory contracts,1417 escape-name/full-native-font cases, and13
original direct source-call pipelines with416 unchanged voice selections.
The native-font sheet was visually reviewed for complete words, first/last
letters, margins and bounds. File I/O and portrait UI construction remain
explicit CPU-test boundaries. Actual combined-ROM gameplay is still required.

The20 static duel entries remain complete on their existing independent
evidence. All13 escape entries remain incomplete. Counts stay1216 complete
(904 revised,312 retained),1267 source/prose reviewed,51 reviewed COMMON
entries incomplete. Separate graphics work, all18 plaques, the remaining
shared/routes/raw-source inventory and the older-record re-audit remain open.
The full editorial goal remains active; no canonical promotion is authorized.

Proof: `work/analysis/escape_binding_erratum_v1187/actual_failure_and_native_successor.json`.
