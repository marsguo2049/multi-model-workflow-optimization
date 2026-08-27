import json

from mmwo.demo import build_mock_workflow


def test_mock_story_to_video_pipeline(tmp_path) -> None:
    run = build_mock_workflow().run("A lantern guides a boat home.", tmp_path)
    assert run.status == "succeeded"
    assert len(run.storyboard.shots) == 4
    assert len([asset for asset in run.assets if asset.kind.value == "image_placeholder"]) == 4
    assert len([asset for asset in run.assets if asset.kind.value == "video_placeholder"]) == 3
    assert len(run.calls) == 18
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary["media_generated"] is False
    assert not list(tmp_path.glob("*.png"))
    assert not list(tmp_path.glob("*.mp4"))
