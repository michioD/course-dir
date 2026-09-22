import os
import json
import asyncio
import urllib.request
import urllib.error
from typing import List, Dict

# Configured to use the llama3.2 model you just pulled
OLLAMA_MODEL = "llama3.1"

# Complete TCSCM course catalog from syllabus
COURSES: List[Dict[str, str]] = [
    # General / Mandatory Courses
    {"code": "DA2210", "title": "Introduction to Philosophy of Science and Research Methodology", "credits": "6.0"},
    {"code": "DD2300", "title": "Program Integrating Course in Computer Science", "credits": "2.0"},
    {"code": "DD2380", "title": "Artificial Intelligence", "credits": "6.0"},
    {"code": "DD2395", "title": "Computer Security", "credits": "6.0"},
    {"code": "DD2440", "title": "Advanced Algorithms", "credits": "6.0"},
    {"code": "IK2218", "title": "Protocols and Principles of the Internet", "credits": "6.0"},
    {"code": "DA231X", "title": "Degree Project in Computer Science and Engineering", "credits": "30.0"},

    # Track: Data Science (CSDA)
    {"code": "DD2421", "title": "Machine Learning", "credits": "7.5"},
    {"code": "DD2417", "title": "Language Engineering", "credits": "7.5"},
    {"code": "DD2420", "title": "Probabilistic Graphical Models", "credits": "7.5"},
    {"code": "DD2424", "title": "Deep Learning in Data Science", "credits": "7.5"},
    {"code": "DD2477", "title": "Search Engines and Information Retrieval Systems", "credits": "7.5"},
    {"code": "DH2322", "title": "Interactive Data Visualization", "credits": "7.5"},
    {"code": "DD2438", "title": "Artificial Intelligence and Multi Agent Systems", "credits": "15.0"},
    {"code": "DT2112", "title": "Speech Technology", "credits": "7.5"},
    {"code": "DT2119", "title": "Speech and Speaker Recognition", "credits": "7.5"},
    {"code": "DD2430", "title": "Project Course in Data Science", "credits": "7.5"},
    {"code": "DD2434", "title": "Machine Learning, Advanced Course", "credits": "7.5"},
    {"code": "DD2437", "title": "Artificial Neural Networks and Deep Architectures", "credits": "7.5"},
    {"code": "DD2447", "title": "Statistical Methods in Applied Computer Science", "credits": "6.0"},
    {"code": "EL2320", "title": "Applied Estimation", "credits": "7.5"},
    {"code": "SF2940", "title": "Probability Theory", "credits": "7.5"},
    {"code": "DD2257", "title": "Visualization", "credits": "7.5"},
    {"code": "DD2368", "title": "Quantum Neural Networks", "credits": "7.5"},
    {"code": "DD2413", "title": "Social Robotics", "credits": "7.5"},
    {"code": "DD2423", "title": "Image Analysis and Computer Vision", "credits": "7.5"},
    {"code": "DD2610", "title": "Deep Learning, advanced course", "credits": "7.5"},
    {"code": "ID2222", "title": "Data Mining", "credits": "7.5"},
    {"code": "ID2223", "title": "Scalable Machine Learning and Deep Learning", "credits": "7.5"},
    {"code": "SF1811", "title": "Optimization", "credits": "6.0"},
    {"code": "DD2361", "title": "Advanced Topics in Deep Learning in Biomedical Image Analysis", "credits": "7.5"},

    # Track: Interaction Design (CSID)
    {"code": "DH2628", "title": "Interaction Design Methods", "credits": "7.5"},
    {"code": "DH2400", "title": "Physical Interaction Design and Realization", "credits": "7.5"},
    {"code": "DH2632", "title": "Human-Computer Interaction. Research Seminars", "credits": "3.0"},
    {"code": "DH2670", "title": "Haptics. Tactile and Tangible Interaction", "credits": "7.5"},
    {"code": "DM2731", "title": "AI for Learning", "credits": "7.5"},
    {"code": "DH2310", "title": "Extended Reality in Theory and Practice", "credits": "7.5"},
    {"code": "DM2588", "title": "Generative AI for Media Technology and Interaction Design", "credits": "7.5"},
    {"code": "DM2630", "title": "User Experience Design and Evaluation", "credits": "9.0"},
    {"code": "DH2408", "title": "Evaluation Methods in Human-Computer Interaction", "credits": "6.0"},
    {"code": "DM2730", "title": "Technology Enhanced Learning", "credits": "7.5"},
    {"code": "DT2140", "title": "Multimodal Interaction and Interfaces", "credits": "7.5"},

    # Track: Cognitive Systems (CSCS)
    {"code": "DD2410", "title": "Introduction to Robotics", "credits": "7.5"},
    {"code": "DT2151", "title": "Project in Conversational Systems", "credits": "7.5"},
    {"code": "DD2419", "title": "Project Course in Robotics and Autonomous Systems", "credits": "9.0"},

    # Track: Software Technology (CSST)
    {"code": "DD2480", "title": "Software Engineering Fundamentals", "credits": "7.5"},
    {"code": "DD2528", "title": "Dependable Autonomous Systems", "credits": "7.5"},
    {"code": "DD2585", "title": "Programmable Society with Blockchains and Smart Contracts", "credits": "7.5"},
    {"code": "DD2459", "title": "Software Reliability", "credits": "7.5"},
    {"code": "DD2481", "title": "Principles of Programming Languages", "credits": "7.5"},
    {"code": "DD2525", "title": "Language-Based Security", "credits": "7.5"},
    {"code": "DD2557", "title": "Program Semantics and Analysis", "credits": "7.5"},
    {"code": "DD2460", "title": "Software Safety and Security", "credits": "7.5"},
    {"code": "ID1217", "title": "Concurrent Programming", "credits": "7.5"},
    {"code": "DD2443", "title": "Parallel and Distributed Computing", "credits": "7.5"},
    {"code": "DD2482", "title": "Automated Software Testing and DevOps", "credits": "7.5"},
    {"code": "DD2489", "title": "Scalable software Development with Functional Programming", "credits": "7.5"},
    {"code": "ID2202", "title": "Compilers and Execution Environments", "credits": "7.5"},
    {"code": "DD2529", "title": "Project Course on Operating Systems and Compiler Support for Security", "credits": "7.5"},
    {"code": "DD2458", "title": "Problem Solving and Programming under Pressure", "credits": "9.0"},
    {"code": "IK2215", "title": "Advanced Internetworking", "credits": "7.5"},
    {"code": "IK2221", "title": "Networked Systems for Machine Learning", "credits": "7.5"},
    {"code": "IK2227", "title": "Network Systems with Edge or Cloud Datacenters", "credits": "7.5"},

    # Track: Theoretical Computer Science (CSTC)
    {"code": "SF2956", "title": "Topological Data Analysis", "credits": "7.5"},
    {"code": "DD2542", "title": "Seminars on Theoretical Computer Science, Algorithms and Complexity", "credits": "7.5"},
    {"code": "DD2452", "title": "Formal Methods", "credits": "7.5"},
    {"code": "SF2741", "title": "Enumerative Combinatorics", "credits": "7.5"},
    {"code": "DD2448", "title": "Foundations of Cryptography", "credits": "7.5"},
    {"code": "SF2930", "title": "Regression Analysis", "credits": "7.5"},
    {"code": "SF2972", "title": "Game Theory", "credits": "7.5"},
    {"code": "DD2467", "title": "Individual Project in Theoretical Computer Science", "credits": "7.5"},
    {"code": "DD2445", "title": "Complexity Theory", "credits": "7.5"},
    {"code": "DD2552", "title": "Seminars on Theoretical Computer Science, Programming Languages and Formal Methods", "credits": "7.5"},
    {"code": "DD2366", "title": "Open Quantum Systems", "credits": "7.5"},
    {"code": "DD2367", "title": "Quantum Computing for Computer Scientists", "credits": "7.5"},

    # Track: Visualization and Interactive Graphics (CSVG)
    {"code": "DD2258", "title": "Introduction to Visualization. Computer Graphics and Image/Video Processing", "credits": "7.5"},
    {"code": "DH2323", "title": "Computer Graphics and Interaction", "credits": "6.0"},
    {"code": "DH2650", "title": "Computer Game Design", "credits": "6.0"},
    {"code": "DD2356", "title": "Methods in High Performance Computing", "credits": "7.5"},
    {"code": "DD2470", "title": "Advanced Topics in Visualization and Computer Graphics", "credits": "6.0"},
    {"code": "DH2413", "title": "Advanced Graphics and Interaction", "credits": "9.0"},
    {"code": "DM2350", "title": "Human Perception for Information Technology", "credits": "7.5"},

    # Track: Parallel Computation (CSPC)
    {"code": "DD2370", "title": "Computational Methods for Electromagnetics", "credits": "7.5"},
    {"code": "DD2358", "title": "Introduction to High Performance Computing", "credits": "7.5"},
    {"code": "DD2363", "title": "Methods in Scientific Computing", "credits": "7.5"},
    {"code": "DD2365", "title": "Advanced Computation in Fluid Mechanics", "credits": "7.5"},
    {"code": "DD2360", "title": "Applied GPU Programming", "credits": "7.5"},
    {"code": "DD2375", "title": "Project Course in High-Performance Computing", "credits": "7.5"},
    {"code": "DD2444", "title": "Project Course in Scientific Computing", "credits": "7.5"},
    {"code": "ID2203", "title": "Distributed Systems. Advanced Course", "credits": "7.5"},
    {"code": "CM2014", "title": "Simulation Methods in Medical Engineering", "credits": "7.5"},
    {"code": "DT2212", "title": "Music Acoustics", "credits": "7.5"},
    {"code": "BB2280", "title": "Molecular Modeling", "credits": "7.5"},
    {"code": "DD2402", "title": "Advanced Individual Course in Computational Biology", "credits": "6.0"},
    {"code": "DD2435", "title": "Mathematical Modelling of Biological Systems", "credits": "9.0"},
    {"code": "EL2820", "title": "Modelling of Dynamical Systems", "credits": "7.5"},
    {"code": "SF2565", "title": "Program Construction in C++ for Scientific Computing", "credits": "7.5"},
]

