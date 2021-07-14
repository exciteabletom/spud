import string


class Utils:
    @staticmethod
    def create_jar_name(text: str) -> str:
        text = text.title()
        return text.translate(str.maketrans("", "", string.whitespace))

    @staticmethod
    def sanitise_input(text: str) -> str:
        return ""
