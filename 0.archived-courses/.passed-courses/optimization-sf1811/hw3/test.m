%%% hw3data.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
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
rvals = linspace(3.00, 9.00, 25);
X = zeros(n,25);
Y = zeros(n,25);
U = zeros(1,25);
V = zeros(1,25);
Sigmas = zeros(1,25);
Mus = zeros(1,25);
%% SOLVE THE QUADRATIC PROGRAM FOR EACH r
% The modified problem is:
% minimize (1/2) x^T C x
% subject to mu^T x = r
% e^T x <= 1
% x >= 0
H = 2*C; % quadprog uses (1/2)x'Hx
f = zeros(n,1);
Aeq = mu'; % equality constraint mu^T x = r
A = ones(1,n); % inequality e^T x <= 1
b = 1;
lb = zeros(n,1);
ub = [];
options = optimoptions('quadprog','Display','off');
for k = 1:25
    r = rvals(k);
    beq = r;
    [x,~,~,~,lambda] = quadprog(H,f,A,b,Aeq,beq,lb,ub,[],options);
% Save primal and dual variables
    X(:,k) = x;
    U(k) = lambda.eqlin(1); % multiplier for mu^T x = r
    V(k) = lambda.ineqlin(1); % multiplier for e^T x <= 1
    Y(:,k) = lambda.lower; % duals for x >= 0
% Risk (std dev) and return
    Sigmas(k) = sqrt(x' * C * x);
    Mus(k) = mu' * x;
end
%% PLOT σ vs μ
figure;
plot(Sigmas, Mus, 'o-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Exercise 3.2 Modified');
grid on;