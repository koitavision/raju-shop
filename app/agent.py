# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


INVENTORY = {
    "Brass Lamp": {"price": 50, "stock": 5},
    "Silk Scarf": {"price": 500, "stock": 2},
    "Taj Mahal": {"price": 2000, "stock": 0},
}


def check_inventory(item_name: str) -> str:
    """Checks the price and availability of an item in the inventory.

    Args:
        item_name: The name of the item to check.

    Returns:
        A string describing the price and stock of the item.
    """
    item = INVENTORY.get(item_name)
    if item:
        return f"The item '{item_name}' costs {item['price']} coins and there are {item['stock']} left in stock."
    return f"Sorry, I don't have an item named '{item_name}' in my bazaar."


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="Tu es Raju, un marchand polyglotte adepte du marchandage dans un bazar numérique. Tu vends : une Brass Lamp (50 pièces), une Silk Scarf (500 pièces) et même le Taj Mahal (2000 pièces) ! Ton objectif est de vendre au prix le plus fort et d'être drôle. Utilise l'outil check_inventory pour vérifier tes stocks avant de confirmer une vente. Tu es capable de parler toutes les langues pour t'adapter à tes clients, tout en gardant l'enthousiasme et l'humour typique d'un marchand de bazar indien.",
    tools=[check_inventory],
)

app = App(
    root_agent=root_agent,
    name="app",
)
