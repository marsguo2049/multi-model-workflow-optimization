from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from mmwo.capabilities import ModelCall


class AssetKind(str, Enum):
    IMAGE_PLACEHOLDER = "image_placeholder"
    VIDEO_PLACEHOLDER = "video_placeholder"
    IMAGE = "image"
    VIDEO = "video"


@dataclass
class Asset:
    asset_id: str
    kind: AssetKind
    uri: str
    source_reference: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["kind"] = self.kind.value
        return data


@dataclass
class Shot:
    shot_id: str
    index: int
    description: str
    prompt: str | None = None
    keyframe_asset_id: str | None = None
    clip_asset_id: str | None = None


@dataclass
class Storyboard:
    story: str
    shots: list[Shot]

    def to_dict(self) -> dict[str, Any]:
        return {"story": self.story, "shots": [asdict(shot) for shot in self.shots]}


@dataclass
class EvaluationRecord:
    output_reference: str
    accepted: bool
    scores: dict[str, float]
    notes: str


@dataclass
class WorkflowRun:
    run_id: str
    task_id: str
    storyboard: Storyboard
    status: str = "running"
    calls: list[ModelCall] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    evaluations: list[EvaluationRecord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "storyboard": self.storyboard.to_dict(),
            "status": self.status,
            "calls": [call.to_dict() for call in self.calls],
            "assets": [asset.to_dict() for asset in self.assets],
            "evaluations": [asdict(record) for record in self.evaluations],
            "metadata": self.metadata,
        }
