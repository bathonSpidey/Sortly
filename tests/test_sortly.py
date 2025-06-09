import dotenv
import pytest
import os

from Sortly import Sortly

dotenv.load_dotenv()


class TestSortly:
    def test_sortly(self):
        sortly = Sortly(os.getenv("OPENAI_API_KEY"))
        root_folder_path = "C:\\Users\\batho\\Downloads\\SortlyTest"
        files = os.listdir(root_folder_path)
        user_message = (
            f"Sort this folder: {root_folder_path} with the contents: {files}."
        )
        result = sortly.sort_folder(user_prompt=user_message)
        assert result is not None
