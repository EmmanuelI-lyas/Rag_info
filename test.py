import asyncio

from src.graph.workflow import build_graph

graph = build_graph()


async def main():

    async for event in graph.astream_events(
        {
            "question": "What is BIS report?"
        },
        version="v2",
    ):
        print(event["event"])


asyncio.run(main())