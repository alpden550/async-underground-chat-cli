import asyncio
import json

from loguru import logger


async def handle_write_chat(message, host='minechat.dvmn.org', port=5050):
    reader, writer = await asyncio.open_connection(
        host=host,
        port=port,
    )

    data = await reader.readline()
    print(data.decode())
    await authorize_chat_user(writer=writer)
    data = await reader.readline()
    print(json.loads(data))
    await write_to_chat('Hello! again:)', writer)


async def authorize_chat_user(token='194849d4-aef9-11ea-b989-0242ac110002', writer=None):
    writer.write(f'{token}\n'.encode())
    await writer.drain()


async def write_to_chat(message, writer):
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


def main():
    asyncio.run(handle_write_chat('Hello!'))


if __name__ == '__main__':
    main()
