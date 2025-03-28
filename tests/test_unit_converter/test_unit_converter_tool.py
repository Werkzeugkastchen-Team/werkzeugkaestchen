import pytest
from tools.unit_converter.unit_converter_tool import UnitConverterTool

class TestUnitConverterTool:

    def test_length_m_to_km(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "länge",
            "value": "1000",
            "from_unit": "meter",
            "to_unit": "kilometer"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert tool.output == "1000.0000 m = 1.0000 km"

    def test_weight_kg_to_g(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "gewicht",
            "value": "2.5",
            "from_unit": "kilogramm",
            "to_unit": "gramm"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert tool.output == "2.5000 kg = 2500.0000 g"

    def test_invalid_category(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "volume",
            "value": "100",
            "from_unit": "l",
            "to_unit": "ml"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Kategorie 'volume' wird nicht unterstützt" in tool.error_message

    def test_unknown_unit(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "länge",
            "value": "10",
            "from_unit": "meter",
            "to_unit": "parsec"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Unbekannte Einheit" in tool.error_message

    def test_invalid_value(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "länge",
            "value": "abc",
            "from_unit": "meter",
            "to_unit": "kilometer"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Ungültiger Zahlenwert" in tool.error_message
