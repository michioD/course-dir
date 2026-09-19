import os
import asyncio
from typing import List, Dict

COURSES: List[Dict[str, str]] = [
    # General / Mandatory Courses
    {"code": "AK2030", "title": "Theory and Methodology of Science", "credits": "4.5"},
    {"code": "SA2001", "title": "Sustainable Development & Research Methodology", "credits": "3.0"},
    {"code": "SF2940", "title": "Probability Theory", "credits": "7.5"},
    # General Conditionally Elective
    {"code": "SF2812", "title": "Applied Linear Optimization", "credits": "7.5"},
    {"code": "SF2524", "title": "Matrix Computations for Large-scale Systems", "credits": "7.5"},
    {"code": "SF2527", "title": "Numerical Methods for Differential Equations I", "credits": "7.5"},
    {"code": "SF2832", "title": "Mathematical Systems Theory", "credits": "7.5"},
    {"code": "SF2863", "title": "Systems Engineering", "credits": "7.5"},
    # Advanced & Track Electives
    {"code": "DD2356", "title": "Methods in High Performance Computing", "credits": "7.5"},
    {"code": "DD2365", "title": "Advanced Computation in Fluid Mechanics", "credits": "7.5"},
    {"code": "DD2421", "title": "Machine Learning", "credits": "7.5"},
    {"code": "SF2526", "title": "Numerical Algorithms for Data-Intensive Science", "credits": "7.5"},
    {"code": "SF2701", "title": "Financial Mathematics, Basic Course", "credits": "7.5"},
    {"code": "SF2822", "title": "Applied Nonlinear Optimization", "credits": "7.5"},
    {"code": "SF2842", "title": "Geometric Control Theory", "credits": "7.5"},
    {"code": "SF2930", "title": "Regression Analysis", "credits": "7.5"},
    {"code": "SF2943", "title": "Time Series Analysis", "credits": "7.5"},
    {"code": "SF2955", "title": "Computer Intensive Methods in Mathematical Statistics", "credits": "7.5"},
    {"code": "SF2971", "title": "Martingales and Stochastic Integrals", "credits": "7.5"},
    {"code": "SG2212", "title": "Computational Fluid Dynamics", "credits": "7.5"},
    {"code": "DD2601", "title": "Deep Generative Models and Synthesis", "credits": "7.5"},
    {"code": "DD2257", "title": "Visualization", "credits": "7.5"},
    {"code": "DD2434", "title": "Machine Learning, Advanced Course", "credits": "7.5"},
    {"code": "DD2435", "title": "Mathematical Modelling of Biological Systems", "credits": "9.0"},
    {"code": "DD2440", "title": "Advanced Algorithms", "credits": "6.0"},
    {"code": "SF2852", "title": "Optimal Control Theory", "credits": "7.5"},
    {"code": "SF2935", "title": "Modern Methods of Statistical Learning", "credits": "7.5"},
    {"code": "SF2942", "title": "Portfolio Theory and Risk Management", "credits": "7.5"},
    {"code": "SF2956", "title": "Topological Data Analysis", "credits": "7.5"},
    {"code": "SF2975", "title": "Financial Derivatives", "credits": "7.5"},
    {"code": "SF2980", "title": "Risk Management", "credits": "7.5"},
    {"code": "DD2352", "title": "Algorithms and Complexity", "credits": "7.5"},
    {"code": "DD2445", "title": "Complexity Theory", "credits": "7.5"},
    {"code": "SF2565", "title": "Program Construction in C++ for Scientific Computing", "credits": "7.5"},
    {"code": "SF2525", "title": "Computational Methods for SDEs and Machine Learning", "credits": "7.5"},
    {"code": "SF2528", "title": "Numerical Methods for Differential Equations II", "credits": "7.5"},
    {"code": "SF2529", "title": "Inverse Problems", "credits": "7.5"},
    {"code": "SF2957", "title": "Statistical Machine Learning", "credits": "7.5"},
    {"code": "BB2280", "title": "Molecular Modeling", "credits": "7.5"},
    {"code": "CB2442", "title": "Bioinformatics", "credits": "7.5"},
    {"code": "SK2532", "title": "Biomedicine for Engineers", "credits": "7.5"},
]

PROMPT_TEMPLATE = """\
Evaluate the course {code}: {title} ({credits} ECTS) strictly according to these 3 criteria:

1. "Autodidact" Threshold (Pass/Fail):
   - PASS if it has high theoretical density (pen-and-paper proofs, complex mathematical rigor, non-trivial concepts hard to self-teach).
   - FAIL if it is tool-, API-, or documentation-heavy (material easily learned via official docs, GitHub, or online tutorials).

2. Transferability (High/Moderate/Low):
    - How easily can the knowledge from this course be applied to other domains or problems?
    - Low if it is highly domain-specific and not applicable outside of its immediate context.
    - Moderate if it has applicability within a few related domains and even other industries
    - High if it can applied to a wide range of domains and industries 
3. Prerequisite Knowledge (High/Low):
   - Is it essential foundational material early on (a "map" or "moat") required before accessing higher-level domain problems?
   - High if it the skill cieling is high and that taking this course is doesn't cover 80 precent of what you need to know
   - High if its a relevant field that is in very high active development and has a lot of depth.

4. Frequently used on the job (High/Moderate/Low):
    - How often are engineers/researchers actually use this knowledge in real-world scenarios?
    - High if it is a core skill used daily. Like if you haven't taken this course, you're incapable of doing the job.
    - Moderate if it is used occasionally
    - Low if it is rarely used on the job and is mainly just nice theory to know for intuition and context but not essential for day-to-day work.

Provide a concise, direct structured breakdown and a final 1-sentence Strategic Takeaway.
"""

async def evaluate_course(course: Dict[str, str], limiter: asyncio.Semaphore):
    async with limiter:
        code = course["code"]
        out_path = f"evaluations/{code}_evaluation.md"
        prompt = PROMPT_TEMPLATE.format(
            code=code,
            title=course["title"],
            credits=course["credits"]
        )

        print(f"[*] Spawning Antigravity Agent for {code}...")

        # Run agy using -p to print output directly to stdout
        proc = await asyncio.create_subprocess_exec(
            "agy", "-p", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            os.makedirs("evaluations", exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("# Evaluation for {code}: {title} ({credits} ECTS)\n\n".format(
                    code=code,
                    title=course["title"],
                    credits=course["credits"]
                ))
                f.write(stdout.decode("utf-8"))
            print(f"[+] Successfully generated evaluation for {code} -> {out_path}")
        else:
            print(f"[!] Error processing {code}: {stderr.decode('utf-8')}")

async def main():
    os.makedirs("evaluations", exist_ok=True)
    limiter = asyncio.Semaphore(4)
    print(f"Starting evaluations for {len(COURSES)} courses from TTMAM syllabus...")
    tasks = [evaluate_course(course, limiter) for course in COURSES]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