PROMPT_TEMPLATE = """\
Evaluate the course {code}: {title} ({credits} ECTS) strictly according to these 3 criteria:

1. "Autodidact" Threshold (Pass/Fail):
   - PASS if it has high theoretical density (pen-and-paper proofs, complex mathematical rigor, non-trivial concepts hard to self-teach).
   - FAIL if it is tool-, API-, or documentation-heavy (material easily learned via official docs, GitHub, or online tutorials).

2. Essential Knowledge in Industry (High/Moderate/Low):
   - Value for high-skill ceiling engineering/research roles (e.g., Compiler/Kernel, Quantitative Research, Bioinformatics, Edge AI, Robotics).

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

CONCURRENCY_LIMITER = asyncio.Semaphore(2)

def call_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    data = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result.get("response", "")

async def evaluate_course(course: Dict[str, str]):
    async with CONCURRENCY_LIMITER:
        code = course["code"]
        out_path = f"evaluations/{code}_evaluation.md"

        if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
            print(f"[=] Skipping {code} (Cached)")
            return

        prompt = PROMPT_TEMPLATE.format(
            code=code,
            title=course["title"],
            credits=course["credits"]
        )

        print(f"[*] Processing evaluation for {code} locally via Ollama ({OLLAMA_MODEL})...")

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, call_ollama, prompt)

            os.makedirs("evaluations", exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("# Evaluation for {code}: {title} ({credits} ECTS)\n\n".format(
                    code=code,
                    title=course["title"],
                    credits=course["credits"]
                ))
                f.write(result)
            print(f"[+] Successfully generated evaluation for {code} -> {out_path}")
        except Exception as e:
            print(f"[!] Error processing {code}: {e}")

async def main():
    os.makedirs("evaluations", exist_ok=True)
    print(f"Starting evaluations for {len(COURSES)} courses via local Ollama ({OLLAMA_MODEL})...")
    tasks = [evaluate_course(course) for course in COURSES]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
