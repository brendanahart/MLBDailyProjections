%% Initialization

%% ================ Part 1: Feature Normalization ================

%% Clear and Close Figures
clear ; close all; clc

fprintf('Loading data ...\n');

%% Load Data
data = csvread('071817data.csv');
playerNamesTest = data((1:floor(end/2)), 1);
playerNamesTarget = data((1:end), 1);
testX = data((1:floor(end/2)), 2:10);
testy = data(1:(floor(end/2)), 11);
testExamples = length(testy);

% (floor(end/2) + 1)

targetX = data((1:end), 2:10);
targetY = data((1:end), 11);

fprintf('Normalizing Features ...\n');

% [testX mu sigma] = featureNormalize(testX);

% Add intercept term to X
testX = [ones(testExamples, 1) testX];

%% ================ Part 2: Gradient Descent ================

fprintf('Running gradient descent ...\n');

% Choose some alpha value
alpha = 0.01;
num_iters = 1500;
num_features = 9;

% Init Theta and Run Gradient Descent 
theta = zeros((num_features + 1), 1)
[theta, J_history] = gradientDescent(testX, testy, theta, alpha, num_iters);

% Plot the convergence graph
figure;
plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Cost J');

% Display gradient descent's result
fprintf('Theta computed from gradient descent: \n');
fprintf(' %f \n', theta);
fprintf('\n');

%% ================ Part 3: Test Gradient Descent ================
targetExamples = length(targetY);

% normalize 
% targetX = (targetX - mu)./(sigma);

% add bias 
targetX = [ones(targetExamples, 1) targetX];

predictY = targetX * theta;

output = [playerNamesTarget predictY];

csvwrite('071817output.csv', output);

errorM = targetY - predictY;

error = (1/targetExamples)*sum(((targetY - predictY).^2))




