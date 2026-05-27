import importlib

from app.utils.logger import log


PIPELINE_CANDIDATES = (
    ("app.agents.ai_pipeline", "review"),
    ("app.reviewer.ai_pipeline", "review"),
    ("app.ai_pipeline", "review"),
)


def _load_pipeline_callable():
    for module_name, attribute_name in PIPELINE_CANDIDATES:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue

        pipeline_callable = getattr(module, attribute_name, None)
        if callable(pipeline_callable):
            return pipeline_callable

    return None


def send_for_review(payload, review_callable=None, mock_mode=False):
    log("Sending payload to AI pipeline")

    try:
        if mock_mode:
            findings = {"findings": []}
        else:
            pipeline_callable = review_callable or _load_pipeline_callable()
            if pipeline_callable is None:
                raise RuntimeError("AI pipeline review callable is unavailable")

            findings = pipeline_callable(payload)

        if findings is None:
            findings = {"findings": []}

        if isinstance(findings, list):
            findings = {"findings": findings}

        log("AI findings received")
        return findings
    except Exception as e:
        log(f"Failed to process payload: {e}", level="ERROR")
        raise