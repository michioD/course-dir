1. ## Move the clusters around and change their sizes. Pay attention to when the optimizer is not able to find a solution.
If the clusters overlap significantly and the Linear Kernel is used with a very high C value (Hard Margin), the optimizer will fail to find a solution.

    Reasoning: In a hard margin SVM, the primal constraints ti​(wT⋅xi​−b)≥1 must be satisfied for all data points. If the data is not linearly separable (i.e., blue and red dots mix), these mathematical constraints are impossible to satisfy simultaneously, and the optimization problem becomes infeasible.

    Observation: The ret['success'] flag in Python will return False.
![alt text](<Screenshot 2026-02-16 at 18.40.47.png>)
![alt text](<Screenshot 2026-02-16 at 18.43.30.png>)
![alt text](<Screenshot 2026-02-16 at 18.44.37.png>)
2. Implement the two non-linear kernels. You should be able to classify very hard data sets with these.
(The code above implements kernel_polynomial and kernel_radial.)

    Observation: By mapping inputs to a higher-dimensional space using ϕ(x), data that is mixed in 2D becomes separable.

        Polynomial: Useful for curved, arc-like boundaries.

        RBF (Radial): Capable of creating "islands" or closed loops around clusters of data points.

3. Explore the parameters of non-linear kernels (e.g., p and σ). Reason in terms of bias-variance trade-off.

    Polynomial (p): Increasing the degree p increases the model complexity.

        Low p (High Bias): The boundary is too simple (stiff) and may miss patterns.

        High p (High Variance): The boundary becomes very "wiggly" and specific to the training data, risking overfitting.

    RBF (σ): The parameter σ controls the width of the Gaussian.

        Large σ (High Bias): The kernel function is very wide/smooth. The decision boundary becomes nearly linear and ignores local details.

        Small σ (High Variance): The kernel is very narrow/sharp. The decision boundary wraps tightly around individual data points, leading to "islands" and overfitting.

4. Explore the role of the slack parameter C. What happens for very large/small values?
The parameter C controls the penalty for misclassification (slack).

    Very Large C (Hard Margin behavior): The model heavily penalizes any non-zero slack variables (ξ). It tries desperately to classify every single training point correctly. This results in a narrow margin and a jagged boundary determined by outlier points.

    Very Small C (Soft Margin behavior): The model tolerates misclassifications (larger ξ) to achieve a wider, more stable margin. It ignores outliers, resulting in a smoother boundary ("flatter" solution).

5. When should you opt for more slack (Low C) vs. a more complex model (Kernel)?

    Use More Slack (Low C): When the data is noisy. If the classes are generally separable but have random outliers (e.g., a blue dot deep in red territory due to measurement error), using a low C allows the SVM to ignore the noise and find the general trend.

    Use Complex Model (Kernel): When the data is non-linearly separable but clean. If the pattern is complex (e.g., one class surrounds another like a donut), simply adding slack to a linear model won't work. You need a kernel (like RBF) to transform the space so the geometry can be captured.