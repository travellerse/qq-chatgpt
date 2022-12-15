import os
import openai
import globalvar as gl

openai.api_key = ''
gl._init()
gl.set_value('temperature', 0.5)
gl.set_value('top_p', 1.0)
gl.set_value('frequency_penalty', 0)
gl.set_value('presence_penalty', 0)

def getResponse(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=gl.get_value('temperature'),
        max_tokens=2048,
        top_p=1,
        frequency_penalty=gl.get_value('frequency_penalty'),
        presence_penalty=gl.get_value('presence_penalty')
    )
    return (response["choices"][0]["text"].strip()), evaluate(response["choices"][0]["text"])

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


if (__name__ == "__main__"):
    print(getResponse("给出爬取程序"))
