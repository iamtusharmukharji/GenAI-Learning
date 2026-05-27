import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you doing today? I hope you're having a great day!"
tokens = enc.encode(text)
print(f"Text: {text}")
print(f"Tokens: {tokens}")
print(f"Decoded Text: {enc.decode(tokens)}")