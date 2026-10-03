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

r_vals = linspace(3.00, 9.00, 25);

xs = zeros(n, 25);
ys = zeros(n,25);
us = zeros(1,25);
vs = zeros(1,25);

sigma_vals = zeros(1,25);
mu_vals    = zeros(1,25);


% multiplying with 2 since quadprog halves it with 0.5 x'Hx
H = 2*C;
f = zeros(n,1);

% two equality constraints
Aeq = [mu'; ones(1,n)];
% lowerbound nonnegativity
lb = zeros(n,1);
% upperbound
ub = [];

for k = 1:25
    r = r_vals(k);
    % muTx eq r and eTx eq 1
    beq = [r; 1];
    % sol x
    [x, blah1, blah2, blah3, lambda] = quadprog(H,f,[],[],Aeq,beq,lb,ub,[]);

    % Solutions
    xs(:, k) = x;
    % Nonnegativity multiplier
    ys(:, k) = lambda.lower;
    % return constraint multiplier
    us(:, k) = lambda.eqlin(1);
    % budget constraint multiplier
    vs(:, k) = lambda.eqlin(2);
    
    sigma_vals(k) = sqrt(x' * C * x);
    mu_vals(k)    = mu' * x;
end


% plotting mu(x) against sigma(x) 
figure;
plot(sigma_vals, mu_vals, 'o-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('\sigma(x)'); 
ylabel('\mu(x)');
title('Excercise 3.1');
grid on;

