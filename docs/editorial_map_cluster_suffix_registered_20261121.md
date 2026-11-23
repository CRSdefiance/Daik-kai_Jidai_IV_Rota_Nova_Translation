# World Map cluster labels and regional finance

The World Map now shows **Syracuse + more** and **Manuel Fleet + more** when entities share a marker. The eight-byte field preserves the original name and suffix substitutions and gives a plain marker just its name. [Source and installed references](../releases/all_routes_editorial_20261121_map_cluster_suffix_candidate/verification/registered_review.json)

The paired replay verified complete glyphs on the two-row town marker and one-row fleet marker. The Syracuse coordinates remained complete, and the single Stockholm marker was identical. Native formatting passed 20 cases and five stress examples fit the measured layout. The replay used a copy of an established regional fleet save. [Map marker comparison](../releases/all_routes_editorial_20261121_map_cluster_suffix_candidate/verification/world_map_label_comparison.png)

The regional fleet panel displayed its English finance fields independently of the stored Japanese finance format. All 276 shared references were rebound to the current review input, and the 35 priority strings had no verbatim duplicate outside COMMON in the clean ROM file inventory. Other display callers remain open. [Shared references and regional trace](../translations/editorial_checkpoints/SharedText_20261110_v1/shared_priority_and_regional_finance_20261121_v1.json)

Six startup holds, 24 protected getters and 17 focused tests passed. The clean-input patch reproduces the registered ROM byte for byte. [Candidate and patch](../releases/all_routes_editorial_20261121_map_cluster_suffix_candidate/README.md)

Checkpoint cleanup removed 14 failed or duplicate verification files totaling 61,931,926 bytes. [Local cleanup receipt](../work/map_cluster_suffix_20261121/checkpoint_cleanup.json)
