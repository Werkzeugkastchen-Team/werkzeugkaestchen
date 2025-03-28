import pytest
from tools.unit_converter.unit_converter_tool import UnitConverterTool

class TestUnitConverterTool:

    def test_length_m_to_km(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "length",
            "value": "1000",
            "from_unit": "m",
            "to_unit": "km"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert "1.0 km" in tool.output

    def test_weight_kg_to_g(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "weight",
            "value": "2.5",
            "from_unit": "kg",
            "to_unit": "g"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert "2500.0 g" in tool.output

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
            "category": "length",
            "value": "10",
            "from_unit": "m",
            "to_unit": "parsec"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Unbekannte Einheit" in tool.error_message

    def test_invalid_value(self):
        tool = UnitConverterTool()
        input_params = {
            "category": "length",
            "value": "abc",
            "from_unit": "m",
            "to_unit": "km"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Ungültiger Zahlenwert" in tool.error_message
