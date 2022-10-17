from h2o_wave import Q, ui, main, app, handle_on, on
from lib.config import Config
from lib.validator import validate_inputs
from tasks.email_assist import get_email
from tasks.text_gen import get_gen

tabs = [
    ui.tab(name='#email', label='E-Mail Assistant', icon='Mail'),
    # ui.tab(name='#summarizer', label='Text Summarization', icon='KnowledgeArticle'),
    ui.tab(name='#text_gen', label='Text Generation', icon='EditNote')
]


@app('/bloom')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.initialized = True
        initialize(q)
    else:
        await handle_on(q)
    q.client.tab = str(q.args['#'])
    await main_view(q)
    await q.page.save()


async def main_view(q: Q):
    sample_message = "Switch off to use greedy decoding for more accurate completion " \
                     "e.g. math/history/translations (but which may be repetitive/less inventive)"
    greedy_message = "Switch on to use sampling for more imaginative completions " \
                     "e.g. story/poetry (but which may be less accurate)"

    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            breakpoint='xl',
            width='1200px',
            zones=[
                ui.zone('header'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('sidebar', size='32%'),
                    ui.zone('content', size='68%'),

                ]),
                ui.zone('footer'),
            ]
        )
    ], theme='h2o-dark')

    q.page['configs'] = ui.form_card(box=ui.boxes('sidebar'), items=[
        ui.textbox(name='token', label="Enter your huggingface token", value=q.args.token, password=True,
                   required=True),
        ui.separator("Model Configurations"),
        ui.dropdown(
            name='model_drop',
            label='Preferred BLOOM model',
            value=q.args.model_drop,
            choices=[ui.choice(name=m, label=m) for m in Config().bloom_versions],
            tooltip="BLOOM model to do the inference."
        ),
        ui.textbox(
            name='top_k',
            label='top_k',
            value=q.args.top_k,
            tooltip="Integer to define the top tokens considered within the sample operation to create new text."
        ),
        ui.textbox(
            name='top_p',
            label='top_p',
            value=q.args.top_p,
            tooltip="Float to define the tokens that are within the sample operation of text generation. "
                    "Add tokens in the sample for more probable to least probable until the sum of the "
                    "probabilities is greater than top_p."
        ),
        ui.slider(
            name='temperature',
            label='Temperature',
            min=0.0,
            max=1.0,
            step=0.1,
            value=q.args.temperature,
            tooltip="The temperature of the sampling operation. 1 means regular sampling, "
                    "0 means always take the highest score.",

        ),
        ui.textbox(
            name='max_new_tokens',
            label='Maximum token length',
            value=q.args.max_new_tokens,
            tooltip="Int (0-250). The amount of new tokens to be generated, "
                    "this does not include the input length it is a estimate of the size of generated text you want. "
                    "Each new tokens slows down the request, "
                    "so look for balance between response times and length of text generated."
        ),
        ui.choice_group(
            name="return_full_text",
            label="Return full text",
            choices=[
                ui.choice(name='True', label='True'),
                ui.choice(name='False', label='False')
            ],
            value=q.args.return_full_text,
            tooltip="If set to False, the return results will not contain the original "
                    "query making it easier for prompting."
        ),
        ui.toggle(name="do_sample", label="Sample", tooltip="Whether or not to use sampling, "
                                                            "use greedy decoding otherwise.", value=q.args.do_sample,
                  trigger=True),
        ui.message_bar(type='info', text=sample_message if q.args.do_sample else greedy_message),
        ui.message_bar(type='error', text=q.client.error, name='error_msg', visible=q.client.visible),
        ui.separator(),
        ui.buttons(justify='center', items=[
            ui.button(name='generate', label='Generate', primary=True),
            ui.button(name='about', label='About')
        ])
    ])

    q.page['body'] = ui.form_card(box=ui.boxes('content'), items=[
        ui.tabs(name='tasks', value='#' + q.client.tab, items=tabs, link=True),
        content_body(q)[0],
        content_body(q)[1]
    ])

    q.page['header'] = ui.header_card(
        # Place card in the header zone, regardless of viewport size.
        box='header',
        title='BLOOMing Wave',
        subtitle='Leveraging the power of LLM',
        icon='Insights'
    )

    q.page['footer'] = ui.footer_card(box='footer', caption='Made with 💛️ by Sakuna ')


def initialize(q: Q):
    q.args.model_drop = Config().bloom_versions[0]
    q.args.token = ''
    q.args.top_k = None
    q.args.top_p = None
    q.args.temperature = 0.7
    q.args.max_new_tokens = None
    q.args.return_full_text = 'False'
    q.args.do_sample = True
    q.client.tab = "email"
    q.client.error = ''
    q.client.visible = False


def content_body(q: Q):
    tab = q.client.tab
    if tab == 'email':
        return email_body(q)
    # elif tab == 'chatbot':
    #     return chat_bot_body()
    # elif tab == 'summarizer':
    #     return summarizer_body()
    # elif tab == 'sentiment':
    #     return sentiment_body()
    elif tab == 'text_gen':
        return [
            ui.textbox('prompt', value=q.args.prompt, label="Prompt",
                       placeholder="Enter the prompt here", multiline=True,
                       spellcheck=True),
            ui.textbox('generated_text', label='Generated Text', value=q.args.generated_text, multiline=True, height='500px')
        ]
    else:
        return email_body(q)


def email_body(q: Q):
    return [
        ui.textbox('email_subject', value=q.args.email_subject, label="Subject",
                   placeholder="Enter the e-mail subject here", multiline=True,
                   spellcheck=True),
        ui.textbox('email_body', label='Email', value=q.args.email_body, multiline=True, height='500px')
    ]


# def chat_bot_body():
#     return [
#         ui.textbox('chatbot_q', label="Question", placeholder="Enter a question you want to ask", multiline=True,
#                    spellcheck=True),
#         ui.textbox('chatbot_conv', label='Continued Conversation', multiline=True, height='500px')
#     ]
#
#
# def summarizer_body():
#     return [
#         ui.textbox('paragraph', label="Paragraph", placeholder="Enter a paragraph to summarize", multiline=True,
#                    spellcheck=True, height='310px'),
#         ui.textbox('summary', label='Summary', multiline=True, height='250px')
#     ]
#
#
# def sentiment_body():
#     return [
#         ui.textbox('statement', label="Statement", placeholder="Enter a statement here", multiline=True,
#                    spellcheck=True),
#         ui.textbox('sentiment', label='Sentiment', multiline=True, height='500px')
#     ]


def show_error(q: Q, error: str):
    q.client.error = error
    q.client.visible = True


@on()
async def generate(q: Q):
    q.client.visible = False
    q.client.error = ''
    error, task, model, token, params = validate_inputs(q.args)
    if error is not None:
        show_error(q, error)
    if task == 'email':
        resp, error = get_email(q.args.email_subject, model, token, params)
        if error is not None:
            show_error(q, error)
        else:
            q.args.email_body = resp
    elif task == 'text_gen':
        resp, error = get_gen(q.args.prompt, model, token, params)
        if error is not None:
            show_error(q, error)
        else:
            q.args.generated_text = resp
