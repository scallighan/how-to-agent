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
    stream = agent.run("Write a haiku about shipping 1.0.", stream=True)
    async for update in stream:
        output_text = update.text
        if len(output_text) > 0:
            print(f"Agent response: {output_text}")
            

    final = await stream.get_final_response()
    print(f"Streaming complete! Full text: {final.text}")
    print(f"Token usage: {final.usage_details}")

asyncio.run(do_the_thing())