# ============================================================================
# FC-001 | Fashion Cube QA Automation - LangChain Self-Healing Engine
# Requirement: Use LLM to analyze failures and generate real code fixes
# Supports: OpenAI (GPT-4) and Google Gemini
# ============================================================================

import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class LangChainHealer:
    """FC-001: LLM-powered self-healing engine for test scripts.

    Uses LangChain + an LLM to:
        1. Read the failure traceback
        2. Read the source code around the failure
        3. Reason about the root cause
        4. Generate a concrete code patch
        5. Apply the patch to the file

    Supported providers: openai, google (set via LLM_PROVIDER env var)
    """

    # Context window: how many lines above/below the failure to send to the LLM
    CONTEXT_LINES = 15

    SYSTEM_PROMPT = """\
You are an expert QA automation engineer specializing in Python, Playwright, and Pytest.
You are analyzing a test failure and must produce a FIXED version of the code.

Rules:
1. Only fix the code that is broken. Do NOT rewrite unrelated code.
2. For Timing issues: add explicit waits (page.wait_for_selector, wait_for_load_state, wait_for_timeout).
3. For Locator issues: suggest a more robust selector (prefer data-testid > id > CSS class > XPath).
4. For Assertion issues: add debug logging or fix expected values if the requirement changed.
5. For API issues: add retry logic with backoff.
6. For Data issues: add null/existence checks before accessing data.
7. Preserve all existing comments and docstrings.
8. Mark every line you change with a trailing comment: # [AI-HEAL]

You MUST respond with ONLY a valid JSON object in this exact format:
{
    "classification": "Timing Issue | Locator Issue | Business Logic Defect | API Defect | Data Problem | Performance Bottleneck",
    "root_cause": "One sentence explaining why it failed",
    "fixed_code": "The complete fixed version of the code snippet provided",
    "explanation": "Brief explanation of what you changed and why"
}

Do NOT include any text outside the JSON object. No markdown fences, no commentary.
"""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "google").lower()
        self.llm = self._init_llm()
        self.heal_log = []

    def _init_llm(self):
        """FC-001: Initialize the LLM based on provider config."""
        try:
            if self.provider == "openai":
                from langchain_openai import ChatOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    print("[LangChain Healer] WARNING: OPENAI_API_KEY not set.")
                    return None
                return ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0,
                    api_key=api_key,
                )

            elif self.provider == "google":
                from langchain_google_genai import ChatGoogleGenerativeAI
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    print("[LangChain Healer] WARNING: GOOGLE_API_KEY not set.")
                    return None
                return ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0,
                    google_api_key=api_key,
                )

            else:
                print(f"[LangChain Healer] Unknown provider: {self.provider}")
                return None

        except ImportError as e:
            print(f"[LangChain Healer] Missing dependency: {e}")
            print("[LangChain Healer] Run: pip install langchain-openai langchain-google-genai")
            return None

    def heal(self, log_text):
        """FC-001: Main entry point — analyze failure and fix the code.

        Returns:
            dict with keys: status, classification, root_cause, explanation, file_path, message
        """
        if not self.llm:
            return {
                "status": "skipped",
                "message": "LLM not initialized. Set LLM_PROVIDER and API key env vars.",
            }

        # Step 1: Extract the failure location
        location = self._extract_location(log_text)
        if not location:
            return {
                "status": "error",
                "message": "Could not extract file path and line number from traceback.",
            }

        file_path, line_num = location

        # Step 2: Read the source code around the failure
        source_context, start_line = self._read_source_context(file_path, line_num)
        if not source_context:
            return {
                "status": "error",
                "message": f"Could not read source file: {file_path}",
            }

        # Step 3: Build the prompt and call the LLM
        user_prompt = self._build_prompt(log_text, source_context, file_path, line_num)

        print(f"\n🤖 [LangChain Healer] Sending failure to {self.provider} LLM...")
        print(f"   📄 File: {file_path}:{line_num}")

        try:
            from langchain_core.messages import SystemMessage, HumanMessage

            messages = [
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=user_prompt),
            ]
            response = self.llm.invoke(messages)
            raw_response = response.content.strip()

            # Step 4: Parse the LLM response
            fix_data = self._parse_response(raw_response)
            if not fix_data:
                return {
                    "status": "error",
                    "message": "LLM response could not be parsed as JSON.",
                    "raw_response": raw_response[:500],
                }

            # Step 5: Apply the fix
            apply_result = self._apply_fix(file_path, start_line, source_context, fix_data["fixed_code"])

            result = {
                "status": "fixed" if apply_result else "error",
                "classification": fix_data.get("classification", "Unknown"),
                "root_cause": fix_data.get("root_cause", ""),
                "explanation": fix_data.get("explanation", ""),
                "file_path": file_path,
                "line_num": line_num,
                "message": f"Applied LLM fix to {file_path}" if apply_result else "Failed to apply fix.",
                "timestamp": datetime.now().isoformat(),
            }

            self.heal_log.append(result)
            self._print_result(result)
            return result

        except Exception as e:
            return {"status": "error", "message": f"LLM call failed: {str(e)}"}

    def _extract_location(self, log_text):
        """FC-001: Extract file path and line number from Python traceback."""
        pattern = r'File "(.*?)", line (\d+)'
        matches = re.findall(pattern, log_text)

        if not matches:
            return None

        # Prefer project files over library code
        for path, line in reversed(matches):
            if "qa-automation" in path or "tests" in path or "pages" in path:
                return path, int(line)

        return matches[-1][0], int(matches[-1][1])

    def _read_source_context(self, file_path, line_num):
        """FC-001: Read source code around the failure point."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            start = max(0, line_num - self.CONTEXT_LINES - 1)
            end = min(len(lines), line_num + self.CONTEXT_LINES)

            # Add line numbers for LLM context
            numbered_lines = []
            for i in range(start, end):
                marker = " >>> FAILURE" if i == line_num - 1 else ""
                numbered_lines.append(f"{i + 1:>4}: {lines[i].rstrip()}{marker}")

            return "\n".join(numbered_lines), start

        except Exception:
            return None, 0

    def _build_prompt(self, log_text, source_context, file_path, line_num):
        """FC-001: Build the user prompt for the LLM."""
        return f"""\
