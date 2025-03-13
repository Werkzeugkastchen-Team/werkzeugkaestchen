from tool_interface import MiniTool
import random
import sys
import string

class RandomNumberGeneratorTool(MiniTool):
    name = "Zufallszahlengenerator"
    description = "Generiere eine Zufallszahl. Beispiel: Nenne mit eine Zahl zwischen 1 und 10"
    
    def __init__(self):
        super().__init__(self.name, "RandomNumberGeneratorTool")
        self.input_params = {
            "Minimum Number": "string",
            "Maximum Number": "string",
            "Amount of Rolls": "string"
        }
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            if not input_params.get("Minimum Number") or not input_params.get("Maximum Number") or not input_params.get("Amount of Rolls"):
                self.error_message = "Alle Eingabefelder müssen ausgefüllt sein."
                return False
            
            min = int(input_params.get("Minimum Number", ""))
            max = int(input_params.get("Maximum Number", ""))
            amount_of_rolls = int(input_params.get("Amount of Rolls", ""))
            
            if not min or not max or not amount_of_rolls:
                self.error_message = "Bitte geben Sie ganze Zahlen in alle Eingabefelder ein."
                return False
                        
            if min > max:
                self.error_message = "Das Minimum darf nicht größer als das Maximum sein."
                return False
            
            if min > sys.maxsize or max > sys.maxsize or min < -sys.maxsize:
                self.error_message = "Zahl zu hoch."
                return False
            
            if amount_of_rolls > 1000:
                self.error_message = "Anzahl Würfe zu hoch."
                return False

            random_numbers = [str(random.randint(min, max)) for _ in range(amount_of_rolls)]
            self.output = ", ".join(random_numbers)
            
            return True
        except Exception as e:
            self.error_message = str(e)
            return False 