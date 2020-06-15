import asyncio
import datetime

import aiofiles


async def handle_read_chat(host=None, port=None, log_file=None):
    reader, _ = await asyncio.open_connection(
        host='minechat.dvmn.org',
        port=5000,
    )

    async with aiofiles.open('chat-log.txt', 'a') as chat_file:
        date_now = datetime.datetime.now()
        await chat_file.write(
            f'[{date_now.strftime("%d.%m.%Y %H:%M")}] Установлено соединение\n',
        )

    while True:
        line = await reader.readline()
        if not line:
            break

        line = line.decode()
        async with aiofiles.open('chat-log.txt', 'a') as chat_file:
            current_date = datetime.datetime.now()
            await chat_file.write(f'[{current_date.strftime("%d.%m.%Y %H:%M")}] {line}')


if __name__ == '__main__':
    asyncio.run(handle_read_chat())
