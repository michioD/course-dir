%%% Homework 3 - Variant: Original vs Modified (μ'x >= r) %%%%%%%%%
clear; clc; close all;

% -------------------------------------------------
% Generate data (same seed as in the report)
% -------------------------------------------------
rng(970729)                    % Jonathan's birth date
n = 8;

% Correlation structure
Corr = zeros(n,n);
for i = 1:n
    for j = 1:n
        Corr(i,j) = (-1)^abs(i-j) / (abs(i-j) + 1);
    end
end

% Standard deviations and expected returns
sigma = zeros(n,1);  mu = zeros(n,1);
sigma(1) = 2;        mu(1) = 3;
for i = 1:n-1
    sigma(i+1) = sigma(i) + 2*rand;
    mu(i+1)     = mu(i) + 1;
end
D = diag(sigma);
C2 = D * Corr * D;
C  = 0.5*(C2 + C2');          % Ensure symmetric positive semidefinite

% Target returns
rvals = linspace(3.00, 9.00, 25);

% Pre-allocation
sigma_orig = zeros(1,25);   mu_orig = zeros(1,25);
sigma_mod  = zeros(1,25);   mu_mod  = zeros(1,25);

H = 2*C;                       % quadprog minimizes (1/2)x'Hx, so this makes objective x'Cx (but problem is 1/2 x'Cx, scaling doesn't affect x*)
f = zeros(n,1);
options = optimoptions('quadprog','Display','off');

% -------------------------------------------------
% 1) Original problem: μ'x = r, e'x = 1, x >= 0
% -------------------------------------------------
Aeq_orig = [mu'; ones(1,n)];   % [μ'; e']
lb = zeros(n,1);

for k = 1:25
    r = rvals(k);
    beq = [r; 1];
    x = quadprog(H,f,[],[],Aeq_orig,beq,lb,[],[],options);
    sigma_orig(k) = sqrt(x'*C*x);
    mu_orig(k)    = mu'*x;
end

% -------------------------------------------------
% 2) Modified problem: μ'x >= r, e'x = 1, x >= 0
% -------------------------------------------------
A_ineq = -mu';                 % -μ'x <= -r for μ'x >= r
Aeq_mod = ones(1,n);           % e'x = 1
beq_mod = 1;
lb = zeros(n,1);

for k = 1:25
    r = rvals(k);
    b_ineq = -r;
    x = quadprog(H,f,A_ineq,b_ineq,Aeq_mod,beq_mod,lb,[],[],options);
    sigma_mod(k) = sqrt(x'*C*x);
    mu_mod(k)    = mu'*x;
end

% -------------------------------------------------
% Plot both frontiers together
% -------------------------------------------------
figure('Position',[100 100 700 550]);
plot(sigma_orig, mu_orig, 'bo-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Original (μ''x = r)');
hold on;
plot(sigma_mod,  mu_mod,  'ro-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Modified (r <= μ''x)');
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Exercise 3.3(c) Markowitz Frontier Original vs Modified ');
legend();
grid on;
axis tight;
hold off;