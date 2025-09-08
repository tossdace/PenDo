"""
UI Module for PenDo
Handles all user interface elements including colors, banners, and animations
"""

import time
import sys
import os

try:
    from colorama import Fore, Back, Style, init
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

def setup_colors():
    """Initialize colorama if available."""
    if COLORAMA_AVAILABLE:
        init(autoreset=True)

def print_colored(text, color='white'):
    """Print colored text to terminal."""
    if not COLORAMA_AVAILABLE:
        print(text)
        return
    
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'bright_green': Fore.LIGHTGREEN_EX,
        'bright_red': Fore.LIGHTRED_EX,
        'bright_yellow': Fore.LIGHTYELLOW_EX,
    }
    
    color_code = color_map.get(color, Fore.WHITE)
    print(f"{color_code}{text}")

def display_banner():
    """Display the PenDo ASCII banner."""
    banner = f"""
{Fore.BRIGHT_GREEN_EX if COLORAMA_AVAILABLE else ''}
    ██████╗ ███████╗███╗   ██╗██████╗  ██████╗ 
    ██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔═══██╗
    ██████╔╝█████╗  ██╔██╗ ██║██║  ██║██║   ██║
    ██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██║   ██║
    ██║     ███████╗██║ ╚████║██████╔╝╚██████╔╝
    ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ 
    
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃        Educational Penetration Testing Tool     ┃
    ┃                 Version 1.0.0                   ┃
    ┃              For Authorized Use Only            ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}
    """
    print(banner)

def loading_animation():
    """Display a loading animation."""
    loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    print_colored("🔧 Initializing PenDo...", 'cyan')
    
    for i in range(20):
        char = loading_chars[i % len(loading_chars)]
        if COLORAMA_AVAILABLE:
            sys.stdout.write(f"\r{Fore.BRIGHT_GREEN_EX}{char} Loading modules... {i*5}%{Style.RESET_ALL}")
        else:
            sys.stdout.write(f"\r{char} Loading modules... {i*5}%")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print_colored("\r✅ Initialization complete!     ", 'green')

def progress_bar(current, total, width=50, prefix="Progress"):
    """Display a progress bar."""
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = '█' * filled + '░' * (width - filled)
    
    if COLORAMA_AVAILABLE:
        color = Fore.GREEN if percentage == 100 else Fore.YELLOW
        print(f"\r{color}{prefix}: |{bar}| {percentage:.1f}% ({current}/{total}){Style.RESET_ALL}", end='')
    else:
        print(f"\r{prefix}: |{bar}| {percentage:.1f}% ({current}/{total})", end='')
    
    if current == total:
        print()  # New line when complete

def display_attempt(attempt_num, username, password, status):
    """Display a single brute force attempt."""
    status_symbol = "✅" if status == "SUCCESS" else "❌" if status == "FAILED" else "🔄"
    
    if status == "SUCCESS":
        color = 'green'
    elif status == "FAILED":
        color = 'red'
    else:
        color = 'yellow'
    
    print_colored(f"   [{attempt_num:04d}] {status_symbol} {username}:{password} - {status}", color)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_stats(attempts, successes, failures, time_elapsed):
    """Display session statistics."""
    stats = f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                  SESSION STATS                   ┃
    ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃  Total Attempts: {attempts:>26}   ┃
    ┃  Successes:      {successes:>26}   ┃
    ┃  Failures:       {failures:>26}   ┃
    ┃  Time Elapsed:   {time_elapsed:>23.2f}s   ┃
    ┃  Avg per second: {attempts/max(time_elapsed,0.01):>23.2f}   ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    print_colored(stats, 'cyan')