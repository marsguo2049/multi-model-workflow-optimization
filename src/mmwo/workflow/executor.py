from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mmwo.capabilities import (
    EvaluationProvider,
    EvaluationRequest,
    ImageGenerationProvider,
    ImageGenerationRequest,
    PromptGenerationProvider,
    PromptRequest,
    VideoGenerationProvider,
    VideoGenerationRequest,
)

from .state import Asset, AssetKind, EvaluationRecord, Shot, Storyboard, WorkflowRun


def _id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class StoryToVideoWorkflow:
    def __init__(
        self,
        prompt_provider: PromptGenerationProvider,
        image_provider: ImageGenerationProvider,
        video_provider: VideoGenerationProvider,
        evaluator: EvaluationProvider,
    ) -> None:
        self.prompt_provider = prompt_provider
        self.image_provider = image_provider
        self.video_provider = video_provider
        self.evaluator = evaluator

    def run(self, story: str, output_dir: str | Path) -> WorkflowRun:
        story = story.strip()
        if not story:
            raise ValueError("story must not be empty")
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        task_id = _id("task", story)
        run = WorkflowRun(
            run_id=_id("run", f"mock-v1:{story}"),
            task_id=task_id,
            storyboard=self._storyboard(story),
            metadata={"mode": "mock", "media_generated": False},
        )

        for shot in run.storyboard.shots:
            prompt_result = self.prompt_provider.generate_prompt(PromptRequest(
                task_id=task_id, story=story, shot_index=shot.index, shot_description=shot.description,
            ))
            shot.prompt = prompt_result.prompt
            run.calls.append(prompt_result.call)
            image_result = self.image_provider.generate_image(ImageGenerationRequest(
                task_id=task_id, prompt=shot.prompt, seed=1000 + shot.index,
            ))
            run.calls.append(image_result.call)
            filename = f"keyframe-{shot.index + 1}.placeholder.json"
            _write_json(destination / filename, {
                "kind": "image_placeholder", "source_reference": image_result.output_reference,
                "notice": "Mock record only; no image bytes were generated.",
            })
            asset = Asset(_id("asset", filename), AssetKind.IMAGE_PLACEHOLDER, filename, image_result.output_reference, {"shot_index": shot.index})
            shot.keyframe_asset_id = asset.asset_id
            run.assets.append(asset)
            self._evaluate(run, image_result.output_reference, "image_generation")

        for index in range(len(run.storyboard.shots) - 1):
            start_asset = run.assets[index]
            end_asset = run.assets[index + 1]
            shot = run.storyboard.shots[index]
            video_result = self.video_provider.generate_video(VideoGenerationRequest(
                task_id=task_id,
                prompt=f"Transition from shot {index + 1} to shot {index + 2}: {shot.prompt}",
                start_image_reference=start_asset.source_reference,
                end_image_reference=end_asset.source_reference,
                seed=2000 + index,
            ))
            run.calls.append(video_result.call)
            filename = f"clip-{index + 1}.placeholder.json"
            _write_json(destination / filename, {
                "kind": "video_placeholder", "source_reference": video_result.output_reference,
                "notice": "Mock record only; no video bytes were generated.",
            })
            asset = Asset(_id("asset", filename), AssetKind.VIDEO_PLACEHOLDER, filename, video_result.output_reference, {"from_shot": index, "to_shot": index + 1})
            shot.clip_asset_id = asset.asset_id
            run.assets.append(asset)
            self._evaluate(run, video_result.output_reference, "video_generation")

        run.status = "succeeded"
        _write_json(destination / "storyboard.json", run.storyboard.to_dict())
        _write_json(destination / "run.json", run.to_dict())
        _write_json(destination / "summary.json", {
            "status": run.status,
            "shots": len(run.storyboard.shots),
            "keyframe_records": 4,
            "clip_records": 3,
            "media_generated": False,
            "mode": "mock",
        })
        return run

    def _evaluate(self, run: WorkflowRun, output_reference: str, capability: str) -> None:
        result = self.evaluator.evaluate(EvaluationRequest(
            task_id=run.task_id, capability_under_test=capability, output_reference=output_reference,
        ))
        run.calls.append(result.call)
        run.evaluations.append(EvaluationRecord(output_reference, result.accepted, result.scores, result.notes))

    @staticmethod
    def _storyboard(story: str) -> Storyboard:
        beats = (
            "Establish the setting and protagonist",
            "Introduce the central action or obstacle",
            "Show the decisive change",
            "Resolve on a clear final image",
        )
        return Storyboard(story=story, shots=[Shot(f"shot-{i + 1}", i, beat) for i, beat in enumerate(beats)])
