import argparse
import asyncio
from datetime import datetime

import aiofiles


async def handle_read_chat(host=None, port=None, log_file='chat-log.txt'):
    reader, _ = await asyncio.open_connection(
        host='minechat.dvmn.org',
        port=5000,
    )

    await write_log_message('Установлено соединение\n', log_file)

    while True:
        line = await reader.readline()
        if not line:
            break
        line = line.decode()
        await write_log_message(line, log_file)


async def write_log_message(message, logfile):
    formatted_timenow = datetime.now().strftime("%d.%m.%Y %H:%M")
    async with aiofiles.open(logfile, 'a') as chatfile:
        await chatfile.write(f'[{formatted_timenow}] {message}')


def main():
    asyncio.run(handle_read_chat())


if __name__ == '__main__':
    main()
