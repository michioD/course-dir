%%% hw3data.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem data for homework assignment 3, SF1811, 2025/2026
% Creates C and mu
clear;
rng(970729)
n=8;
Corr=zeros(n,n);
for i=1:n
for j=1:n
Corr(i,j)=(-1)^abs(i-j)/(abs(i-j)+1);
end
end
sigma_vals=zeros(n,1);
mu=zeros(n,1);
sigma_vals(1)=2;
mu(1)=3;
for i=1:n-1
    sigma_vals(i+1)=sigma_vals(i)+2*rand;
    mu(i+1)=mu(i)+1;
end
D=diag(sigma_vals);
C2=D*Corr*D;
C=0.5*(C2+C2');







%%  Original Problem %%%%%%%%%%%%%%%%%%%%%
r_vals = linspace(3, 9, 25);

% the 25 (x, u, v, y, sigma, mu) values we're storing 
x_vals = zeros(n, 25);
u_vals = zeros(1, 25);
v_vals = zeros(1, 25);
y_vals = zeros(n, 25);
sigma_vals = zeros(1, 25);
mu_vals = zeros(1, 25);


H = C;
f = zeros(n,1);

% the LHS of the equality constraints i.e mu and e

Aeq = [mu'; ones(1,n)];

% the lower bound ensuring nonnegativity
lb = zeros(n,1);

ub = [];

for k=1:25
    r = r_vals(k);
    % RHS for muTx =r and eTx = 1
    beq = [r;1];
    % sol x and multiplier values

    [x, blah1, blah2, blah3, lambda] = quadprog(H, f, [], [], Aeq, beq, lb, ub);

    % sols
    x_vals(:, k) = x;
    % multiplier for return constraint
    u_vals(:, k) = lambda.eqlin(1);
    %multiplier for budget constraint
    v_vals(:, k) = lambda.eqlin(2);
    % multiplier for nonnegativity
    y_vals(:, k) = lambda.lower;
    
    sigma_vals(k) = sqrt(x'*C*x);
    mu_vals(k) = mu'*x;
end


%% Modified Problem (e'x <= 1) %%%%%%%%%%%%%%%%

x_vals_mod = zeros(n, 25);
u_vals_mod = zeros(1, 25);
v_vals_mod = zeros(1, 25);
y_vals_mod = zeros(n, 25);
sigma_vals_mod = zeros(1, 25);
mu_vals_mod = zeros(1, 25);

%LHS and RHS of the inequality constraint for budget
A_ineq = ones(1,n); b_ineq = 1;

%LHS of the equality constraint for return
Aeq_mod = mu'; 

for k=1:25
    r = r_vals(k);
    % RHS for muTx =r
    beq_mod = r;
    % sol x and multiplier values

    [x, blah1, blah2, blah3, lambda] = quadprog(H, f, A_ineq, b_ineq, Aeq_mod, beq_mod, lb, ub);

    % sols
    x_vals_mod(:, k) = x;
    % multiplier for return constraint
    u_vals_mod(:, k) = lambda.eqlin;
    %multiplier for budget constraint
    v_vals_mod(:, k) = lambda.ineqlin;
    % multiplier for nonnegativity
    y_vals_mod(:, k) = lambda.lower;
    
    sigma_vals_mod(k) = sqrt(x'*C*x);
    mu_vals_mod(k) = mu'*x;
end

% plotting original and modified on same figure
figure();
plot(sigma_vals, mu_vals, 'bo-', 'LineWidth', 1.5, 'DisplayName', 'Original (e^Tx = 1)');
hold on;
plot(sigma_vals_mod, mu_vals_mod, 'ro-','LineWidth',1.5, 'DisplayName', 'Modified (e^Tx <= 1)'); 
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Exercise 3.2 (c)');
legend();
grid on;
hold off;
