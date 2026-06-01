import asyncio
import json

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)

MODEL_NAME = "Qwen/Qwen3-4B-Instruct"


class MCPAgent:

    def __init__(self):
        self.tokenizer = None
        self.model = None

    def load_model(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto"
        )

    def ask_llm(self, prompt: str) -> str:

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

    async def run(self):

        self.load_model()

        server_params = StdioServerParameters(
            command="python",
            args=["weather_server.py"]
        )

        async with stdio_client(server_params) as (
            read,
            write
        ):

            async with ClientSession(
                read,
                write
            ) as session:

                await session.initialize()

                tools = await session.list_tools()

                tool_text = ""

                for tool in tools:
                    tool_text += f"""
                Tool:
                Name: {tool.name}
                Description: {tool.description}
                """

                while True:

                    user_input = input(
                        "\nUser > "
                    )

                    prompt = f"""
                    You are an AI assistant.

                    Available tools:

                    {tool_text}

                    If a tool is needed,
                    return ONLY JSON.

                    Example:

                    {{
                    "tool": "search_location",
                    "arguments": {{
                        "query": "Surabaya"
                    }}
                    }}

                    User:
                    {user_input}
                    """

                    llm_response = self.ask_llm(
                        prompt
                    )

                    print(
                        "\nLLM RAW:\n",
                        llm_response
                    )

                    try:

                        start = llm_response.find("{")
                        end = llm_response.rfind("}")

                        json_text = (
                            llm_response[
                                start:end+1
                            ]
                        )

                        tool_call = json.loads(
                            json_text
                        )

                        tool_name = (
                            tool_call["tool"]
                        )

                        arguments = (
                            tool_call["arguments"]
                        )

                        print(
                            "\nCalling MCP Tool:",
                            tool_name
                        )

                        tool_result = (
                            await session.call_tool(
                                tool_name,
                                arguments
                            )
                        )

                        print(
                            "\nTool Result:\n",
                            tool_result
                        )

                        final_prompt = f"""
                        User:
                        {user_input}

                        Tool Result:
                        {tool_result}

                        Answer naturally.
                        """

                        final_answer = (
                            self.ask_llm(
                                final_prompt
                            )
                        )

                        print(
                            "\nAssistant:\n",
                            final_answer
                        )

                    except Exception:

                        print(
                            "\nAssistant:\n",
                            llm_response
                        )


async def main():

    agent = MCPAgent()

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())