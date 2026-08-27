# Research roadmap

## Phase 0 — foundation

Define positioning, typed capability interfaces, mock providers, state models, offline tests, and documentation.

## Phase 1 — Story-to-Video MVP

Integrate real providers for story planning, image generation, and video generation. Reuse independently maintained execution backends such as [comfyui-py-workflow](https://github.com/marsguo2049/comfyui-py-workflow), produce four keyframes and three short clips, stitch them, and retain complete run metadata.

## Phase 2 — alternatives

Add at least two alternatives for one capability and vary meaningful parameters. Record measured runtime, cost or compute, failures, and evaluation outputs without inventing missing values.

## Phase 3 — evaluation and benchmark

Create a versioned task set, reproducible configurations, repeated runs, and human and/or automated evaluation. Report uncertainty and evaluator limitations.

## Phase 4 — model routing

Compare rules, supervised routing, contextual bandits, Bayesian optimization, and simple multi-armed bandit baselines for selecting a model and configuration from task context.

## Phase 5 — workflow optimization

Jointly consider workflow structure, model per node, parameters, compute budget, branching, retry policy, and stopping criteria.

## Phase 6 — agent-system integration

Expose the optimizer as a resource-decision layer for a larger agent system that decomposes tasks into required capabilities.
