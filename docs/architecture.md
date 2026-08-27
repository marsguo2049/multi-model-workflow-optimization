# Architecture

The framework separates workflow orchestration from capability execution.

1. A task enters the Python orchestrator.
2. The orchestrator requests capabilities through typed protocols.
3. A registry resolves a capability to a provider.
4. Providers call a mock or an independently maintained execution backend.
5. Results and measured metadata flow back into workflow state.
6. Evaluators may accept, reject, or annotate results; retry policy remains in the orchestrator.

This boundary keeps vendor names and backend graph details out of high-level workflow code. Backend workflow graphs are execution templates, not the top-level application state machine.

## Core records

- `ModelCall`: capability, provider, model, configuration, timing, status, cost, and metadata
- `Asset`: a reference to a text, image, video, or placeholder artifact
- `Shot` and `Storyboard`: structured planning state
- `EvaluationResult`: explicit measured or mock evaluation output
- `WorkflowRun`: task state, calls, assets, evaluations, and final status

Values that have not been measured remain absent or `null`. Provider output references can point to local portable artifacts, remote objects, or backend-specific identifiers.

## Provider boundary

Provider implementations are replaceable and may expose text, prompt, image, video, or evaluation capabilities. The initial mocks are deterministic. The separately maintained [comfyui-py-workflow](https://github.com/marsguo2049/comfyui-py-workflow) project can serve as a concrete local ComfyUI execution backend without coupling this research framework to particular workflow graphs.
