from model.inference import infer

defaultPrompt = """*Intelligent email assistant that can generate the following emails from the descriptive input*
    Subject: Thank John for the book, John is a childhood friend who gifted me a book last week on my birthday.
    
    Output:
    Dear John,
    Hope you are doing well. 
    Thank you so much for giving such a precious gift.
    I really appreciate this gesture amd hope to hang out soon. 
    Your friend
    -
    Subject: Tell TechCorp I appreciate the great service, I visited the TechCorp showroom last weekend where I was very impressed by the warmth and great service of their staff
    
    Output:
    To Whom it May Concern,
    I want you to know that I appreciate the great service at TechCorp.
    The staff is outstanding and I enjoy every visit.
    Sincerely
    -
    Subject: Invite Amanda and Paul to the company event Friday night. Amanda and Paul are close friends. This friday we are celebrating the five year anniversary for zolotech
    
    Output:
    Hey Guys,
    I hope this finds you doing well.
    With great joy and immense pleasure I would like to invite you to the fifth anniversary celebration for zolotech.
    Looking forward to seeing you there.
    Your friend
    -
    Subject: Resigning from the company
    
    Output:
    Hi All,
    I write to inform you that I am resigning from my position.
    Thank you so much for all of the opportunities this company has provided me. I have learned so much these past years, and will never forget the kindness of all of my colleagues.
    Let me know if there is anything I can do to make this transition easier.
    Thank You
    -
    Subject: {}
    Output: 
    """


def postprocess_email(output: str, title: str):
    l = output.split("*")[-1].split("-")
    for email in l:
        if title in email:
            return email


def get_email(title: str, model: str, token: str, params: dict):
    prompt = defaultPrompt.format(title)
    resp, error = infer(prompt, model, token, params)
    if error is None:
        return postprocess_email(resp, title), None
    else:
        return None, error
