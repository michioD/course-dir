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

% Target returns
rvals = linspace(3.00, 9.00, 25);

% Pre-allocation
sigma_orig = zeros(1,25);   mu_orig = zeros(1,25);
sigma_ss   = zeros(1,25);   mu_ss   = zeros(1,25);

H = 2*C;                       % quadprog minimizes (1/2)x'Hx
f = zeros(n,1);
options = optimoptions('quadprog','Display','off');

% -------------------------------------------------
% 1) Original problem: μ'x = r, e'x = 1, x >= 0
% -------------------------------------------------
Aeq = [mu'; ones(1,n)];       % [μ'; e']
beq_orig = [rvals; ones(1,25)];
lb_orig = zeros(n,1);
ub = [];

for k = 1:25
    beq = [rvals(k); 1];
    x = quadprog(H,f,[],[],Aeq,beq,lb_orig,ub,[],options);
    sigma_orig(k) = sqrt(x'*C*x);
    mu_orig(k)    = mu'*x;
end

% -------------------------------------------------
% 2) Short selling allowed: μ'x = r, e'x = 1, no bounds on x
% -------------------------------------------------
lb_ss = [];  % No lower bounds (allows x < 0)

for k = 1:25
    beq = [rvals(k); 1];
    x = quadprog(H,f,[],[],Aeq,beq,lb_ss,ub,[],options);
    sigma_ss(k) = sqrt(x'*C*x);
    mu_ss(k)    = mu'*x;
end

% -------------------------------------------------
% Plot both frontiers together
% -------------------------------------------------
figure('Position',[100 100 700 550]);
plot(sigma_orig, mu_orig, 'bo-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Original (x \geq 0)');
hold on;
plot(sigma_ss,  mu_ss,  'ro-', 'LineWidth',1.8, 'MarkerSize',6, ...
     'DisplayName','Short selling allowed (removed x \geq 0)');
xlabel('\sigma(x)');
ylabel('\mu(x)');
title('Exercise 3.4(c) Original vs allowing Short Selling markowitz frontier');
legend('Location','southeast');
grid on;
axis tight;
hold off;