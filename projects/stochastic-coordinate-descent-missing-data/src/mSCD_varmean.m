function [x,Ea,t] = mSCD_varmean(A,x_tru,y,maxit,p,muVec,gamma)
% mSCD_varmean stochastic coordinate descent for linear systems with varying means for each column


% input matrix A, sol'n x_tru, vector y, #iterations maxit, probability p
% output approx solution x, approx error Ea, residual error Er, cpu time t

% init
[m,n] = size(A);
x = zeros(n,1);
%x = xn;

%X = zeros(n,maxit);
t = zeros(maxit,1);
%r = y;
%gamma = 1e-6;
I = eye(n); % choose column for standard basis vector


%BigOne = ones(m,1); % mx1 array, all entries are one 
% MuRow = mu*ones(m,1); % mx1 array, all entries are mean value 
%ONEONE = ones(m,n);
ONEMU = repmat(muVec, [m 1]); %mxn mu matrix

%SquareMu = MuRow'*MuRow; % 1x1 matrix, all entries are squared mean
%DiaMu = diag(diag(MuRow'*MuRow)); % diagonal for SquareMu

% iterates
Ea = zeros(maxit,1);
start = tic;
    for k = 0:maxit-1
        if mod(k,10000) == 0
            disp(k);
        end

        % j = mod(k,n)+1;
        j = randi(n);
        MuRow = muVec(j) * ones(m,1);
        MUrowOneMu = MuRow'*ONEMU;

        [mA] = bnmsk_varmean(A,p,muVec);
        e = I(:,j);
        r = mA*x - p*y;

        alpha = mA(:,j)'*r - (1-p)*(mA(:,j)'*ONEMU + MuRow'*mA)*x + (1-p)^2*(MUrowOneMu*x) + (1-p)*p*MuRow'*y;
        beta = (1-p)*(norm(mA(:,j))^2)*x(j) - (1-p)*(mA(:,j)'*MuRow + MuRow'*mA(:,j))*x(j) + (1-p)*(MuRow'*MuRow*x(j));
        x = x - gamma*(p^-2)*(alpha-beta)*e;

        Ea(k+1) = norm(x-x_tru)^2;
        t(k+1) = toc(start);
    end

end

%% Helper functions

function [mA] = bnmsk_varmean(A,p,muVec)
% bnmsk binary mask

% input matrix A and probability p
% output matrix mA with entries missing iid Bernoulli

[m,n] = size(A);
D = binornd(1,p,m,n);
mA = D.*A+(1-D).*repmat(muVec, [m 1]);

end