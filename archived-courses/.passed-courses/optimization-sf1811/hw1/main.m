clear;
[A, b, c, beta] = hw1data(021012);
[m, n] = size(A);

% --- Initialization ---
ny = 1:n;
ny(beta) = [];        
fuzz = sqrt(eps);     
max_iter = 100;       
iter = 0;

fprintf('Starting Simplex Method...\n');

while iter < max_iter
    iter = iter + 1;
    
    % 1. Extract matrices
    Abeta = A(:, beta);
    Any = A(:, ny);
    cbeta = c(beta);
    cny = c(ny);
    
    % 2. Calculate BFS
    % We solve the system for the basic variables; non-basics are 0.
    bbar = Abeta \ b;
    x_curr = zeros(n, 1);
    x_curr(beta) = bbar;
    
    % 3. Calculate Simplex Multipliers (y) and Reduced Costs (r_ny)
    y = (Abeta') \ cbeta;
    rny = cny - Any' * y;
    
    % --- PRINT ITERATION DATA ---
    fprintf('\n================ ITERATION %d ================\n', iter);
    fprintf('Current BFS (x):\n');
    disp(x_curr'); % Transposed for a compact row view
    fprintf('Reduced Costs (r_nu):\n');
    disp(rny');   % Transposed for a compact row view
    
    % 4. Optimality Check
    [rnymin, q_idx] = min(rny);
    
    if rnymin >= -fuzz
        fprintf('>>> Optimal solution found at iteration %d!\n', iter);
        break;
    end
    
    % 5. Determine Entering and Leaving Variables
    entering_var = ny(q_idx);
    abar = Abeta \ A(:, entering_var);
    
    t_ratio = bbar ./ abar;
    t_ratio(abar <= fuzz) = inf; 
    
    [t_max, i_idx] = min(t_ratio);
    
    if t_max == inf
        error('The problem is unbounded.');
    end
    
    leaving_var = beta(i_idx);
    fprintf('Entering: x%d | Leaving: x%d | Step: %.4f\n', entering_var, leaving_var, t_max);
    
    % 6. Update indices
    beta(i_idx) = entering_var;
    ny(q_idx) = leaving_var;
end

fprintf('\nFinal optimal x:\n');
disp(x_curr);