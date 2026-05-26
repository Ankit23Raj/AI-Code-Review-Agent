def log(message, level="INFO"):
    # Keep logging simple so beginners can follow what happens in each step.
    print(f"[{level}] {message}", flush=True)


def log_error(message):
    log(message, level="ERROR")