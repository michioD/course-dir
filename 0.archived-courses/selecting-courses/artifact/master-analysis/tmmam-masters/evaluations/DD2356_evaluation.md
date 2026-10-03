# Evaluation for DD2356: Methods in High Performance Computing (7.5 ECTS)

### Evaluation: DD2356: Methods in High Performance Computing (7.5 ECTS)

#### 1. "Autodidact" Threshold
- **Rating:** **FAIL**
- **Rationale:** The course centers on standard parallel programming interfaces (MPI, OpenMP), profiling tools, and practical hardware optimization in C/C++. It lacks dense pen-and-paper proofs or heavy mathematical theory; the core concepts (shared-memory concurrency, distributed message passing, cache optimization, Roofline model) are standard software engineering/systems topics well-documented across official APIs, vendor guides, and tutorials.

---

#### 2. Transferability
- **Rating:** **High**
- **Rationale:** The principles of parallel memory hierarchies, data locality, communication-to-computation trade-offs, and concurrency primitives transfer widely across distributed systems, machine learning infrastructure (distributed training/inference), quantitative finance, backend performance engineering, and game engine architecture.

---

#### 3. Prerequisite Knowledge / Depth
- **Rating:** **High**
- **Rationale:** While this course provides foundational frameworks for parallel computing, it only introduces the basics of scaling and parallel execution. HPC and modern systems engineering have an exceptionally high skill ceiling (GPU kernels, hardware-specific micro-optimizations, non-blocking asynchronous algorithms, custom communication topologies) that requires substantial depth beyond the introductory 7.5 ECTS scope.

---

#### 4. Frequently Used on the Job
- **Rating:** **Moderate** (Low for general software engineering, High for HPC/ML systems)
- **Rationale:** Most general software engineering roles abstract these low-level parallel primitives away via high-level frameworks; however, for engineers working specifically in ML infrastructure, scientific simulation, or latency-critical systems, distributed memory patterns and low-level performance profiling are routine.

---

### Strategic Takeaway
DD2356 provides highly transferable foundational intuition for low-level systems and distributed performance, but its standard API- and tool-driven syllabus makes it straightforward to learn independently rather than requiring formal academic enrollment.
