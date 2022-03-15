'''
Copyright 2022 Simone Sestito
This file is part of "Docker Projects Manager".

"Docker Projects Manager" is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Docker Projects Manager" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with "Docker Projects Manager".  If not, see <http://www.gnu.org/licenses/>.
'''

from simple_term_menu import TerminalMenu

def show_menu(options: list, default=None) -> str:
    # options[i] = (key, display_value, return_value)
    if default is None:
        selected_index = TerminalMenu([v for _, v, _ in options]).show()
        selected_option = options[selected_index]
    else:
        selected_option = next(
            (option for option in options if option[0] == default),
            None
        )
        if selected_option is None:
            raise Exception("Invalid option: " + default)
    
    return selected_option[2]

def ask_yes_no(question: str, default: bool) -> bool:
    if default:
        reply = input(f'{question} [Y/n] ')
    else:
        reply = input(f'{question} [y/N] ')
    reply = reply.lower()

    if reply.startswith('y'): return True
    if reply.startswith('n'): return False
    return default