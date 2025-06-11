from openai import OpenAI
from toolregistry import ToolRegistry


import json
import os
import shutil
from typing import Dict, List


class Sortly:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/",
    ):
        self.api_key = api_key
        self.model = model
        self.agent = OpenAI(api_key=self.api_key, base_url=base_url)

    registry = ToolRegistry()
    system_instruction = """
    You are an intelligent folder organizer AI agent working with local files. The user will provide:
    A path to a root folder (root_folder_path). 
    A flat list of file names (not paths, and no metadata)
    Your task is to analyze the list of file names and create an optimal folder_structure, which is a dictionary mapping folder names to lists of files that belong in them.
    Use your best judgment to group files logically. Consider factors such as:
      - File type (e.g., PDFs, images, code, audio)
      - Common prefixes or keywords in file names (e.g., invoice_, projectX_, photo_)
      -Natural groupings (e.g., documents vs. media vs. backups).
    You will then call the tool to physically reorganize the files on the local system.
    Important Notes:
      - Folder names should be descriptive (Maximum 3 words) and meaningful, not just file extensions.
      - Keep original file names intact; do not rename files.
      - If there are existing folders do not rename or move them. try to put the files in the existing folders if it matches the context.
      - If there are files that don’t clearly belong in a category, place them into an "Misc" folder. But before putting any file in that check if it can be put in any existing files.
      - You do not have to arrange the existing folders. Do not include them unless they can be combined in a meaningful way. 
    """

    def sort_folder(self, user_prompt: str):
        tools = self.registry.to_openai_tools()
        result = self.agent.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": user_prompt},
            ],
            tools=tools,
            temperature=0.7,
        )
        message = result.choices[0].message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                self.call_tool(tool_call)
                return f"{message.content}, \n I have sorted the files based on the provided folder structure."
            print("No tools called")
            return message

    def call_tool(self, tool_call):
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool_func = self.registry.tools[tool_name]["function"]
        tool_func = tool_func.__get__(self, self.__class__)
        return tool_func(**arguments)

    @registry.register(
        description="Sorts the files given the root_folder_path based on the folder_strcuture",
        tags=["sort"],
    )
    def sort(
        self, root_folder_path: str, folder_structure: Dict[str, List[str]]
    ) -> str:
        """
        Sorts the files in the root_folder_path based on the suggested folder_strcuture
        Args:
            root_folder_path (str): Path to the root folder
            folder_strcuture (dict[str, List[str]]): Dictionary containing the foldername as keys and full filenames as values
        Returns:
            Done: Message
        """
        for folder_name, file_list in folder_structure.items():
            target_folder_path = os.path.join(root_folder_path, folder_name)
            os.makedirs(target_folder_path, exist_ok=True)

            for file_name in file_list:
                source_path = os.path.join(root_folder_path, file_name)
                destination_path = os.path.join(target_folder_path, file_name)
                if os.path.exists(source_path):
                    try:
                        shutil.move(source_path, destination_path)
                        print(f"Moved {file_name} → {folder_name}/")
                    except Exception as e:
                        print(f"Error moving {file_name}: {e}")
                else:
                    print(f"File not found: {file_name}")

        return "Done"