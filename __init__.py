from .wildcardtext import wildcardtext
WEB_DIRECTORY = "./"
NODE_CLASS_MAPPINGS = {
    "GORTNodes": wildcardtext
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GORTNodes": "Wild Card Text"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']