import asyncio
from abc import ABC, abstractmethod
import telegram
from discord.ext import commands
from slack_sdk import WebClient
import tweepy
from email.mime.text import MIMEText
import smtplib
import imaplib

class MessagePlatform(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def send_message(self, destination, content):
        pass

    @abstractmethod
    async def receive_messages(self):
        pass

class TelegramPlatform(MessagePlatform):
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)

    async def connect(self):
        try:
            await self.bot.get_me()
            return True
        except Exception as e:
            print(f"Erreur de connexion Telegram: {e}")
            return False

    async def send_message(self, chat_id, content):
        try:
            await self.bot.send_message(chat_id=chat_id, text=content)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Telegram: {e}")
            return False

    async def receive_messages(self):
        try:
            async with self.bot:
                await self.bot.get_updates()
        except Exception as e:
            print(f"Erreur de réception Telegram: {e}")

class DiscordPlatform(MessagePlatform):
    def __init__(self, token):
        self.bot = commands.Bot(command_prefix='!')
        self.token = token

    async def connect(self):
        try:
            await self.bot.start(self.token)
            return True
        except Exception as e:
            print(f"Erreur de connexion Discord: {e}")
            return False

    async def send_message(self, channel_id, content):
        try:
            channel = self.bot.get_channel(int(channel_id))
            await channel.send(content)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Discord: {e}")
            return False

    async def receive_messages(self):
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            # Traitement du message reçu
            print(f"Message Discord reçu: {message.content}")

class SlackPlatform(MessagePlatform):
    def __init__(self, token):
        self.client = WebClient(token=token)

    async def connect(self):
        try:
            self.client.auth_test()
            return True
        except Exception as e:
            print(f"Erreur de connexion Slack: {e}")
            return False

    async def send_message(self, channel, content):
        try:
            self.client.chat_postMessage(channel=channel, text=content)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Slack: {e}")
            return False

    async def receive_messages(self):
        # Utilisation de l'API Events de Slack pour recevoir les messages
        pass

class EmailPlatform(MessagePlatform):
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    async def connect(self):
        try:
            self.smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.smtp.starttls()
            self.smtp.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"Erreur de connexion Email: {e}")
            return False

    async def send_message(self, to_email, content):
        try:
            msg = MIMEText(content)
            msg['Subject'] = 'Message from Hub'
            msg['From'] = self.email
            msg['To'] = to_email
            self.smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Email: {e}")
            return False

    async def receive_messages(self):
        try:
            mail = imaplib.IMAP4_SSL(self.smtp_server)
            mail.login(self.email, self.password)
            mail.select('inbox')
            return True
        except Exception as e:
            print(f"Erreur de réception Email: {e}")
            return False

class PlatformManager:
    def __init__(self):
        self.platforms = {}

    def add_platform(self, name, platform):
        self.platforms[name] = platform

    async def send_to_all(self, content):
        tasks = []
        for platform in self.platforms.values():
            if hasattr(platform, 'default_destination'):
                tasks.append(platform.send_message(platform.default_destination, content))
        await asyncio.gather(*tasks)

    async def initialize_all(self):
        tasks = []
        for platform in self.platforms.values():
            tasks.append(platform.connect())
        await asyncio.gather(*tasks)
