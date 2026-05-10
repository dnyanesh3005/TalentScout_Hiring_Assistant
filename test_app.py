"""
Testing and Demo Script for TalentScout Hiring Assistant
Demonstrates various features and utility functions
"""

import sys
from typing import List, Dict
from utils import (
    is_exit_command,
    extract_email,
    extract_phone,
    extract_tech_stack,
    extract_years_from_text,
    is_valid_email,
    is_valid_phone,
    format_candidate_summary,
    parse_json_response,
    build_conversation_text,
    create_test_conversation,
)

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_test(test_name: str, result: bool, details: str = ""):
    """Print test result"""
    status = f"{Colors.OKGREEN}✅ PASS{Colors.ENDC}" if result else f"{Colors.FAIL}❌ FAIL{Colors.ENDC}"
    print(f"  {status} | {test_name}")
    if details:
        print(f"    {Colors.OKCYAN}{details}{Colors.ENDC}")


def test_string_utilities():
    """Test string utility functions"""
    print_section("Testing String Utilities")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Exit command detection
    tests_total += 1
    result = is_exit_command("goodbye!")
    print_test("Exit command detection", result, "detected 'goodbye'")
    if result:
        tests_passed += 1
    
    tests_total += 1
    result = not is_exit_command("hello world")
    print_test("Non-exit command detection", result, "correctly rejected 'hello world'")
    if result:
        tests_passed += 1
    
    # Test 2: Email extraction
    tests_total += 1
    email = extract_email("You can reach me at john.doe@example.com for more info")
    result = email == "john.doe@example.com"
    print_test("Email extraction", result, f"extracted: {email}")
    if result:
        tests_passed += 1
    
    # Test 3: Phone extraction
    tests_total += 1
    phone = extract_phone("Call me at +1-555-123-4567")
    result = phone is not None and len(phone) > 0
    print_test("Phone extraction", result, f"extracted: {phone}")
    if result:
        tests_passed += 1
    
    # Test 4: Tech stack extraction
    tests_total += 1
    tech_stack = extract_tech_stack("I'm proficient in Python, React, and Docker")
    result = "python" in tech_stack and "react" in tech_stack
    print_test("Tech stack extraction", result, f"found: {tech_stack[:30]}...")
    if result:
        tests_passed += 1
    
    # Test 5: Years from text
    tests_total += 1
    years = extract_years_from_text("I have 7 years of experience in software development")
    result = years == 7
    print_test("Years extraction", result, f"extracted: {years} years")
    if result:
        tests_passed += 1
    
    return tests_passed, tests_total


def test_validation():
    """Test validation functions"""
    print_section("Testing Validation Functions")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Valid email
    tests_total += 1
    result = is_valid_email("john@example.com")
    print_test("Valid email detection", result, "john@example.com")
    if result:
        tests_passed += 1
    
    # Test 2: Invalid email
    tests_total += 1
    result = not is_valid_email("not-an-email")
    print_test("Invalid email rejection", result, "correctly rejected 'not-an-email'")
    if result:
        tests_passed += 1
    
    # Test 3: Valid phone
    tests_total += 1
    result = is_valid_phone("5551234567") or is_valid_phone("+1-555-123-4567")
    print_test("Valid phone detection", result, "phone number accepted")
    if result:
        tests_passed += 1
    
    # Test 4: Invalid phone
    tests_total += 1
    result = not is_valid_phone("123")  # Too short
    print_test("Invalid phone rejection", result, "correctly rejected '123'")
    if result:
        tests_passed += 1
    
    return tests_passed, tests_total


def test_data_extraction():
    """Test data extraction from JSON"""
    print_section("Testing JSON Extraction")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Valid JSON parsing
    tests_total += 1
    json_str = '{"name": "John", "email": "john@example.com"}'
    result = parse_json_response(json_str)
    success = result is not None and result.get("name") == "John"
    print_test("Valid JSON parsing", success, f"parsed: {result}")
    if success:
        tests_passed += 1
    
    # Test 2: JSON in markdown code block
    tests_total += 1
    json_str = '```json\n{"age": 30}\n```'
    result = parse_json_response(json_str)
    success = result is not None and result.get("age") == 30
    print_test("Markdown JSON parsing", success, f"extracted from markdown block")
    if success:
        tests_passed += 1
    
    # Test 3: JSON in curly braces
    tests_total += 1
    json_str = 'Some text before {"status": "ok"} and after'
    result = parse_json_response(json_str)
    success = result is not None and result.get("status") == "ok"
    print_test("Embedded JSON parsing", success, "extracted from mixed content")
    if success:
        tests_passed += 1
    
    return tests_passed, tests_total


