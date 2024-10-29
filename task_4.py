from typing import Callable, Dict, List, Tuple, Optional
import re
from functools import wraps


def input_error(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner


def validate_phone(phone: str) -> bool:
    """Validate phone number format using regex."""
    return bool(re.match(r"^\+?\d{10,12}$", phone))


def validate_name(name: str) -> bool:
    """Validate contact name."""
    return bool(name) and name.isalnum() and len(name) >= 2


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse and normalize user input."""
    if not user_input.strip():
        return "", []
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = [arg.strip() for arg in parts[1:]]
    return cmd, args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """Add a new contact with validation."""
    if len(args) != 2:
        raise ValueError

    name, phone = args
    if not validate_name(name):
        return "Invalid name. Use alphanumeric characters (min 2 characters)."
    if not validate_phone(phone):
        return "Invalid phone. Use 10-12 digits, optionally starting with '+'."

    if name in contacts:
        return f"Contact {name} already exists. Use 'change' command to update."

    contacts[name] = phone
    return f"Contact {name} added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """Update existing contact with validation."""
    if len(args) != 2:
        raise ValueError

    name, new_phone = args
    if not validate_phone(new_phone):
        return "Invalid phone. Use 10-12 digits, optionally starting with '+'."

    if name not in contacts:
        raise KeyError

    contacts[name] = new_phone
    return f"Contact {name} updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    """Show phone number for a contact."""
    if len(args) != 1:
        raise ValueError

    name = args[0]
    if name not in contacts:
        raise KeyError

    return f"{name}'s phone: {contacts[name]}"


@input_error
def show_all(contacts: Dict[str, str]) -> str:
    """Show all contacts in a formatted way."""
    if not contacts:
        return "No contacts saved."

    return "\n".join(f"{name}: {phone}" for name, phone in sorted(contacts.items()))


def get_help() -> str:
    """Return help information about available commands."""
    return """
Available commands:
- hello: Get a greeting
- add [name] [phone]: Add new contact
- change [name] [new_phone]: Update existing contact
- phone [name]: Show phone for a contact
- all: Show all contacts
- help: Show this help message
- exit/close: Exit the program
    """.strip()


def handle_command(
    command: str, args: List[str], contacts: Dict[str, str]
) -> Optional[str]:
    """Handle command using command pattern."""
    commands = {
        "hello": lambda _: "How can I help you?",
        "add": lambda a: add_contact(a, contacts),
        "change": lambda a: change_contact(a, contacts),
        "phone": lambda a: show_phone(a, contacts),
        "all": lambda _: show_all(contacts),
        "help": lambda _: get_help(),
    }

    if command in ["close", "exit"]:
        return None

    handler = commands.get(command)
    if handler:
        return handler(args)
    return "Invalid command. Type 'help' for available commands."


def main():
    """Main function running the bot loop."""
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot! Type 'help' for available commands.")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parse_input(user_input)
            result = handle_command(command, args, contacts)

            if result is None:
                print("Good bye!")
                break

            print(result)

        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
