import os
import random
import re
import folder_paths


class wildcardtext:
    def __init__(self):
        self.file_cache = {}  # Cache to store file contents
        self.last_selected = {}  # Track last selected line for each keyword
        self.wildcard_directory = os.path.join(folder_paths.base_path, "wildcards")
        self.num_inputs = 3

        # Check if the directory exists
        if not os.path.exists(self.wildcard_directory):
        # Create the directory if it does not exist
            os.makedirs(self.wildcard_directory)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {f"text_input_{i}": ("STRING", {"default": "", "multiline": True}) for i in range(1, 4)}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Text",)
    FUNCTION = "combine_text"
    CATEGORY = "GORTNodes"

    def load_file_lines(self, keyword):
        # Load lines from a file and cache them
        if keyword not in self.file_cache:
            file_path =  os.path.join(self.wildcard_directory, f"{keyword}.txt")
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    self.file_cache[keyword] = [line.strip() for line in lines]
            except FileNotFoundError:
                self.file_cache[keyword] = []  # File not found, empty list


    def select_random_line(self, keyword):
        # Select a random line from the cached file contents, avoiding immediate repetition
        lines = self.file_cache.get(keyword, [])
        if not lines:
            return f"__{keyword}__"  # Return the keyword itself if file not found

        if len(lines) == 1:
            return lines[0]  # Only one line available

        last_selected = self.last_selected.get(keyword)
        available_lines = [line for line in lines if line != last_selected]
        selected_line = random.choice(available_lines)
        self.last_selected[keyword] = selected_line
        return selected_line

    def combine_text(self, **kwargs):
        combined_text = ""

        for i in range(1,self.num_inputs + 1):
            text_input_key = f"text_input_{i}"
            if text_input_key in kwargs:
                text = kwargs[text_input_key]
                processed_text = self.process_text(text)
                combined_text += processed_text + " "
        
        return (combined_text.strip(),)

    def process_text(self, text):
        pattern = re.compile(r'__(\w+)__')
        matches = pattern.findall(text)
        for match in matches:
            keyword = match
            self.load_file_lines(keyword)
            replacement = self.select_random_line(keyword)
            text = text.replace(f"__{keyword}__", replacement, 1)
        return text