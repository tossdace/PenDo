"""
Brute Force Engine Module for PenDo
Handles the core brute force simulation logic
"""

import time
import random
from pathlib import Path
from .ui import print_colored, display_attempt, progress_bar, display_stats

class BruteForceEngine:
    """
    Brute force simulation engine for educational purposes.
    This simulates brute force attacks without actually connecting to real services.
    """
    
    def __init__(self, username, wordlist_path, target, delay=0.5, logger=None):
        """
        Initialize the brute force engine.
        
        Args:
            username (str): Target username
            wordlist_path (str): Path to password wordlist
            target (str): Target service/system
            delay (float): Delay between attempts
            logger: Logger instance
        """
        self.username = username
        self.wordlist_path = wordlist_path
        self.target = target
        self.delay = delay
        self.logger = logger
        
        self.attempts = 0
        self.successes = 0
        self.failures = 0
        self.start_time = None
        
        # Load wordlist
        self.passwords = self._load_wordlist()
        
        # Simulate a "correct" password for demo purposes
        # In a real tool, this would attempt actual authentication
        self.simulated_password = self._select_demo_password()
    
    def _load_wordlist(self):
        """Load passwords from wordlist file."""
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            print_colored(f"📋 Loaded {len(passwords)} passwords from wordlist", 'cyan')
            return passwords
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Wordlist file not found: {self.wordlist_path}")
        except Exception as e:
            raise Exception(f"Error loading wordlist: {str(e)}")
    
    def _select_demo_password(self):
        """
        Select a password from the wordlist for demonstration.
        In simulation mode, we'll randomly pick one to "succeed" with.
        """
        if not self.passwords:
            return None
        
        # For demo purposes, select a password from the middle portion
        # This makes it more realistic than always succeeding immediately
        start_idx = len(self.passwords) // 4
        end_idx = len(self.passwords) * 3 // 4
        
        if start_idx < end_idx:
            return random.choice(self.passwords[start_idx:end_idx])
        else:
            return random.choice(self.passwords)
    
    def _simulate_attempt(self, password):
        """
        Simulate a brute force attempt.
        
        Args:
            password (str): Password to attempt
            
        Returns:
            bool: True if simulated success, False otherwise
        """
        # Add realistic delay
        time.sleep(self.delay)
        
        # In simulation mode, check against our demo password
        if self.target == 'simulation':
            return password == self.simulated_password
        
        # For other targets, this would contain actual connection logic
        # For now, always return False to simulate failure
        return False
    
    def _log_attempt(self, password, success):
        """Log an attempt."""
        self.attempts += 1
        
        if success:
            self.successes += 1
            status = "SUCCESS"
        else:
            self.failures += 1
            status = "FAILED"
        
        # Display attempt
        display_attempt(self.attempts, self.username, password, status)
        
        # Log to logger if available
        if self.logger:
            self.logger.log_attempt(self.username, password, success, self.target)
    
    def run(self):
        """
        Run the brute force simulation.
        
        Returns:
            dict: Results of the brute force attempt
        """
        self.start_time = time.time()
        
        print_colored(f"🎯 Target: {self.target}", 'white')
        print_colored(f"👤 Username: {self.username}", 'white')
        print_colored(f"🔑 Testing {len(self.passwords)} passwords...\n", 'white')
        
        try:
            for i, password in enumerate(self.passwords):
                # Update progress bar every 10 attempts or on last attempt
                if i % 10 == 0 or i == len(self.passwords) - 1:
                    progress_bar(i + 1, len(self.passwords), prefix="Testing")
                
                # Attempt the password
                success = self._simulate_attempt(password)
                
                # Log the attempt
                self._log_attempt(password, success)
                
                # If successful, break the loop
                if success:
                    end_time = time.time()
                    time_taken = end_time - self.start_time
                    
                    return {
                        'success': True,
                        'password': password,
                        'attempts': self.attempts,
                        'time_taken': time_taken
                    }
            
            # If we get here, no password worked
            end_time = time.time()
            time_taken = end_time - self.start_time
            
            return {
                'success': False,
                'password': None,
                'attempts': self.attempts,
                'time_taken': time_taken
            }
            
        except KeyboardInterrupt:
            # Handle user interruption gracefully
            end_time = time.time()
            time_taken = end_time - self.start_time
            
            print_colored("\n\n⚡ Attack interrupted by user", 'yellow')
            display_stats(self.attempts, self.successes, self.failures, time_taken)
            
            raise KeyboardInterrupt()
        
        finally:
            # Display final stats
            if hasattr(self, 'start_time') and self.start_time:
                end_time = time.time()
                time_taken = end_time - self.start_time
                display_stats(self.attempts, self.successes, self.failures, time_taken)

class PasswordGenerator:
    """Utility class for generating password variations."""
    
    @staticmethod
    def generate_variations(base_password):
        """
        Generate common password variations.
        
        Args:
            base_password (str): Base password to create variations from
            
        Returns:
            list: List of password variations
        """
        variations = [base_password]
        
        # Common substitutions
        substitutions = {
            'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
        }
        
        # Apply substitutions
        modified = base_password.lower()
        for old, new in substitutions.items():
            modified = modified.replace(old, new)
        if modified != base_password.lower():
            variations.append(modified)
        
        # Add common suffixes
        common_suffixes = ['123', '!', '1', '2023', '2024', '2025']
        for suffix in common_suffixes:
            variations.append(base_password + suffix)
        
        # Capitalization variations
        if base_password.islower():
            variations.append(base_password.capitalize())
            variations.append(base_password.upper())
        
        return list(set(variations))  # Remove duplicates