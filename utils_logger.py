"""
Logger Module for PenDo
Handles logging of attempts and results
"""

import datetime
import json
import os
from pathlib import Path

class Logger:
    """
    Logger class for recording brute force attempts and results.
    """
    
    def __init__(self, log_dir="logs", verbose=False):
        """
        Initialize the logger.
        
        Args:
            log_dir (str): Directory to store log files
            verbose (bool): Enable verbose logging
        """
        self.log_dir = Path(log_dir)
        self.verbose = verbose
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(exist_ok=True)
        
        # Generate log filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"pendo_session_{timestamp}.log"
        self.json_file = self.log_dir / f"pendo_session_{timestamp}.json"
        
        # Initialize session data
        self.session_data = {
            'start_time': datetime.datetime.now().isoformat(),
            'attempts': [],
            'summary': {}
        }
        
        # Write initial log entry
        self._write_log("INFO", "PenDo session started")
        if self.verbose:
            print(f"📝 Logging to: {self.log_file}")
    
    def _write_log(self, level, message):
        """Write a log entry to the log file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_attempt(self, username, password, success, target):
        """
        Log a brute force attempt.
        
        Args:
            username (str): Username attempted
            password (str): Password attempted
            success (bool): Whether the attempt was successful
            target (str): Target system/service
        """
        timestamp = datetime.datetime.now().isoformat()
        
        # Create attempt record
        attempt_record = {
            'timestamp': timestamp,
            'username': username,
            'password_length': len(password),  # Don't log actual password for security
            'success': success,
            'target': target
        }
        
        # Add to session data
        self.session_data['attempts'].append(attempt_record)
        
        # Write to log file
        status = "SUCCESS" if success else "FAILED"
        self._write_log("ATTEMPT", f"Target: {target}, User: {username}, Status: {status}")
        
        if self.verbose:
            print(f"📝 Logged attempt #{len(self.session_data['attempts'])}")
    
    def log_session_end(self, total_attempts, successes, failures, duration):
        """
        Log the end of a session with summary statistics.
        
        Args:
            total_attempts (int): Total number of attempts
            successes (int): Number of successful attempts
            failures (int): Number of failed attempts
            duration (float): Duration of the session in seconds
        """
        self.session_data['end_time'] = datetime.datetime.now().isoformat()
        self.session_data['summary'] = {
            'total_attempts': total_attempts,
            'successes': successes,
            'failures': failures,
            'duration_seconds': duration,
            'attempts_per_second': total_attempts / max(duration, 0.01)
        }
        
        # Write summary to log file
        self._write_log("INFO", f"Session ended - Attempts: {total_attempts}, Successes: {successes}")
        
        # Write JSON session data
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2)
        
        if self.verbose:
            print(f"📊 Session data saved to: {self.json_file}")
    
    def log_error(self, error_message):
        """
        Log an error message.
        
        Args:
            error_message (str): Error message to log
        """
        self._write_log("ERROR", error_message)
        
        if self.verbose:
            print(f"❌ Error logged: {error_message}")
    
    def log_info(self, info_message):
        """
        Log an informational message.
        
        Args:
            info_message (str): Info message to log
        """
        self._write_log("INFO", info_message)
        
        if self.verbose:
            print(f"ℹ️  Info logged: {info_message}")
    
    def get_session_summary(self):
        """
        Get a summary of the current session.
        
        Returns:
            dict: Session summary data
        """
        return {
            'total_attempts': len(self.session_data['attempts']),
            'successes': sum(1 for attempt in self.session_data['attempts'] if attempt['success']),
            'failures': sum(1 for attempt in self.session_data['attempts'] if not attempt['success']),
            'start_time': self.session_data['start_time']
        }
    
    def export_results(self, format_type='json', filename=None):
        """
        Export session results to a file.
        
        Args:
            format_type (str): Export format ('json', 'csv')
            filename (str): Optional custom filename
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pendo_export_{timestamp}.{format_type}"
        
        export_path = self.log_dir / filename
        
        if format_type.lower() == 'json':
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2)
        
        elif format_type.lower() == 'csv':
            import csv
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                if self.session_data['attempts']:
                    writer = csv.DictWriter(f, fieldnames=self.session_data['attempts'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.session_data['attempts'])
        
        return export_path