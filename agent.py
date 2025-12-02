import os
from openai import OpenAI
import datetime
import time

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY manquant dans GitHub Secrets")

client = OpenAI(api_key=API_KEY)

ASSISTANT_ID = "asst_9s7tribjjPzp2DbOF4nNxa8j"
OUTPUT_FILE = "journal_reponses.csv"

def run_agent():
    print("Lancement de l'agent...")
    thread = client.beta.threads.create()
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread.id)
    answer = messages.data[0].content[0].text.value

    today = datetime.date.today()
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{today};{answer}\n")

    print("Réponse enregistrée :", answer)

if __name__ == "__main__":
    run_agent()
