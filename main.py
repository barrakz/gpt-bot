import openai
import config
import time

openai.api_key = config.openai_api_key


# Funkcja pomocnicza do zadawania pytań GPT-3
def ask_gpt3(prompt, model_engine="text-davinci-002", max_tokens=2048, n=1):
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0].text.strip()
    except openai.error.RateLimitError as e:
        # Jeśli wystąpi błąd `RateLimitError`, poczekaj 5 sekund i spróbuj ponownie
        print("Osiągnięto limit zapytań. Czekam 5 sekund przed ponowną próbą...")
        time.sleep(5)
        return ask_gpt3(prompt, model_engine, max_tokens, n)
    except Exception as e:
        print("Wystąpił błąd podczas zadawania pytania GPT-3:", e)
        message = ""

    return message


# Sprawdzenie połączenia z OpenAI API
try:
    models = openai.Model.list()
    print("Połączenie z OpenAI jest poprawne.")
except Exception as e:
    print("Wystąpił błąd podczas łączenia z OpenAI:", e)

while True:
    # Zadawanie pytań GPT-3
    prompt = input("Podaj pytanie, na które chcesz uzyskać odpowiedź (lub wpisz 'exit' aby zakończyć): ")
    if prompt == 'exit':
        break
    response = ask_gpt3(prompt)

    print("Odpowiedź od GPT-3:")
    print(response)