## Test Failure Log
```
{log_text[:2000]}
```

## Source Code (from {file_path}, failure at line {line_num})
```python
{source_context}
```

Analyze the failure and provide the fixed code. Remember to respond with ONLY a JSON object.
"""

    def _parse_response(self, raw_response):
        """FC-001: Parse the LLM JSON response."""
        try:
            # Try direct JSON parse
            return json.loads(raw_response)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code fences
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Try finding raw JSON object
        json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    def _apply_fix(self, file_path, start_line, original_context, fixed_code):
        """FC-001: Apply the LLM-generated fix to the source file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Strip line numbers from the fixed code (LLM might include them)
            clean_lines = []
            for line in fixed_code.split("\n"):
                # Remove line number prefix like "  42: "
                cleaned = re.sub(r"^\s*\d+:\s?", "", line)
                clean_lines.append(cleaned + "\n")

            # Remove the marker comments the LLM might echo back
            clean_lines = [line.replace(" >>> FAILURE", "") for line in clean_lines]

            # Calculate the range to replace
            orig_lines = original_context.split("\n")
            end_line = start_line + len(orig_lines)

            # Replace the lines
            lines[start_line:end_line] = clean_lines

            # Write back
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return True

        except Exception as e:
            print(f"[LangChain Healer] ERROR applying fix: {e}")
            return False

    def _print_result(self, result):
        """FC-001: Pretty-print the healing result."""
        print(f"\n{'='*60}")
        print(f"🤖  LANGCHAIN SELF-HEAL RESULT")
        print(f"{'='*60}")
        print(f"Status:         {result['status']}")
        print(f"Classification: {result.get('classification', 'N/A')}")
        print(f"Root Cause:     {result.get('root_cause', 'N/A')}")
        print(f"Explanation:    {result.get('explanation', 'N/A')}")
        print(f"File:           {result.get('file_path', 'N/A')}:{result.get('line_num', 'N/A')}")
        print(f"{'='*60}\n")

    def generate_report(self, output_path="reports/langchain_heal_report.json"):
        """FC-001: Generate a JSON report of all healing actions."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "provider": self.provider,
            "total_healed": len(self.heal_log),
            "results": self.heal_log,
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"📊 Healing report saved to {output_path}")
        return report


# ---- CLI Entry Point ----
if __name__ == "__main__":
    import sys

    healer = LangChainHealer()

    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        try:
            with open(log_file, "r") as f:
                log_content = f.read()
            result = healer.heal(log_content)
            healer.generate_report()
        except FileNotFoundError:
            print(f"File not found: {log_file}")
            sys.exit(1)
    else:
        print("FC-001 LangChain Self-Healing Engine")
        print(f"Provider: {healer.provider}")
        print("Usage: python langchain_healer.py <failure_log_file>")
