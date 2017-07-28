%% Initialization

%% ================ Part 1: Feature Normalization ================

%% Clear and Close Figures
clear ; close all; clc

fprintf('Loading data ...\n');

%% Load Data
data = csvread('071917results.csv');
predictY = data(:,3);
targetY = data(:,2);

%% Error Calculation
errorM = targetY - predictY;
targetExamples = size(targetY,1);

error = (1/targetExamples)*sum(((targetY - predictY).^2))