from model.inference import infer


def get_gen(prompt: str, model: str, token: str, params: dict):
    resp, error = infer(prompt, model, token, params)
    if error is None:
        return resp, None
    else:
        return None, error
