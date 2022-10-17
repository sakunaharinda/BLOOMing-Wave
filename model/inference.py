from huggingface_hub import InferenceApi
import time
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')


def infer(prompt: str, model: str, token: str, params: dict):
    inference = InferenceApi(model, token=token)
    s = time.time()
    response = inference(prompt, params=params)
    proc_time = time.time() - s

    if isinstance(response, list):
        logging.info(f"Processing time was {proc_time} seconds")
        logging.info(response)
        return response[0]['generated_text'], None
    elif 'error' in response:
        print("\n\n")
        print(response['error'])
        logging.error(response['error'])
        return None, response['error']
    else:
        logging.warning(response)
        return None, response
