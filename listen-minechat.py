import asyncio
from datetime import datetime

import aiofiles
import click


async def handle_read_chat(host=None, port=None, log_file='chat-log.txt'):
    try:
        reader, writer = await asyncio.open_connection(
            host=host,
            port=port,
        )

        await write_log_message('Установлено соединение\n', log_file)

        while True:
            line = await reader.readline()
            if not line:
                break

            line = line.decode()
            await write_log_message(line, log_file)

    finally:
        writer.close()


async def write_log_message(message, logfile):
    formatted_timenow = datetime.now().strftime("%d.%m.%Y %H:%M")
    async with aiofiles.open(logfile, 'a') as chatfile:
        await chatfile.write(f'[{formatted_timenow}] {message}')


@click.command()
@click.option(
    '-h',
    '--host',
    default='minechat.dvmn.org',
    help='Host to connect',
    show_default=True,
)
@click.option(
    '-p',
    '--port',
    default=5000,
    type=int,
    help='Port for connected host',
    show_default=True,
)
@click.option(
    '-o',
    '--output',
    default='chat-log.txt',
    type=str,
    help='Path to file to write chat history',
    show_default=True,
)
def main(host, port, output):
    asyncio.run(handle_read_chat(host=host, port=port, log_file=output))


if __name__ == '__main__':
    main()
