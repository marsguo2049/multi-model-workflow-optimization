from __future__ import annotations

import argparse
from pathlib import Path

from mmwo.providers.mock import MockEvaluationProvider, MockImageProvider, MockPromptProvider, MockVideoProvider
from mmwo.workflow import StoryToVideoWorkflow


def build_mock_workflow() -> StoryToVideoWorkflow:
    return StoryToVideoWorkflow(MockPromptProvider(), MockImageProvider(), MockVideoProvider(), MockEvaluationProvider())


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic mock Story-to-Video workflow")
    parser.add_argument("story", help="One story sentence")
    parser.add_argument("--output", type=Path, default=Path("outputs/demo"))
    args = parser.parse_args()
    run = build_mock_workflow().run(args.story, args.output)
    print(f"Mock workflow {run.status}: {args.output}")
    print("No image or video media was generated.")


if __name__ == "__main__":
    main()
