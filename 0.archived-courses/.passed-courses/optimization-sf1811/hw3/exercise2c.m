%%% hw3data.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem data for homework assignment 3, SF1811, 2025/2026
% Creates C and mu
clear;
rng(970729) % Replace YYMMDD by one member's date of birth
n=8;
Corr=zeros(n,n);
for i=1:n
for j=1:n
Corr(i,j)=(-1)^abs(i-j)/(abs(i-j)+1);
end
end
sigma=zeros(n,1);
mu=zeros(n,1);
sigma(1)=2;
mu(1)=3;
for i=1:n-1
    sigma(i+1)=sigma(i)+2*rand;
    mu(i+1)=mu(i)+1;
end
D=diag(sigma);
C2=D*Corr*D;
C=0.5*(C2+C2');

r_vals = linspace(3.00, 9.00, 25);

% create 2 versions of the sigma and mu vectors
sigma_vals = zeros(1,25);
mu_vals = zeros(1,25);


% quadprog uses (1/2)x'Hx
H = 2*C;
f = zeros(n,1);
options = optimoptions('quadprog','Display','off');


%---------- Original problem
Aeq_orig = [mu'; ones(1,n)];   % [mu'; e']
lb = zeros(n,1);

for k = 1:25
    r = r_vals(k);
    beq = [r; 1];
    x = quadprog(H,f,[],[],Aeq_orig,beq,lb,[],[]);
    sigma_vals(k) = sqrt(x'*C*x);
    mu_vals(k)    = mu'*x;
end


%---------------------- Modified problem: e'x <= 1
sigma_mod  = zeros(1,25);
mu_mod  = zeros(1,25);

xs = zeros(n, 25);
ys = zeros(n,25);
us = zeros(1,25);
vs = zeros(1,25);

A_ineq = ones(1,n);            % e'x <= 1
b_ineq = 1;
Aeq_mod = mu';                 % only mu'x = r is equality
beq_mod = r_vals;               % vector for the loop

for k = 1:25
    r = r_vals(k);
    [x, blah1, blah2, blah3, lambda] = quadprog(H,f,A_ineq,b_ineq,Aeq_mod,r,lb,[],[]);
    xs(:, k) = x;
    ys(:, k) = lambda.lower;
    us(k) = lambda.ineqlin; % Store the dual variables for the inequality constraint
    vs(k) = lambda.eqlin;               % Store the dual variables for the equality constraint
    sigma_mod(k) = sqrt(x'*C*x);
    mu_mod(k)    = mu'*x;
end

% -------------------------------------------------
% Plot both frontiers together
% -------------------------------------------------
figure('Position',[100 100 700 550]);
plot(sigma_vals, mu_vals, 'bo-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Original (e''x = 1)');
hold on;
plot(sigma_mod,  mu_mod,  'ro-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Modified (e''x <= 1)');
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Exercise 3.2 (c)');
legend();
grid on;
axis tight;
hold off;