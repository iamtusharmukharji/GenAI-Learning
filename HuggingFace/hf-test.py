from transformers import pipeline

# It will going to download the model first if it already not on our system
pipe = pipeline("image-text-to-text", model="google/gemma-3n-E2B-it")

# Struct the chatML prompts
messages1 = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]


messages2 = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "what will be the RGB value of cyan"}
            # {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]


# execute through pipe object
# res = pipe(text=messages2, max_new_tokens = 64)

# print(res[0]["generated_text"][-1]["content"])

#============================================================

def get_struct_msg(prompt):
    msg = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt}
            ]
        },
    ]
    return msg


while True:
    inp = input("Ask me anything! \n")
    
    rm = get_struct_msg(inp)

    res = pipe(text=rm, max_new_token = 64 )
    print(res)


"""
Structure of res
[
    {
        "input_text": [
                        {
                            "role": "user",
                            "content": [
                                            {
                                                "type": "text",
                                                "text": "what is RGB value of sea green ?"
                                            }
                                        ]
                        }
            ],
        "generated_text": [
                                {
                                    "role": "user",
                                    "content": [
                                                    {
                                                    "type": "text",
                                                    "text": "what is RGB value of sea green ?"
                                                    }
                                                ]
                                },
                                {
                                    "role": "assistant",
                                    "content": "The RGB value for Sea Green is approximately **164, 206, 161**. However, keep in mind that color perception can vary slightly between devices and displays. This is a common approximation. You might find variations depending on the specific color palette being used. "
                                }
                            ]
    }
]

"""