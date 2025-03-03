from abc import ABC, abstractmethod
from enum import Enum

class OutputType(Enum):
    """
    Attributes:
        FILE (str): Represents output type as a path to a file to then offer as download (eg /tmp/generated.mp4).
        TEXT (str): Represents output type as text.
    """
    FILE = "file"
    TEXT = "text"

class MiniTool(ABC):
    output = ""
    error_message = ""
    description = ""
    
    def __init__(self, name, identifier, output_type=OutputType.TEXT):
        self.name = name
        self.identifier = identifier
        self.output_type = output_type
        self.input_params = {}
    
    @abstractmethod    
    def execute_tool(self, input_params: dict) -> bool:
        """
        Executes the tool with the given input parameters.
        
        Returns True if the tool successfully passed, False if execution failed.
        """
        pass