def test_conversation_utilities():
    """Test conversation handling utilities"""
    print_section("Testing Conversation Utilities")
    
    tests_passed = 0
    tests_total = 0
    
    # Create test conversation
    messages = create_test_conversation()
    
    # Test 1: Conversation building
    tests_total += 1
    conv_text = build_conversation_text(messages)
    result = "Hello! Welcome to TalentScout" in conv_text
    print_test("Conversation text building", result, "successfully built conversation text")
    if result:
        tests_passed += 1
    
    # Test 2: Candidate summary formatting
    tests_total += 1
    candidate_info = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "555-1234",
        "years_of_experience": 5,
        "desired_positions": "Backend Developer",
        "current_location": "San Francisco",
        "tech_stack": ["Python", "Django", "PostgreSQL"]
    }
    summary = format_candidate_summary(candidate_info)
    result = "John Doe" in summary and "5 years" in summary
    print_test("Candidate summary formatting", result, "summary formatted correctly")
    if result:
        tests_passed += 1
    
    return tests_passed, tests_total


def test_sample_workflow():
    """Demonstrate a sample workflow"""
    print_section("Sample Workflow Demonstration")
    
    print(f"{Colors.OKBLUE}Simulating a candidate interview interaction...{Colors.ENDC}\n")
    
    # Sample user inputs
    sample_inputs = [
        ("Candidate: hello!", "System: Greeting detected"),
        ("Candidate: My name is Alice Johnson", "System: Name extracted: Alice Johnson"),
        ("Candidate: You can reach me at alice@techcompany.com", "System: Email extracted"),
        ("Candidate: I have 8 years of experience", "System: Experience: 8 years"),
        ("Candidate: I know Python, JavaScript, React, and Docker", "System: Tech stack identified"),
        ("Candidate: goodbye!", "System: Exit command detected - Concluding interview"),
    ]
    
    for user_input, system_response in sample_inputs:
        print(f"  {Colors.OKCYAN}{user_input}{Colors.ENDC}")
        
        # Demonstrate processing
        if "hello" in user_input.lower():
            is_greeting = True
        elif "goodbye" in user_input.lower():
            is_exit = is_exit_command(user_input)
        elif "@" in user_input:
            email = extract_email(user_input)
        elif "years" in user_input:
            years = extract_years_from_text(user_input)
        elif any(tech in user_input.lower() for tech in ["python", "javascript", "react", "docker"]):
            tech_stack = extract_tech_stack(user_input)
        
        print(f"  {Colors.OKGREEN}{system_response}{Colors.ENDC}\n")


def run_all_tests():
    """Run all tests and display summary"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   TalentScout Hiring Assistant - Test Suite           ║")
    print("║                Version 1.0                            ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    all_passed = 0
    all_total = 0
    
    # Run test suites
    test_suites = [
        ("String Utilities", test_string_utilities),
        ("Validation", test_validation),
        ("Data Extraction", test_data_extraction),
        ("Conversation Utilities", test_conversation_utilities),
    ]
    
    for suite_name, test_func in test_suites:
        passed, total = test_func()
        all_passed += passed
        all_total += total
    
    # Demonstrate workflow
    test_sample_workflow()
    
    # Summary
    print_section("Test Summary")
    success_rate = (all_passed / all_total * 100) if all_total > 0 else 0
    
    print(f"  {Colors.BOLD}Total Tests:{Colors.ENDC} {all_total}")
    print(f"  {Colors.OKGREEN}Passed:{Colors.ENDC} {all_passed}")
    print(f"  {Colors.FAIL}Failed:{Colors.ENDC} {all_total - all_passed}")
    print(f"  {Colors.BOLD}Success Rate:{Colors.ENDC} {success_rate:.1f}%\n")
    
    if all_passed == all_total:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ All tests passed successfully!{Colors.ENDC}\n")
        return 0
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠️  Some tests failed. Please review the output above.{Colors.ENDC}\n")
        return 1


def print_feature_overview():
    """Print feature overview"""
    print_section("Feature Overview")
    
    features = [
        ("✅ Conversational Interview", "Natural dialogue with candidates"),
        ("✅ Information Gathering", "Collects candidate details automatically"),
        ("✅ Tech Stack Assessment", "Identifies technology proficiency"),
        ("✅ Dynamic Questions", "Generates relevant technical questions"),
        ("✅ Context Maintenance", "Remembers previous information"),
        ("✅ Exit Handling", "Graceful conversation conclusion"),
        ("✅ Data Export", "Download interview data (JSON, Markdown)"),
        ("✅ Professional UI", "Clean Streamlit interface"),
    ]
    
    for feature, description in features:
        print(f"  {feature:30} → {description}")


if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        print_feature_overview()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Error running tests: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)