# ============================================================================
# FC-001 | Fashion Cube QA Automation - AI Failure Analyzer
# Requirement: Classify test failures and suggest fixes
# Categories: Locator, Timing, Business Logic, API, Data, Performance
# ============================================================================

import re
import json
import sys
from datetime import datetime


class AIFailureAnalyzer:
    """FC-001: AI-powered test failure root cause analyzer.

    Classifies failures into:
        - Locator issue
        - Timing issue
        - Business logic defect
        - API defect
        - Data problem
        - Performance bottleneck

    Provides:
        - Exact root cause
        - Code-level fix
        - Application-level fix (if required)
    """

    # ---- Pattern Definitions ----
    PATTERNS = {
        "locator_issue": {
            "patterns": [
                r"Element.*not found",
                r"selector.*not.*visible",
                r"No element matches",
                r"waiting for selector",
                r"locator.*resolved to.*elements",
                r"page\.locator\(",
                r"ElementNotFound",
                r"InvalidSelectorError",
                r"could not find element",
                r"NoSuchElementException",
            ],
            "description": "Locator Issue",
            "icon": "🎯",
        },
        "timing_issue": {
            "patterns": [
                r"Timeout.*exceeded",
                r"TimeoutError",
                r"waiting for.*timed out",
                r"navigation timeout",
                r"page\.wait_for",
                r"within \d+ms",
                r"exceeded \d+ milliseconds",
                r"net::ERR_CONNECTION_TIMED_OUT",
            ],
            "description": "Timing Issue",
            "icon": "⏱️",
        },
        "business_logic_defect": {
            "patterns": [
                r"AssertionError.*Expected",
                r"assert.*==",
                r"assert.*!=",
                r"assert.*in",
                r"not equal",
                r"expected.*but got",
                r"mismatch",
                r"incorrect.*value",
                r"wrong.*result",
            ],
            "description": "Business Logic Defect",
            "icon": "🧠",
        },
        "api_defect": {
            "patterns": [
                r"status.*code.*[45]\d{2}",
                r"HTTP.*[45]\d{2}",
                r"ConnectionError",
                r"ConnectionRefusedError",
                r"requests\.exceptions",
                r"JSONDecodeError",
                r"Invalid JSON",
                r"net::ERR_CONNECTION_REFUSED",
                r"ECONNREFUSED",
                r"502 Bad Gateway",
                r"503 Service Unavailable",
            ],
            "description": "API Defect",
            "icon": "🌐",
        },
        "data_problem": {
            "patterns": [
                r"KeyError",
                r"IndexError",
                r"NoneType.*attribute",
                r"null.*undefined",
                r"missing.*field",
                r"schema.*validation",
                r"ValidationError",
                r"data.*not found",
                r"empty.*response",
            ],
            "description": "Data Problem",
            "icon": "📊",
        },
        "performance_bottleneck": {
            "patterns": [
                r"threshold.*exceeded",
                r"p95.*exceeded",
                r"p99.*exceeded",
                r"rate.*exceeded",
                r"response.*time.*>\s*\d+",
                r"slow.*response",
                r"memory.*exceeded",
                r"CPU.*spike",
                r"MemoryError",
            ],
            "description": "Performance Bottleneck",
            "icon": "🚀",
        },
    }

    # ---- Fix Suggestions ----
    FIX_SUGGESTIONS = {
        "locator_issue": {
            "root_cause": "The test is using a selector that does not match any element on the page. This can happen when the UI changes, dynamic IDs are used, or the element has not rendered yet.",
            "code_fix": [
                "1. Update the locator in the Page Object to match the current DOM structure.",
                "2. Use more stable selectors: prefer data-testid > id > CSS class > XPath.",
                "3. Add explicit waits before interacting with the element:",
                "   page.wait_for_selector('selector', state='visible', timeout=30000)",
                "4. Verify the element exists in the DOM using browser DevTools.",
                "5. Check if the element is inside an iframe or shadow DOM.",
            ],
            "app_fix": "If the UI was intentionally changed, update the test locators to match. Consider adding data-testid attributes to critical UI elements for test stability.",
        },
        "timing_issue": {
            "root_cause": "The test is timing out waiting for an element, page load, or network request. This typically indicates slow page rendering, unresponsive backend, or insufficient wait times.",
            "code_fix": [
                "1. Increase the timeout value in the wait call:",
                "   page.wait_for_selector('selector', timeout=60000)",
                "2. Use wait_for_load_state('networkidle') after navigation.",
                "3. Add retry logic for flaky network conditions.",
                "4. Replace fixed sleep() with explicit waits on specific conditions.",
                "5. Check if the tested feature requires backend services to be running.",
            ],
            "app_fix": "Investigate server-side performance issues. Check for slow database queries, unoptimized API responses, or resource-intensive operations blocking the UI.",
        },
        "business_logic_defect": {
            "root_cause": "An assertion failed because the actual behavior does not match the expected behavior defined in the test. This indicates a potential bug in the application logic.",
            "code_fix": [
                "1. Verify the expected values in the test match the current requirements.",
                "2. Check if the test data is still valid and up-to-date.",
                "3. Add more descriptive assertion messages for easier debugging.",
                "4. Log the actual values before assertions for comparison.",
                "5. If the requirement changed, update both test and expected values.",
            ],
            "app_fix": "Review the business logic in the application code. Compare the actual behavior against the Jira requirement (FC-001). File a bug if the behavior deviates from the spec.",
        },
        "api_defect": {
            "root_cause": "The API returned an unexpected status code or the connection was refused. This indicates the API server is down, the endpoint has changed, or there is a network issue.",
            "code_fix": [
                "1. Verify the API server is running and accessible.",
                "2. Check the endpoint URL matches the actual server routes.",
                "3. Verify request headers (authorization, content-type).",
                "4. Add connection retry logic with exponential backoff.",
                "5. Check for CORS issues if testing from a different origin.",
            ],
            "app_fix": "Check server logs for errors. Verify the API endpoint is deployed correctly. Check database connectivity and middleware configuration.",
        },
        "data_problem": {
            "root_cause": "The test encountered missing or malformed data in the API response or page content. This can be caused by empty database, stale test data, or schema changes.",
            "code_fix": [
                "1. Add null/undefined checks before accessing nested properties.",
                "2. Validate API response schema before processing data.",
                "3. Use test fixtures or seed data to ensure consistent test data.",
                "4. Add defensive error handling for missing fields.",
                "5. Check if the database has been seeded with test data.",
            ],
            "app_fix": "Run the database seed script to populate test data. Verify the API response schema matches the frontend expectations. Check for missing required fields in the data model.",
        },
        "performance_bottleneck": {
            "root_cause": "Performance thresholds were exceeded. Response times or error rates are higher than the defined acceptable limits.",
            "code_fix": [
                "1. Review k6 threshold settings and adjust if needed.",
                "2. Check if the VU count is realistic for the environment.",
                "3. Verify the test environment has sufficient resources.",
                "4. Add response time breakdown to identify slow endpoints.",
                "5. Run the test during off-peak hours to eliminate noise.",
            ],
            "app_fix": "Profile the application for slow database queries. Add caching for frequently accessed data. Optimize API response sizes. Consider horizontal scaling.",
        },
    }

    def __init__(self):
        self.results = []

    def analyze(self, log_text):
        """FC-001: Analyze a failure log and classify the root cause."""
        classification = self._classify(log_text)
        suggestions = self.FIX_SUGGESTIONS.get(classification, {})
        jira_id = self._extract_jira_id(log_text)

        result = {
            "timestamp": datetime.now().isoformat(),
            "jira_id": jira_id or "FC-001",
            "classification": self.PATTERNS[classification]["description"],
            "icon": self.PATTERNS[classification]["icon"],
            "root_cause": suggestions.get("root_cause", "Unknown"),
            "code_fix": suggestions.get("code_fix", []),
            "app_fix": suggestions.get("app_fix", "No application-level fix required."),
            "matched_patterns": self._get_matched_patterns(log_text, classification),
            "log_snippet": log_text[:500],
        }
        self.results.append(result)
        return result

    def _classify(self, log_text):
        """FC-001: Classify the failure by matching patterns."""
        scores = {}
        for category, config in self.PATTERNS.items():
            score = 0
            for pattern in config["patterns"]:
                matches = re.findall(pattern, log_text, re.IGNORECASE)
                score += len(matches)
            scores[category] = score

        if max(scores.values()) == 0:
            return "business_logic_defect"  # Default classification

        return max(scores, key=scores.get)

    def _get_matched_patterns(self, log_text, classification):
        """FC-001: Return the specific patterns that matched."""
        matched = []
        for pattern in self.PATTERNS[classification]["patterns"]:
            if re.search(pattern, log_text, re.IGNORECASE):
                matched.append(pattern)
        return matched

    def _extract_jira_id(self, log_text):
        """FC-001: Extract Jira ID from log text."""
        match = re.search(r"FC-\d+", log_text)
        return match.group(0) if match else None

    def generate_report(self, output_path="reports/failure_analysis.json"):
        """FC-001: Generate a JSON report of all analyzed failures."""
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_failures_analyzed": len(self.results),
            "classification_summary": self._get_summary(),
            "details": self.results,
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        return report

    def _get_summary(self):
        """FC-001: Summarize classifications."""
        summary = {}
        for result in self.results:
            cls = result["classification"]
            summary[cls] = summary.get(cls, 0) + 1
        return summary

    def print_analysis(self, result):
        """FC-001: Pretty-print a single analysis result."""
        print(f"\n{'='*60}")
        print(f"{result['icon']}  FAILURE ANALYSIS – {result['jira_id']}")
        print(f"{'='*60}")
        print(f"Classification: {result['classification']}")
        print(f"\n📋 Root Cause:")
        print(f"   {result['root_cause']}")
        print(f"\n🔧 Code-Level Fix:")
        for fix in result['code_fix']:
            print(f"   {fix}")
        print(f"\n🏗️  Application-Level Fix:")
        print(f"   {result['app_fix']}")
        print(f"\n🔍 Matched Patterns: {result['matched_patterns']}")
        print(f"{'='*60}\n")


# ---- CLI Entry Point ----
if __name__ == "__main__":
    analyzer = AIFailureAnalyzer()

    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        try:
            with open(log_file, "r") as f:
                log_content = f.read()
            result = analyzer.analyze(log_content)
            analyzer.print_analysis(result)
            analyzer.generate_report()
            print(f"✅ Report saved to reports/failure_analysis.json")
        except FileNotFoundError:
            print(f"❌ File not found: {log_file}")
            sys.exit(1)
    else:
        # Interactive mode: read from stdin
        print("FC-001 AI Failure Analyzer")
        print("Paste failure logs below (Ctrl+D / Ctrl+Z to submit):")
        print("-" * 40)
        try:
            log_content = sys.stdin.read()
            if log_content.strip():
                result = analyzer.analyze(log_content)
                analyzer.print_analysis(result)
            else:
                print("No input provided.")
        except EOFError:
            pass
