from abc import ABC, abstractmethod

class MiniTool(ABC):
    output = ""
    error_message = ""
    
    def __init__(self, name):
        self.name = name
        self.input_params = {}
    
    @abstractmethod    
    def execute_tool(self, input_params: dict) -> bool:
        """
        Executes the tool with the given input parameters.
        
        Returns True if the tool successfully passed, False if execution failed.
        """
        pass