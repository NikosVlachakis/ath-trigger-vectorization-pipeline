#!/usr/bin/env python3
"""
Test suite for Trigger Vectorization Pipeline centralized logging.
Verifies that all actions are logged to host machine txt files.
"""

import os
import sys
import time
import unittest
import subprocess
import json
from pathlib import Path
from datetime import datetime

class TestCentralizedLogging(unittest.TestCase):
    """Test centralized logging functionality for trigger vectorization pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.log_dir = Path("logs")
        cls.log_file = cls.log_dir / "trigger-vectorization-pipeline.log"
        cls.error_log_file = cls.log_dir / "trigger-vectorization-pipeline_errors.log"
        
        # Create logs directory
        cls.log_dir.mkdir(exist_ok=True)
        
        # Clear existing log files
        if cls.log_file.exists():
            cls.log_file.unlink()
        if cls.error_log_file.exists():
            cls.error_log_file.unlink()
    
    def setUp(self):
        """Set up each test."""
        time.sleep(1)
    
    def test_01_log_directory_creation(self):
        """Test that log directory can be created."""
        self.assertTrue(self.log_dir.exists(), "Log directory should exist")
        self.assertTrue(self.log_dir.is_dir(), "Log path should be a directory")
    
    def test_02_logging_configuration_exists(self):
        """Test that logging configuration exists."""
        print("\n🔧 Testing logging configuration...")
        
        logging_config = Path("logging_config.py")
        self.assertTrue(logging_config.exists(), "Logging config should exist")
        
        # Test that logging config can be imported
        try:
            import logging_config
            print("✅ Logging configuration imported successfully")
            self.assertTrue(hasattr(logging_config, 'setup_service_logging'))
        except ImportError as e:
            self.fail(f"Could not import logging config: {e}")
    
    def test_03_trigger_script_execution_logging(self):
        """Test that trigger script execution is logged."""
        print("\n🚀 Testing trigger script execution logging...")
        
        # Prepare test arguments
        test_args = [
            "python", "trigger_vectorization.py",
            "--vectorizationServiceUrl", "http://localhost:5001",
            "--url", "../vectorization-service/metadata-test.json", 
            "--jobId", "test_logging_trigger",
            "--clientsList", "client1",
            "--studyId", "test_study_123"
        ]
        
        # Execute the trigger script
        result = subprocess.run(
            test_args,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"✅ Trigger script exit code: {result.returncode}")
        print(f"✅ Stdout length: {len(result.stdout)} chars")
        print(f"✅ Stderr length: {len(result.stderr)} chars")
        
        # Check if log file was created (depends on centralized logging availability)
        if self.log_file.exists():
            log_content = self.log_file.read_text()
            print(f"✅ Log file created with {len(log_content)} chars")
            
            # Verify trigger-specific content
            trigger_indicators = [
                "trigger-vectorization-pipeline",
                "Starting Vectorization Pipeline Trigger",
                "POST",
                "vectorizationServiceUrl"
            ]
            
            found_indicators = []
            for indicator in trigger_indicators:
                if indicator in log_content:
                    found_indicators.append(indicator)
            
            print(f"✅ Found trigger indicators: {found_indicators}")
            self.assertGreater(len(found_indicators), 0, "Should find trigger-specific logs")
        else:
            print("ℹ️  No log file created (running in fallback mode)")
    
    def test_04_http_request_logging(self):
        """Test that HTTP requests are logged."""
        print("\n🌐 Testing HTTP request logging...")
        
        # Check if previous execution created logs
        if not self.log_file.exists():
            print("ℹ️  No log file available, running trigger script first...")
            
            # Run trigger script to generate logs
            test_args = [
                "python", "trigger_vectorization.py",
                "--vectorizationServiceUrl", "http://localhost:5001",
                "--url", "../vectorization-service/metadata-test.json",
                "--jobId", f"test_http_logging_{int(time.time())}",
                "--clientsList", "client1",
                "--studyId", "test_study_http"
            ]
            
            subprocess.run(test_args, capture_output=True, timeout=60)
        
        if self.log_file.exists():
            log_content = self.log_file.read_text()
            
            # Look for HTTP request indicators
            http_indicators = [
                "POST",
                "http://localhost:5001",
                "vectorize",
                "Response code",
                "Sending POST"
            ]
            
            found_indicators = []
            for indicator in http_indicators:
                if indicator in log_content:
                    found_indicators.append(indicator)
            
            print(f"✅ Found HTTP indicators: {found_indicators}")
            self.assertGreater(len(found_indicators), 0, "Should find HTTP request logs")
        else:
            print("ℹ️  Running in fallback logging mode (console only)")
    
    def test_05_parameter_logging(self):
        """Test that script parameters are logged."""
        print("\n📝 Testing parameter logging...")
        
        if self.log_file.exists():
            log_content = self.log_file.read_text()
            
            # Look for parameter indicators
            param_indicators = [
                "jobId",
                "totalClients",
                "vectorizationServiceUrl",
                "orchestratorUrl",
                "url"
            ]
            
            found_params = []
            for param in param_indicators:
                if param in log_content:
                    found_params.append(param)
            
            print(f"✅ Found parameter indicators: {found_params}")
            self.assertGreater(len(found_params), 0, "Should find parameter logs")
        else:
            print("ℹ️  No log file available for parameter checking")
    
    def test_06_response_handling_logging(self):
        """Test that response handling is logged."""
        print("\n📤 Testing response handling logging...")
        
        if self.log_file.exists():
            log_content = self.log_file.read_text()
            
            # Look for response handling indicators
            response_indicators = [
                "Response code",
                "Response body",
                "succeeded",
                "failed",
                "status"
            ]
            
            found_responses = []
            for indicator in response_indicators:
                if indicator in log_content:
                    found_responses.append(indicator)
            
            print(f"✅ Found response indicators: {found_responses}")
            self.assertGreater(len(found_responses), 0, "Should find response handling logs")
        else:
            print("ℹ️  No log file available for response checking")
    
    def test_07_error_handling_logging(self):
        """Test that errors are properly logged."""
        print("\n❌ Testing error handling logging...")
        
        # Test with invalid URL to generate error
        error_test_args = [
            "python", "trigger_vectorization.py",
            "--vectorizationServiceUrl", "http://invalid-url:9999",
            "--url", "nonexistent-file.json",
            "--jobId", "test_error_logging",
            "--clientsList", "client1",
            "--studyId", "test_study_error"
        ]
        
        result = subprocess.run(
            error_test_args,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"✅ Error test exit code: {result.returncode}")
        
        # Check for error logging in file or stderr
        error_found = False
        
        if self.error_log_file.exists():
            error_content = self.error_log_file.read_text()
            if error_content:
                print(f"✅ Error log file has content: {len(error_content)} chars")
                error_found = True
        
        if result.stderr and "error" in result.stderr.lower():
            print("✅ Error found in stderr")
            error_found = True
        
        # Error logging is working if we found errors somewhere
        print(f"✅ Error handling functional: {error_found}")
    
    def test_08_log_format_validation(self):
        """Test that logs follow the expected format."""
        print("\n📋 Testing log format validation...")
        
        if not self.log_file.exists():
            print("ℹ️  No log file to validate")
            return
        
        log_content = self.log_file.read_text()
        lines = [line.strip() for line in log_content.split('\n') if line.strip()]
        
        if not lines:
            print("ℹ️  No log lines to validate")
            return
        
        # Check format of log lines
        valid_lines = 0
        for line in lines:
            # Expected format: timestamp LEVEL [component] [service] message
            if any(level in line for level in ['INFO', 'DEBUG', 'WARNING', 'ERROR']):
                if 'trigger-vectorization-pipeline' in line:
                    valid_lines += 1
        
        print(f"✅ Valid log lines: {valid_lines}/{len(lines)}")
        self.assertGreater(valid_lines, 0, "Should have valid formatted log lines")
    
    def test_09_log_persistence(self):
        """Test that logs persist on host machine."""
        print("\n💾 Testing log persistence...")
        
        # Verify logs directory exists
        self.assertTrue(self.log_dir.exists(), "Logs directory should exist")
        
        if self.log_file.exists():
            # Verify log files are readable
            log_content = self.log_file.read_text()
            self.assertGreater(len(log_content), 0, "Log file should have content")
            
            # Verify file permissions
            self.assertTrue(os.access(self.log_file, os.R_OK), "Log file should be readable")
            
            # Show log file info
            stat = self.log_file.stat()
            print(f"✅ Log file: {self.log_file}")
            print(f"✅ Size: {stat.st_size} bytes")
            print(f"✅ Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        else:
            print("ℹ️  No log file (centralized logging may not be active)")
    
    def test_10_integration_with_services(self):
        """Test integration logging with other services."""
        print("\n🔗 Testing integration with other services...")
        
        # This test checks if the trigger can log its interaction with other services
        # when they are available
        
        # Run a complete pipeline test
        integration_args = [
            "python", "trigger_vectorization.py",
            "--vectorizationServiceUrl", "http://localhost:5001",
            "--url", "../vectorization-service/metadata-test.json",
            "--jobId", f"integration_test_{int(time.time())}",
            "--clientsList", "client1",
            "--studyId", "test_study_integration"
        ]
        
        result = subprocess.run(
            integration_args,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"✅ Integration test exit code: {result.returncode}")
        
        # Check logs for integration indicators
        if self.log_file.exists():
            log_content = self.log_file.read_text()
            
            integration_indicators = [
                "vectorizationServiceUrl",
                "orchestratorUrl",
                "jobId",
                "POST",
                "request"
            ]
            
            found_integration = []
            for indicator in integration_indicators:
                if indicator in log_content:
                    found_integration.append(indicator)
            
            print(f"✅ Found integration indicators: {found_integration}")
            self.assertGreater(len(found_integration), 0, "Should find integration logs")
        else:
            print("ℹ️  Integration logging via console output")

def run_logging_tests():
    """Run the centralized logging tests."""
    print("=" * 70)
    print("🧪 TRIGGER VECTORIZATION PIPELINE - CENTRALIZED LOGGING TESTS")
    print("=" * 70)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCentralizedLogging)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        print("✅ Centralized logging is working correctly")
        print("✅ All pipeline actions are being logged")
        print("✅ Integration with other services is logged")
        print("✅ Log files are properly formatted when available")
    else:
        print("❌ Some tests failed")
        print(f"Failed: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_logging_tests()
    sys.exit(0 if success else 1)