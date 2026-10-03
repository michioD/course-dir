%SIMPLEX Crude simplex code for solving an LP problem given an
%        initial feasible basis beta.
%        [x,z,y,r,beta,iter] = simplex(A,b,c,beta)
%        solves the problem 
%                        minimize     c'x
%                        subject to   A x = b
%                                     x >= 0
%        
%        On successful termination, x contains the optimal solution, and
%        z contains the final objective function value. Y contains
%        an optimal dual solution and r contains the dual slacks. On entry,
%        beta is a row vector containing the indices of the basis, which
%        is assumed to be primal feasible. On exit, beta contains the indices
%        of the final basis and iter denotes the number of iterations. 
%
%        Notation selected to fit with the KTH course SF1811 Optimization.

%        Crude version, written by Anders Forsgren for use in SF1811 Optimization

function [x,z,y,r,beta,iter] = simplex(A,b,c,beta)

[m,n] = size(A);

iter = 0;
rnymin = -1;
fuzz = sqrt(eps);

% fprintf( '\n  Iter           zbar    betap      nyq           tmax \n' ) 
        
ny = [1:n];
ny(beta) = [];

Abeta = A(:,beta);
bbar = Abeta\b;

x(beta,1) = bbar;
x(ny,1) = zeros(length(ny),1);

while rnymin < -fuzz

  Abeta = A(:,beta);
  Any = A(:,ny);

  cbeta = c(beta);
  cny = c(ny);

  y = (Abeta')\cbeta;
   
  rny = cny-Any'*y;
     fprintf("badabingboom y")
    disp(y)
  zbar = cbeta'*bbar;
  
  if min(bbar) < -fuzz
    keyboard
    fprintf('\n Error, basis is not primal feasible \n\n')
    break;
  end
    
% Dantzig rule

  [rnymin,q] = min(rny);

  if iter == 0
      q = 1;
  end
  if rnymin < -fuzz
    k = ny(q);
    Abark = Abeta\A(:,k);
    Abarkpos = find(Abark>fuzz);
    if length(Abarkpos) > 0
      [tmax,ppos]= min(bbar(Abarkpos)./Abark(Abarkpos));
      p = Abarkpos(ppos);
    else
      fprintf('\n Problem has unbounded solution \n\n')
      break;
    end
    
    bbar = bbar-tmax*Abark;

    bbar(p) = tmax;

    betap = beta(p);
    nyq = ny(q);        
    beta(p) = nyq;
    ny(q) = betap;

    % str1 = sprintf( ' %5g   %12.5e', iter, zbar );
    % str2 = sprintf( ' %8g   %6g   %12.2e', betap, nyq, tmax );        
    % disp([str1 str2])
  
    iter = iter + 1;
    
  else
    % str1 = sprintf( ' %5g   %12.5e', iter, zbar );
    % str2 = sprintf( '\n' );        
    % disp([str1 str2])
  
    % fprintf( '  Optimal solution found \n\n' ) 
  end

end

x(beta,1) = bbar;
x(ny,1) = zeros(length(ny),1);

r(beta,1) = zeros(length(beta),1);
r(ny,1) = rny;

z = zbar;
