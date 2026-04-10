from microsoft_agents.activity import load_configuration_from_env
from microsoft_agents.authentication.msal import MsalConnectionManager
from microsoft_agents.hosting.core import (
   AgentApplication,
   Authorization,
   TurnState,
   TurnContext,
   MemoryStorage,
)
from microsoft_agents.hosting.aiohttp import CloudAdapter
from os import environ
from .server import start_server
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient


agents_sdk_config = load_configuration_from_env(environ)
print(f"Loaded configuration: {agents_sdk_config}")
# Create storage and connection manager
STORAGE = MemoryStorage()
CONNECTION_MANAGER = MsalConnectionManager(**agents_sdk_config)
ADAPTER = CloudAdapter(connection_manager=CONNECTION_MANAGER)
AUTHORIZATION = Authorization(STORAGE, CONNECTION_MANAGER, **agents_sdk_config)

AGENT_APP = AgentApplication[TurnState](
    storage=STORAGE,
    adapter=ADAPTER,
    authorization=AUTHORIZATION
)

CONVERSATION_ID=None

async def _help(context: TurnContext, _: TurnState):
    await context.send_activity(
        "Welcome to the Level Up Agent sample 🚀. "
        "Type 'help' for help or send a message to see the echo feature in action."
    )

async def _reset(context: TurnContext, _: TurnState):
    global CONVERSATION_ID
    CONVERSATION_ID = None
    await context.send_activity("Conversation reset. Start a new conversation to see the effect.")

#AGENT_APP.conversation_update("membersAdded")(_help)

AGENT_APP.message("help")(_help)
AGENT_APP.message("reset")(_reset)

AGENT = Agent(
            client= FoundryChatClient(
            project_endpoint=os.environ.get("AZURE_AI_PROJECT_ENDPOINT"),
            model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
            credential=DefaultAzureCredential(),
            ),
            name="HelloAgent",
            instructions="You are a friendly assistant."
        )
    
@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _):
    global CONVERSATION_ID

    text = context.activity.text
    print(f"Received message: {text}")
    try:
        context.streaming_response.queue_informative_update("Getting ready...\n")
        
        async for update in AGENT.run(text, stream=True):
            #await context.send_activity(f"{text} (echo from agent)")
            context.streaming_response.queue_text_chunk(update)
        
    except Exception as e:
        print(f"Error processing message: {e}")
        await context.send_activity(f"Sorry, something went wrong while processing your message. {e}")


    
    

if __name__ == "__main__":
    try:
        start_server(AGENT_APP, CONNECTION_MANAGER.get_default_connection_configuration())
    except Exception as error:
        raise error