clear;
[A, b, c, beta] = hw1data(021012);
[m, n] = size(A);

figure(1);
polyplot(A, b, [0; 10], [0; 10]);
xlabel('x_1')
ylabel('x_2')
hold on;

ny = 1:n;

ny(beta) = [];
fuzz = sqrt(eps);
iteration = 0;


while iteration < 10
    iteration = iteration +1;

    Abeta = A(:, beta);
    Any = A(:, ny);