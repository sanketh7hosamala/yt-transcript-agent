import asyncio
from pathlib import Path
from typing import TypedDict

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
)

# import ANTHROPIC_API_KEY from .env file
from dotenv import load_dotenv
load_dotenv()
import os
k = os.getenv("ANTHROPIC_API_KEY")
print("key loaded:", bool(k), "| length:", len(k) if k else 0)

class ChatMessage(TypedDict):
    role: str
    content: str


def load_system_prompt() -> str:
    """Load the default system prompt from the project prompt folder."""
    project_root = Path(__file__).resolve().parent
    prompt_path = project_root / "mcp-server" / "prompts" / "system_instructions.md"
    return prompt_path.read_text(encoding="utf-8")


def format_history(conversation: list[ChatMessage]) -> str:
    """Render the history into a plain-text transcript for the model."""
    if not conversation:
        return ""
    return "\n\n".join(
        f"{entry['role'].capitalize()}: {entry['content']}" for entry in conversation
    )


#def summarize_tool_result(value: object) -> str:
def summarize_tool_result(value: str | list[dict[str, object]] | dict[str, object] | None) -> str:
    """Create a compact preview for tool output so the console stays readable."""
    if isinstance(value, str):
        text = value.strip().replace("\n", " ")
        return text[:200] if text else "tool finished"
    if isinstance(value, list):
        return f"{len(value)} item(s) returned"
    if isinstance(value, dict):
        return f"result: {list(value.keys())[:5]}"
    return "tool finished"

async def handle_user_turn(
    client: ClaudeSDKClient,
    conversation: list[ChatMessage],
    user_input: str,
) -> None:
    """Send one user message with previous context, then print tool activity and response."""
    conversation.append({"role": "user", "content": user_input})
    transcript = format_history(conversation)
    prompt_text = (
        "You are continuing this conversation. "
        "Use the earlier discussion as context and answer the newest user message.\n\n"
        f"{transcript}"
    )

    await client.query(prompt_text)

    print("\nAgent: ", end="", flush=True)
    assistant_text_parts: list[str] = []

    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                    assistant_text_parts.append(block.text)
                elif isinstance(block, ToolUseBlock):
                    tool_name = block.name
                    if tool_name == "fetch_video_transcript":
                        status = "\n-- Fetching transcript..."
                    elif tool_name == "fetch_intstructions":
                        status = "\n-- Fetching instructions..."
                    else:
                        status = f"\n-- Calling {tool_name}..."
                    print(status, end="", flush=True)
                elif isinstance(block, ToolResultBlock):
                    preview = summarize_tool_result(block.content)
                    #print(f"\n-- Tool result: {preview}", end="", flush=True)
                    print(block.content, end="", flush=True)

        elif isinstance(message, ResultMessage):
            if message.result and not assistant_text_parts:
                print(message.result, end="", flush=True)
                assistant_text_parts.append(message.result)
            if message.errors:
                print(f"\n-- Result error: {message.errors}", end="", flush=True)

    if not assistant_text_parts:
        print("I could not generate a response.", end="", flush=True)

    full_reply = "".join(assistant_text_parts).strip()
    if full_reply:
        conversation.append({"role": "assistant", "content": full_reply})

    print("\n")


async def run_chat() -> None:
    project_root = Path(__file__).resolve().parent
    system_prompt = load_system_prompt()
    conversation: list[ChatMessage] = []

    options = ClaudeAgentOptions(
        cwd=str(project_root),
        system_prompt={"type": "custom", "prompt": system_prompt},
        mcp_servers={
            "youtube_mcp": {
                "type": "stdio",
                "command": "uv",
                "args": ["run", "mcp-server/yt-mcp.py"],
            }
        },
        permission_mode="acceptEdits",
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep","mcp__youtube_mcp__fetch_video_transcript", "mcp__youtube_mcp__fetch_intstructions"],
        #allowed_tools=["fetch_video_transcript", "fetch_intstructions"],   
    )

    print("=== Claude Agent SDK YouTube Agent ===")
    print("Type 'exit' to end the conversation")

    async with ClaudeSDKClient(options) as client:
        await client.connect()

        while True:
            user_input = input("\nUser: ").strip()

            if user_input.lower() in {"exit", "quit", "bye"}:
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            await handle_user_turn(client, conversation, user_input)


if __name__ == "__main__":
    asyncio.run(run_chat())
