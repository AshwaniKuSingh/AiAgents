from transformers import pipeline
from langchain.llms.base import LLM
from typing import Optional, List, Any
import requests

# Custom HuggingFacePipeline class with proper field definition
class HuggingFacePipeline(LLM):
    pipeline: Any  # Define pipeline as a Pydantic field

    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        result = self.pipeline(prompt, max_length=100, num_return_sequences=1)
        return result[0]["generated_text"]

    @property
    def _llm_type(self) -> str:
        return "custom_huggingfac

# Load Hugging Face model
hf_pipeline = pipeline("text-generation", model="distilgpt2", device=0)  # Use GPU if available
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Agents
class CalculationAgent:
    def execute(self, query: str) -> str:
        try:
            result = eval(query)
            return f"Calculation result: {result}"
        except Exception as e:
            return f"Error in calculation: {e}"

class WikipediaAgent:
    def execute(self, query: str) -> str:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
            },
        )
        try:
            snippet = response.json()["query"]["search"][0]["snippet"]
            return f"Wikipedia result: {snippet}"
        except (KeyError, IndexError):
            return "No Wikipedia results found."

class WeatherAgent:
    def execute(self, location: str) -> str:
        return f"Weather at {location}: 25°C, Sunny (Mock Data)"

# Orchestrator
class Orchestrator:
    def __init__(self):
        self.agents = {
            "calculation": CalculationAgent(),
            "wikipedia": WikipediaAgent(),
            "weather": WeatherAgent(),
        }

    def process_tasks(self, tasks):
        results = {}
        for task_type, task_data in tasks.items():
            agent = self.agents.get(task_type)
            if agent:
                results[task_type] = agent.execute(task_data)
            else:
                results[task_type] = f"No agent found for task: {task_type}"
        return results

# Tasks
tasks = {
    "calculation": "15 * 7 + 12",
    "wikipedia": "Python programming language",
    "weather": "New York",
}

# Run Orchestrator
orchestrator = Orchestrator()
results = orchestrator.process_tasks(tasks)

# Print Results
for task, result in results.items():
    print(f"{task.capitalize()} Agent Result: {result}")

# Combine and Summarize Results
combined_results = "\n".join([f"{task}: {result}" for task, result in results.items()])
summary_prompt = f"Here are the results of the tasks:\n{combined_results}\nCan you summarize this for me?"
summary = llm(summary_prompt)

# Print Summary
print("\nSummary of All Results:")
print(summary)