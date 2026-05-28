#!/bin/bash

# Parse the "Prompt for AI Agents" section from a comment
# Extracts content between triple backticks after "Prompt for AI Agents"
# Usage: parse_llm_instructions "$SUGGESTION"

echo "$SUGGESTION"
echo "this is a test"

echo "$SUGGESTION" | awk '
    /<summary>🤖 Prompt for AI Agents<\/summary>/ { found=1; next }
    found && /```/ { 
        if (in_code_block) {
            printf "%s", code_content
            exit
        } else {
            in_code_block=1
            code_content=""
        }
        next
    }
    in_code_block { code_content = code_content $0 "\n" }
'