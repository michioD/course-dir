clear;
[A, b, c, beta] = hw1data(021012);
[m, n] = size(A);

% Initialize Plot
figure(1); clf;
polyplot(A, b, [0; 10], [0; 10]);
xlabel('x_1')
ylabel('x_2')
hold on; % Keep the polyplot visible for scatter points

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
    
    % 2. Calculate BFS
    bbar = Abeta \ b;
    x_curr = zeros(n, 1);
    x_curr(beta) = bbar;
    
    % --- PLOT CURRENT BFS (x1, x2) ---
    scatter(x_curr(1), x_curr(2), 'filled');
    text(x_curr(1) + 0.2, x_curr(2) + 0.2, sprintf('(%.2f, %.2f)', x_curr(1), x_curr(2)), 'FontWeight', 'bold');
    
    % 3. Calculate Simplex Multipliers and Reduced Costs
    y = (Abeta') \ cbeta;
    rny = c(ny) - Any' * y;
    
    % --- PRINT ITERATION DATA ---
    fprintf('\n================ ITERATION %d ================\n', iter);
    fprintf('Current BFS (x):\n');
    disp(x_curr'); 
    fprintf('Reduced Costs (r_nu):\n');
    disp(rny');  
    fprintf('Dual Variables (y):\n');
    disp(y');
    % 4. Optimality Check
    [rnymin, q_idx] = min(rny);
    if iter == 1
        q_idx = 2; 
        rnymin = rny(q_idx); % Update rnymin to reflect x1
        fprintf('EX 1.4: Manually forcing q = %d (Entering: x%d)\n', q_idx, ny(q_idx));
    end
    if rnymin >= -fuzz
        fprintf('>>> Optimal solution found at iteration %d!\n', iter);
        % Highlight optimal point in Red
        % scatter(x_curr(1), x_curr(2), 120, 'r', 'LineWidth', 2);
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

hold off;
fprintf('\nFinal optimal x:\n');
disp(x_curr);