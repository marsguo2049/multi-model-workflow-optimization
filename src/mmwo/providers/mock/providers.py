from __future__ import annotations

import hashlib
from time import perf_counter

from mmwo.capabilities import (
    CallStatus,
    Capability,
    EvaluationRequest,
    EvaluationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    ModelCall,
    PromptRequest,
    PromptResponse,
    TextRequest,
    TextResponse,
    VideoGenerationRequest,
    VideoGenerationResponse,
)


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


def _call(
    *, task_id: str, capability: Capability, material: str, inputs: list[str],
    outputs: list[str], started: float, seed: int | None = None,
) -> ModelCall:
    return ModelCall(
        call_id=_stable_id("call", f"{capability.value}:{material}"),
        task_id=task_id,
        capability=capability,
        provider="mock",
        model="deterministic-mock-v1",
        configuration={},
        input_references=inputs,
        output_references=outputs,
        status=CallStatus.SUCCEEDED,
        runtime_ms=(perf_counter() - started) * 1000,
        seed=seed,
        cost_usd=None,
        compute=None,
        metadata={"mock": True},
    )


class MockTextProvider:
    def generate_text(self, request: TextRequest) -> TextResponse:
        started = perf_counter()
        text = f"Mock plan for: {request.prompt.strip()}"
        call = _call(task_id=request.task_id, capability=Capability.TEXT_GENERATION,
                     material=request.prompt, inputs=[request.prompt], outputs=[text], started=started)
        return TextResponse(text=text, call=call)


class MockPromptProvider:
    def generate_prompt(self, request: PromptRequest) -> PromptResponse:
        started = perf_counter()
        prompt = f"Shot {request.shot_index + 1}: {request.shot_description}. Story context: {request.story}"
        call = _call(task_id=request.task_id, capability=Capability.PROMPT_GENERATION,
                     material=prompt, inputs=[request.story, request.shot_description], outputs=[prompt], started=started)
        return PromptResponse(prompt=prompt, call=call)


class MockImageProvider:
    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        started = perf_counter()
        reference = f"mock://image/{_stable_id('asset', request.prompt)}"
        call = _call(task_id=request.task_id, capability=Capability.IMAGE_GENERATION,
                     material=request.prompt, inputs=[request.prompt, *request.input_references],
                     outputs=[reference], started=started, seed=request.seed)
        return ImageGenerationResponse(output_reference=reference, call=call)


class MockVideoProvider:
    def generate_video(self, request: VideoGenerationRequest) -> VideoGenerationResponse:
        started = perf_counter()
        material = f"{request.prompt}|{request.start_image_reference}|{request.end_image_reference}"
        reference = f"mock://video/{_stable_id('asset', material)}"
        inputs = [request.prompt, request.start_image_reference]
        if request.end_image_reference:
            inputs.append(request.end_image_reference)
        call = _call(task_id=request.task_id, capability=Capability.VIDEO_GENERATION,
                     material=material, inputs=inputs, outputs=[reference], started=started, seed=request.seed)
        return VideoGenerationResponse(output_reference=reference, call=call)


class MockEvaluationProvider:
    def evaluate(self, request: EvaluationRequest) -> EvaluationResponse:
        started = perf_counter()
        accepted = request.output_reference.startswith("mock://")
        notes = "Mock structural validation only; no perceptual quality was measured."
        call = _call(task_id=request.task_id, capability=Capability.EVALUATION,
                     material=f"{request.capability_under_test}:{request.output_reference}",
                     inputs=[request.output_reference], outputs=[str(accepted)], started=started)
        return EvaluationResponse(accepted=accepted, scores={}, notes=notes, call=call)
