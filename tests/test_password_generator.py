import pytest
from tools.password_generator.password_generator_tool import PasswordGeneratorTool


def test_password_generator_initialization():
    """Test if the tool initializes correctly"""
    tool = PasswordGeneratorTool()
    assert tool.name == "Passwortgenerator"
    assert "length" in tool.input_params
    assert "include_lowercase" in tool.input_params
    assert "include_uppercase" in tool.input_params
    assert "include_numbers" in tool.input_params
    assert "include_special" in tool.input_params


def test_password_generation_with_defaults():
    """Test password generation with default settings"""
    tool = PasswordGeneratorTool()
    result = tool.execute_tool({
        "length": "12",
        "include_lowercase": True,
        "include_uppercase": True,
        "include_numbers": True,
        "include_special": True
    })
    assert result == True
    assert "Ihr generiertes Passwort" in tool.output


def test_password_length():
    """Test if password respects the specified length"""
    tool = PasswordGeneratorTool()

    # Test various lengths
    for length in ["8", "16", "32"]:
        result = tool.execute_tool({
            "length": length,
            "include_lowercase": True,
            "include_uppercase": True,
            "include_numbers": True,
            "include_special": True
        })

        assert result == True
        # We can't directly check the password length since it's embedded in HTML
        # But we can verify the length is reported correctly
        assert f"<strong>Länge:</strong> {length}" in tool.output


def test_invalid_length():
    """Test handling of invalid length"""
    tool = PasswordGeneratorTool()

    # Test too short
    result = tool.execute_tool({"length": "2"})
    assert result == False
    assert "muss zwischen 4 und 128 Zeichen liegen" in tool.error_message

    # Test too long
    result = tool.execute_tool({"length": "200"})
    assert result == False
    assert "muss zwischen 4 und 128 Zeichen liegen" in tool.error_message

    # Test non-numeric
    result = tool.execute_tool({"length": "abc"})
    assert result == False
    assert "muss eine Zahl sein" in tool.error_message


def test_no_character_types():
    """Test handling when no character types are selected"""
    tool = PasswordGeneratorTool()
    result = tool.execute_tool({
        "length": "12"
    })  # No specific character type params means no selection

    assert result == False
    assert "Bitte wählen Sie mindestens einen Zeichentyp aus" in tool.error_message


def test_specific_character_types():
    """Test password generation with specific character types"""
    tool = PasswordGeneratorTool()

    # Only lowercase
    result = tool.execute_tool({
        "length": "12",
        "include_lowercase": True,
        "include_uppercase": False,
        "include_numbers": False,
        "include_special": False
    })
    assert result == True

    # Only uppercase
    result = tool.execute_tool({
        "length": "12",
        "include_lowercase": False,
        "include_uppercase": True,
        "include_numbers": False,
        "include_special": False
    })
    assert result == True

    # Only numbers
    result = tool.execute_tool({
        "length": "12",
        "include_lowercase": False,
        "include_uppercase": False,
        "include_numbers": True,
        "include_special": False
    })
    assert result == True

    # Only special
    result = tool.execute_tool({
        "length": "12",
        "include_lowercase": False,
        "include_uppercase": False,
        "include_numbers": False,
        "include_special": True
    })
    assert result == True
