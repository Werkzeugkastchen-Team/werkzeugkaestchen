import pytest
from tools.unit_converter.unit_converter_tool import UnitConverterTool
from flask_babel import lazy_gettext as _

class TestUnitConverterTool:

    def test_length_m_to_km(self):
        tool = UnitConverterTool()
        input_params = {
            _("Kategorie"): "länge",
            _("Wert"): "1000",
            _("Von Einheit"): "meter",
            _("Zu Einheit"): "kilometer"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert "1000.0 meter = 1.0 kilometer" in tool.output

    def test_weight_kg_to_g(self):
        tool = UnitConverterTool()
        input_params = {
            _("Kategorie"): "gewicht",
            _("Wert"): "2.5",
            _("Von Einheit"): "kilogramm",
            _("Zu Einheit"): "gramm"
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert "2.5 kilogramm = 2500.0 gramm" in tool.output

    def test_invalid_category(self):
        tool = UnitConverterTool()
        input_params = {
            _("Kategorie"): "volume",
            _("Wert"): "100",
            _("Von Einheit"): "l",
            _("Zu Einheit"): "ml"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Kategorie 'volume' wird nicht unterstützt" in tool.error_message

    def test_unknown_unit(self):
        tool = UnitConverterTool()
        input_params = {
            _("Kategorie"): "länge",
            _("Wert"): "10",
            _("Von Einheit"): "meter",
            _("Zu Einheit"): "parsec"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Unbekannte Einheit" in tool.error_message

    def test_invalid_value(self):
        tool = UnitConverterTool()
        input_params = {
            _("Kategorie"): "länge",
            _("Wert"): "abc",
            _("Von Einheit"): "meter",
            _("Zu Einheit"): "kilometer"
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert "Ungültiger Zahlenwert" in tool.error_message
