import asyncio
from turtle import update

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

agent = Agent(
    client= FoundryChatClient(
      project_endpoint="https://aifhowtolghosarx.services.ai.azure.com/api/projects/fphowtolghosarx",
      model="gpt-5.4-mini",
      credential=AzureCliCredential(),
    ),
    name="HelloAgent",
    instructions="You are a friendly assistant."
)

async def do_the_thing():
    
    async for update in agent.run("Write a haiku about shipping 1.0.", stream=True):
        print(update)

asyncio.run(do_the_thing())