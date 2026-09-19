%%% hw3data.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

% plot for mu(x), sigma(x)

figure; 

plot(sigma_vals, mu_vals,'o-', 'LineWidth',1.5)
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Excercise 3.1');
grid on;




