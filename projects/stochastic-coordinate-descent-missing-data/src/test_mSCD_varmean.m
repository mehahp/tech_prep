
close all; clc; clear

mm = 100;
nn = 20;

AA = randn(mm,nn);
muVec = [ones(1,nn/2) ones(1,nn/2)*10];
AA = AA+repmat(muVec, [mm,1]);
xx = randn(nn,1);
yy = AA*xx;

cond(AA)
[x2,Ea2,t2] = mSCD_varmean(AA,xx,yy,50000,.9,muVec,0.00001);


semilogy(Ea2);