# Story-to-Video demo

The baseline accepts one story sentence and constructs an inspectable four-shot workflow. In mock mode it emits:

- `storyboard.json`
- four `keyframe-*.placeholder.json` records
- three `clip-*.placeholder.json` records
- `run.json` with call metadata and state
- `summary.json` explicitly stating that no media was generated

The demo validates planning order, prompt changes between shots, asset references, evaluation boundaries, and reproducibility. It does not create fake image or video bytes.

Real backends should preserve the same state model. The separate [comfyui-py-workflow](https://github.com/marsguo2049/comfyui-py-workflow) project already provides reusable local ComfyUI execution primitives: it loads portable API-format workflows, substitutes prompts and input references, submits jobs, polls history, and collects generated assets. A future integration here should adapt those results to this framework's `Asset` and `ModelCall` records rather than duplicating the runner.
