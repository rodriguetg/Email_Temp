import re
from datetime import datetime
import schedule
import time
import threading

class Rule:
    def __init__(self, conditions, actions):
        self.conditions = conditions
        self.actions = actions

    def check_conditions(self, message):
        for condition, value in self.conditions.items():
            if condition == 'contains':
                if not any(keyword.lower() in message['content'].lower() for keyword in value):
                    return False
            elif condition == 'from':
                if message['sender'] != value:
                    return False
            elif condition == 'platform':
                if message['platform'] != value:
                    return False
            elif condition == 'time_range':
                current_time = datetime.now().time()
                if not (value['start'] <= current_time <= value['end']):
                    return False
        return True

    def execute_actions(self, message, platform_manager):
        for action, value in self.actions.items():
            if action == 'forward_to':
                platform = platform_manager.platforms.get(value['platform'])
                if platform:
                    platform.send_message(value['destination'], message['content'])
            elif action == 'auto_reply':
                source_platform = platform_manager.platforms.get(message['platform'])
                if source_platform:
                    source_platform.send_message(message['sender'], value)
            elif action == 'tag':
                message['tags'] = message.get('tags', []) + [value]
            elif action == 'archive':
                message['archived'] = True

class AutoResponse:
    def __init__(self, template, schedule=None, conditions=None):
        self.template = template
        self.schedule = schedule
        self.conditions = conditions or {}

    def format_response(self, context):
        return self.template.format(**context)

    def should_respond(self, message):
        if not self.conditions:
            return True
        return all(
            message.get(key) == value
            for key, value in self.conditions.items()
        )

class AutomationManager:
    def __init__(self, platform_manager):
        self.platform_manager = platform_manager
        self.rules = []
        self.auto_responses = []
        self.scheduled_tasks = {}

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_auto_response(self, auto_response):
        self.auto_responses.append(auto_response)
        if auto_response.schedule:
            self.setup_scheduled_response(auto_response)

    def setup_scheduled_response(self, auto_response):
        def send_scheduled_response():
            for platform in self.platform_manager.platforms.values():
                if hasattr(platform, 'default_destination'):
                    platform.send_message(
                        platform.default_destination,
                        auto_response.format_response({})
                    )

        if 'daily' in auto_response.schedule:
            schedule.every().day.at(auto_response.schedule['daily']).do(send_scheduled_response)
        elif 'weekly' in auto_response.schedule:
            getattr(schedule.every(), auto_response.schedule['weekly']['day'])\
                .at(auto_response.schedule['weekly']['time']).do(send_scheduled_response)

    def process_message(self, message):
        # Appliquer les règles
        for rule in self.rules:
            if rule.check_conditions(message):
                rule.execute_actions(message, self.platform_manager)

        # Vérifier les réponses automatiques
        for auto_response in self.auto_responses:
            if auto_response.should_respond(message):
                response = auto_response.format_response({
                    'sender': message['sender'],
                    'platform': message['platform'],
                    'time': datetime.now().strftime('%H:%M')
                })
                source_platform = self.platform_manager.platforms.get(message['platform'])
                if source_platform:
                    source_platform.send_message(message['sender'], response)

    def start_scheduler(self):
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
