import asyncio
import os
import sys

PROMPT = """
You are an AI research assistant. Your task is to search online (using web search tools) to find out why students have chosen the TCSCM (Master's in Computer Science) program at KTH Royal Institute of Technology.

Please collect exactly 10 distinct opinions/reasons from real students. 
- You MUST provide real references (URLs to KTH student blogs, Reddit threads, university interviews, etc.) for each opinion.
- At least ONE of the opinions MUST be specifically about why a student chose the High-Performance Computing (HPC) track or courses within this master.

Format your response as a Markdown list where each entry includes:
- The opinion / reason for choosing TCSCM (or the HPC track).
- A brief quote or summary of the student's perspective.
- The reference link.
"""

async def main():
    print("[*] Spawning Antigravity Agent to search for TCSCM opinions...")
    print("[*] This may take a minute or two as the agent browses the web...\n")
    
    # Run agy using -p to print output directly to stdout
    proc = await asyncio.create_subprocess_exec(
        "agy", "-p", PROMPT,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await proc.communicate()
    
    if proc.returncode == 0:
        output_file = "tcscm_opinions.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(stdout.decode("utf-8"))
        print(f"[+] Successfully gathered 10 opinions.")
        print(f"[+] Results saved to {output_file}")
        print("\n--- Output Preview ---\n")
        # Print the first 1000 characters as a preview
        print(stdout.decode("utf-8")[:1000] + "...\n")
    else:
        print(f"[!] Error running agent. Return code: {proc.returncode}")
        print(f"[!] Stderr:\n{stderr.decode('utf-8')}")

if __name__ == "__main__":
    asyncio.run(main())
