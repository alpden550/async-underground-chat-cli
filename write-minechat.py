import asyncio
import json

from loguru import logger


def sanitize_text(text):
    return text.replace('\n', '')


async def handle_write_chat(message, host='minechat.dvmn.org', port=5050, token=None, username=None):
    try:
        reader, writer = await asyncio.open_connection(
            host=host,
            port=port,
        )
        data = await reader.readline()
        logger.debug('sender: {}'.format(data.decode()))

        if username and not token:
            token = await register_chat_user(reader, writer, username)
        elif token:
            await authorize_chat_user(token=token, writer=writer)

            logger.debug(f'Tried to authorize with token {token}')
            authorize_data = await reader.readline()

            if not json.loads(authorize_data):
                logger.error('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
                return

        await submit_message(message, writer)
        logger.debug('Message sended.')

    finally:
        writer.close()


async def register_chat_user(reader, writer, username):
    writer.write('\n'.encode())
    await reader.readline()

    sanitazed_username = sanitize_text(username)
    writer.write(f'{sanitazed_username}\n'.encode())
    user_data = await reader.readline()
    nickname = json.loads(user_data.decode()).get('nickname')
    token = json.loads(user_data.decode()).get('account_hash')
    logger.info(f'\nUser {nickname} successfull created.\nToken: {token}')

    return token


async def authorize_chat_user(token=None, writer=None):
    writer.write(f'{token}\n'.encode())
    await writer.drain()


async def submit_message(message, writer):
    sanitazed_message = sanitize_text(message)
    writer.write(f'{sanitazed_message}\n\n'.encode())
    await writer.drain()


def main():
    asyncio.run(handle_write_chat('Hello!\n', username='2\n'))


if __name__ == '__main__':
    main()
