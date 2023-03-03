import os
import traceback

import openai
from revChatGPT.V1 import Chatbot

import chatgpt
import config as cf
from api import error_print
from chatbot import chatbot
from chatbot import chatbot_dict as bot
from conversation import conversation_dict as con

cf._init()
openai.api_key = cf.get_value('Openai', "APIkey")
openai.proxy = cf.get_value("Chatgpt", "proxy")


def getResponse(prompt, uid_or_gid, chatgpt=False):
    if (chatgpt == False):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=con.get_value(uid_or_gid).getParam('temperature'),
            top_p=con.get_value(uid_or_gid).getParam('top_p'),
            frequency_penalty=con.get_value(
                uid_or_gid).getParam('frequency_penalty'),
            presence_penalty=con.get_value(
                uid_or_gid).getParam('presence_penalty')
        )
        return response["choices"][0]["message"]["content"].strip(), response["choices"][0]["message"]["role"].strip()
    else:
        if bot.get_value(uid_or_gid) == None:
            bot.set_value(uid_or_gid, chatbot(uid_or_gid))
        b = bot.get_value(uid_or_gid)
        try:
            for data in b.core.ask(prompt):
                response = data["message"]
            bot.set_value(uid_or_gid, b)
            return response
        except Exception as e:
            return error_print(e)


def evaluate(output_label):
    # This is the probability at which we evaluate that a "2" is likely real
    # vs. should be discarded as a false positive
    toxic_threshold = -0.355

    if output_label == "2":
        # If the model returns "2", return its confidence in 2 or other output-labels
        logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # If the model is not sufficiently confident in "2",
        # choose the most probable of "0" or "1"
        # Guaranteed to have a confidence for 2 since this was the selected token.
        if logprobs["2"] < toxic_threshold:
            logprob_0 = logprobs.get("0", None)
            logprob_1 = logprobs.get("1", None)

            # If both "0" and "1" have probabilities, set the output label
            # to whichever is most probable
            if logprob_0 is not None and logprob_1 is not None:
                if logprob_0 >= logprob_1:
                    output_label = "0"
                else:
                    output_label = "1"
            # If only one of them is found, set output label to that one
            elif logprob_0 is not None:
                output_label = "0"
            elif logprob_1 is not None:
                output_label = "1"

            # If neither "0" or "1" are available, stick with "2"
            # by leaving output_label unchanged.

    # if the most probable token is none of "0", "1", or "2"
    # this should be set as unsafe
    if output_label not in ["0", "1", "2"]:
        output_label = "2"

    return output_label


if __name__ == "__main__":
    from conversation import Conversation
    while 1:
        msg = input()
        con.set_value(1, Conversation(1, True))
        print(getResponse(msg, 1))
