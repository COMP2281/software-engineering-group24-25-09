import ollama

model_name = "llama3.2:1b"

test_prompt = "hello"

response = ollama.chat(model_name, [{"role": "user", "content": test_prompt}])
response_text = response["message"]["content"]

print(response_text)
