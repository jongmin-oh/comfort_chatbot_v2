import openai

from app.config import openai_settings, paths

openai.api_key = openai_settings.OPENAI_API_KEY
prompt = open(paths.PROMPT_DIR.joinpath("chatgpt.txt")).read()


def chatgpt_reply(user_message: str) -> str:
    messages = [{"role": "system", "content": (prompt)}]

    messages.append({"role": "user", "content": f"{user_message}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    answer = completion.choices[0].message["content"].strip()
    answer = answer.replace("\n", " ")
    answer = answer.replace("당신", "선생님")
    answer = answer.replace("너", "선생님")
    answer = answer.replace("내가", "제가")
    answer = answer.replace("내담자님", "선생님")
    return answer


if __name__ == "__main__":
    print(chatgpt_reply("공무원시험 준비를 계속해야할까? 이번에 또 떨어지면 부모님 볼 자신이 없어.."))
