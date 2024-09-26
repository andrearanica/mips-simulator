import os, json
from enum import Enum

from libs import constants

class MessageManager:
    def __init__(self, language: str) -> None:
        self.__language = language
        self.__json_path = os.path.join(constants.CONFIG_PATH, f'messages_{language}.json')
        
    @property
    def language(self) -> constants.Languages:
        return self.__language

    @language.setter
    def language(self, language: str) -> None:
        if not language in [language.value for language in constants.Languages]:
            raise RuntimeError(f'Language \'{language}\' is not compatible with message manager')
        if not os.path.exists(self.__json_path):
            raise RuntimeError(f'Language \'{language}\' file not found (messages_{self.language.value}.json)')
        self.__json_path = os.path.join(constants.CONFIG_PATH, f'messages_{language}.json')
        self.__language = language

    def get_message(self, message: str):
        """ Returns the passed message in the setted language
        """
        with open(self.__json_path, 'r+') as file_reader:
            messages = json.loads(file_reader.read())

        if not message in messages.keys():
            raise RuntimeError(f'Message \'{message}\' is not defined for the language \'{self.language}\'')
    
        return messages.get(message)