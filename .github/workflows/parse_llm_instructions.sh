#!/bin/bash

# Parse the "Prompt for AI Agents" section from a comment
# Extracts content between triple backticks after "Prompt for AI Agents"
# Usage: echo "$SUGGESTION" | ./parse_llm_instructions.sh

parse_llm_instructions() {
    local content
    content=$(cat)
    
    # Find the "Prompt for AI Agents" section and extract content between triple backticks
    # Using awk to handle multi-line content between ``` markers
    echo "$content" | awk '
        /<summary>🤖 Prompt for AI Agents<\/summary>/ { found=1; next }
        found && /```/ { 
            if (in_code_block) {
                # End of code block - print collected content
                printf "%s", code_content
                exit
            } else {
                # Start of code block
                in_code_block=1
                code_content=""
            }
            next
        }
        in_code_block { code_content = code_content $0 "\n" }
    '
}

parse_llm_instructions
