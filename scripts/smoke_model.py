from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agents.model_adapter import ask_model

response = ask_model("Say hello in one short sentence.")
print(response)