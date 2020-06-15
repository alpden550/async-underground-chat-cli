import asyncio
import json

import click
from loguru import logger


def sanitize_text(text):
    return text.replace('\n', '')


async def handle_write_chat(message=None, host=None, port=None, token=None, username=None):
    try:
        reader, writer = await asyncio.open_connection(
            host=host,
            port=port,
        )
        data = await reader.readline()
        logger.debug('sender: {}'.format(data.decode()))

        if username:
            token = await register_chat_user(reader, writer, username)
            await submit_message(message, writer)
        elif token:
            await authorize_chat_user(token=token, writer=writer)

            logger.debug(f'Tried to authorize with token {token}')
            authorize_data = await reader.readline()

            if not json.loads(authorize_data):
                logger.error('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
                return

            await submit_message(message, writer)

    finally:
        writer.close()


async def register_chat_user(reader, writer, username):
    writer.write('\n'.encode())
    await reader.readline()

    sanitazed_username = sanitize_text(username)
    writer.write(f'{sanitazed_username}\n'.encode())
    user_data = await reader.readline()
    await writer.drain()
    nickname = json.loads(user_data.decode()).get('nickname')
    token = json.loads(user_data.decode()).get('account_hash')
    logger.info(f'\nUser {nickname} successfull created.\nToken: {token}')

    return token


async def authorize_chat_user(token, writer):
    writer.write(f'{token}\n'.encode())
    await writer.drain()


async def submit_message(message, writer):
    sanitazed_message = sanitize_text(message)
    writer.write(f'{sanitazed_message}\n\n'.encode())
    logger.debug('Message sended.')
    await writer.drain()


@click.command()
@click.option('-t', '--token', required=False, help='Token to authenticate')
@click.option('-u', '--username', required=False, help='Username for creating a new user.')
@click.option('-h', '--host', default='minechat.dvmn.org', help='Chat host.')
@click.option('-p', '--port', type=int, default=5050, help='Chat port.')
@click.option('-m', '--message', default='Hello, everybody.', help='Message for sending.')
def main(message, host, port, token, username):
    asyncio.run(
        handle_write_chat(message=message, token=token, username=username, host=host, port=port),
    )


if __name__ == '__main__':
    main()
