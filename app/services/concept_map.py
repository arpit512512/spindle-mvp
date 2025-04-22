from openai import OpenAI
import json
from app.core.config import Settings
from app.core.logger import logger

client = OpenAI(api_key=Settings().OPENAI_API_KEY)

PROMPT_TEMPLATE = """
You are an AI assistant that transforms educational content into structured concept maps.

Given the following text, extract key concepts and their relationships, and represent them in a JSON format.

Each node should include:
- id
- label
- description

Each edge should include:
- source
- target
- relation

ONLY return valid JSON. Do not wrap the output in markdown. Do not add any explanation.

Text:
{text}
"""

def to_mermaid(data):
    lines = ["graph TD"]
    for node in data.get("nodes", []):
        lines.append(f'{node["id"]}[{node["label"]}]')
    for edge in data.get("edges", []):
        lines.append(f'{edge["source"]} -->|{edge["relation"]}| {edge["target"]}')
    return "\n".join(lines)

async def generate_concept_map(text: str):
    prompt = PROMPT_TEMPLATE.format(text=text)

    logger.debug("Concept Extractor AI Input:\n{}", prompt)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content

    logger.debug("Concept Extractor AI Output:\n{}", content)

    try:
        parsed = json.loads(content[content.find('{'):])
        logger.info("Parsed concept map with %d nodes", len(parsed.get("nodes", [])))
        return parsed
    except Exception as e:
        logger.error("JSON parsing failed: {}", str(e))
        return {"error": str(e), "raw": content}
