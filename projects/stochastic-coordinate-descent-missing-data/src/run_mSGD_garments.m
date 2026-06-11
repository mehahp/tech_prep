%% mSCD real world data set example 

close all; clc; clear

%% Parameters
numTrials = 20;
maxIter = 100000;
p = .85;
saveRun = 1; % 1 = save figures, 0 = dont save figures

%% Load raw data set
% 	Data loads as .mat file from CSV import
load(fullfile('..','data','garments.mat'))
onehot = @(X)bsxfun(@eq, X(:), 1:max(X));


%% Pre-Process data set
% 	Categorical variables to one hot vectors
%		Column 2: quarter
% 		Column 3: department 
% 		Column 4: day of the week
% 	Numerival variables to arrays
%		Columns 5-14: various numerical data
% 		Column 15: response variable (productivity)
col2 = garmentsworkerproductivity(:,2);
col2 = double(table2array(col2));
col2onehot = double(onehot(col2));

col3 = garmentsworkerproductivity(:,3);
col3 = double(table2array(col3));
col3onehot = double(onehot(col3));

col4 = garmentsworkerproductivity(:,4);
col4 = double(table2array(col4));
col4onehot = double(onehot(col4));

%col5to14 = garmentsworkerproductivity(:,5:14);
col5to14 = garmentsworkerproductivity(:, [5, 6, 7, 11, 12, 13]);
col5to14 = double(table2array(col5to14));

col15 = garmentsworkerproductivity(:,15);
col15 = double(table2array(col15));

%% Construct Linear System
% 	AA: team statistics (department, target, overtime, number of style changes, etc.)
% 	yy: team productivity
% AA = [col2onehot col3onehot col4onehot col5to14];
AA = [col5to14];
yy = col15;
xls = pinv(AA)*yy; 
norm(AA * xls - yy)
cond(AA)

%% Estimate means for each column 
muVec = mean(AA)

%% Run mSCD_varmean on data set
[mm,nn] = size(AA);
approxErr = zeros(maxIter, 1);

for tt = 1:numTrials
    tt
    [~,approxErrBuff,~] = mSCD_varmean(AA, xls, yy, maxIter, p, muVec, 0.000005);
    approxErr = approxErr + approxErrBuff;
end

approxErr0 = zeros(maxIter, 1);

for tt = 1:numTrials
    tt
    [~,approxErrBuff0,~] = mSCD_varmean(AA, xls, yy, maxIter, p, zeros(1,nn), 0.000005);
    approxErr0 = approxErr0 + approxErrBuff0;
end

figure
semilogy(approxErr/numTrials, 'LineWidth',4,'DisplayName','Mean imputation')
hold on
semilogy(approxErr0/numTrials, 'LineWidth',4,'DisplayName', 'Zero imputation')
xlabel('Iterations')
ylabel('Approximation Error')
set(gca,'FontSize',12);
legend('show')

%% savefig
if(saveRun)
	fname = sprintf('figs/%s_%.2fpp', mfilename(pwd), p);
	saveas(gcf, strcat(fname ,'.png'))
	saveFigure(strcat(fname ,'.fig'))
end







