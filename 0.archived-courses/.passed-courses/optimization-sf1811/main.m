A = zeros(14,16);
%the following 14 lines are the coefficients of each inequality used to populate the constraint matrix 
A(1, 13) = 2; A(1, 14) = 3; 
A(2, 13) = 1; A(2, 14) = 2;
A(3, 15) = 2; A(3, 16) = 3;
A(4, 15) = 1; A(4, 16) = 2;

A(5, 1) = 1; A(5, 7) = 1;
A(6, 2) = 1; A(6, 8) = 1;
A(7, 3) = 1; A(7, 9) = 1;
A(8, 4) = 1; A(8, 10) = 1;
A(9, 5) = 1; A(9, 11) = 1;
A(10, 6) = 1; A(10, 12) = 1;

A(11, 13) = -1; A(11, 1) = 1; A(11, 2) = 1; A(11, 3) = 1;
A(12, 14) = -1; A(12, 4) = 1; A(12, 5) = 1; A(12, 6) = 1;
A(13, 15) = -1; A(13, 7) = 1; A(13, 8) = 1; A(13, 9) = 1;
A(14, 16) = -1; A(14, 10) = 1; A(14, 11) = 1; A(14, 12) = 1;

Aeq = []; % no equality constraints defined 
beq = []; 

%max prod and availible labor constraints

b = [600; 
    500; 
    800; 
    700;
    % market cap on units sold constraint
    100;
    150; 
    200; 
    120; 
    100; 
    150; 
    % flow balance constraints
    0; 
    0; 
    0; 
    0];

c = [4 6 9 4 6 9 5 4 7 5 4 7 30 50 30 50] - [60 60 60 90 90 90 60 60 60 90 90 90 0 0 0 0];

% lower bound
lb = zeros(16,1);  

x = linprog(c, A, b, Aeq, beq, lb);

max_profit = -c*x;

disp(['max profit is ' num2str(max_profit) 'kr']);
