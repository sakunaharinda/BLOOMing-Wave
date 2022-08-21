from h2o_wave import Expando


def validate_inputs(args: Expando):
    token = args.token
    model = args.model_drop
    top_k = args.top_k
    top_p = args.top_p
    temperature = args.temperature
    max_new_tokens = args.max_new_tokens
    return_full_text = args.return_full_text
    do_sample = args.do_sample
    task = args['#']

    if token == '':
        return ["token is mandatory", task, model, token, get_params()]

    if top_k == '':
        top_k = None
    elif top_k.isdigit():
        top_k = int(top_k)
    else:
        return ["top_k should be an integer", task, model, token, get_params()]

    if top_p == '':
        top_p = None
    elif is_float(top_p):
        top_p = float(top_p)
    else:
        return ["top_p should be a float", task, model, token, get_params()]

    if max_new_tokens == '':
        max_new_tokens = 1
    elif max_new_tokens.isdigit() and 0 <= int(max_new_tokens) <= 250:
        max_new_tokens = int(max_new_tokens)
    else:
        return ["max_new_token should be an integer between 0 and 250", task, model, token, get_params()]

    return [None, task, model, token, get_params(
        top_k,
        top_p,
        temperature,
        max_new_tokens,
        return_full_text,
        do_sample
    )]


def get_params(top_k=0, top_p=0.0, temperature=0, max_new_tokens=0, return_full_text=False, do_sample=False):
    return {
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
        "return_full_text": return_full_text,
        "do_sample": do_sample
    }


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
