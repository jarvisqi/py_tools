from openai import OpenAI

api_key = "sk-cccccccccccc"
base_url = "https://api.deepseek.com"


def app():
    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    app()
