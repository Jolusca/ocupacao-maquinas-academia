from datetime import datetime, timezone
import os
from pathlib import Path
import random
import time
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
  env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
uri = os.getenv("MONGODB_URI")

if not uri:
  raise ValueError("Defina MONGODB_URI no arquivo .env")

# Se a URI tiver placeholders <username> / <password>, preenche com quote_plus
if username and "<username>" in uri:
  uri = uri.replace("<username>", quote_plus(username))
if password and "<password>" in uri:
  uri = uri.replace("<password>", quote_plus(password))

DB_NAME = os.getenv("MONGODB_DB", "gym_occupancy")

client = MongoClient(uri)
db = client[DB_NAME]
telemetry_col = db["telemetry"]
nodes_col = db["nodes"]


def generate_gym_doc(machine_name: str, ocupacao: bool) -> dict:
  return {
      "name": machine_name,
      "ocupacao": ocupacao,
      "timestamp": datetime.now(timezone.utc),
  }


def run_simulation(
    machines: list[str],
    duration_seconds: int = 20,
    interval_seconds: float = 2.0,
    change_prob: float = 0.35,
):
  estados = {name: False for name in machines}
  start_time = time.monotonic()

  print(
      f"Enviando dados por {duration_seconds}s a cada {interval_seconds}s..."
  )

  while (time.monotonic() - start_time) < duration_seconds:
    for name in machines:
      if random.random() < change_prob:
        estados[name] = not estados[name]

      doc = generate_gym_doc(name, estados[name])

      telemetry_col.insert_one(doc.copy())
      nodes_col.update_one(
          {"name": name},
          {
              "$set": {
                  "name": name,
                  "ocupacao": doc["ocupacao"],
                  "timestamp": doc["timestamp"],
              }
          },
          upsert=True,
      )
      print("Enviado:", doc)

    remaining = duration_seconds - (time.monotonic() - start_time)
    if remaining <= 0:
      break
    time.sleep(min(interval_seconds, remaining))

  print("Envio finalizado apos 20 segundos.")


if __name__ == "__main__":
  run_simulation(
      machines=["maquina_1", "maquina_2", "maquina_3"],
      duration_seconds=20,
      interval_seconds=2.0,
      change_prob=0.35,
  )