from __future__ import annotations
from typing import Any
from village_rain_fusion.geo.runtime import RunState, SQLiteLedger, fingerprint, number, sequence

class FusionCoordinator:
    artifact_key = 'fusion_consensus'

    def execute(self, state: RunState, stages: list[Any], ledger: SQLiteLedger) -> None:
        branches = {"geometry": [], "signals": [], "confidence": []}
        for position in (0, 1, 2):
            stages[position].apply(state)
            branches["geometry" if position == 0 else "signals"].append(stages[position].name)
            ledger.save(state)
        seed_scores = [state.artifacts[name]["score"] for name in branches["geometry"] + branches["signals"]]
        consensus = sum(seed_scores) / max(len(seed_scores), 1)
        for position in (3, 4, 5, 6):
            stages[position].apply(state)
            branches["confidence"].append(stages[position].name)
            ledger.save(state)
        final_scores = [state.artifacts[name]["score"] for name in branches["confidence"]]
        state.artifacts[self.artifact_key] = {"branches": branches, "seed_consensus": round(consensus, 6), "final_consensus": round(sum(final_scores) / max(len(final_scores), 1), 6), "signature": fingerprint(branches)}
        state.emit(self.artifact_key, "fusion_completed", branches=len(branches))
