%% Lab Topic 2_1.pdf, slide 2:
% Pseudo-random numbers.

%% Miriam Ramos Arevalo

%% 1. Generate 10,000 values from each function.
% rand: Generates numbers between 0 and 1 with no part of the range favored.
% randn: Generates Gaussian numbers centered at 0, positive or negative.
%        Numbers near 0 are common, numbers far from 0 are rare.

uniform_values = rand(10000, 1);     
gaussian_values = randn(10000, 1);     

%% 2. Plot one histogram for each set.
% A bin groups nearby values; its bar height counts the values in that bin.

figure;
subplot(1, 2, 1);                   % Left plot in a 1 row, 2column figure.
histogram(uniform_values, 30);      % We are using 30 bins.
title('rand: 10,000 values');
xlabel('Value');
ylabel('Count');

subplot(1, 2, 2);                   % Right plot in the same figure.
histogram(gaussian_values, 30);
title('randn: 10,000 values');
xlabel('Value');
ylabel('Count');

%% 3. Generate two sets of 5,000 values from randn, set same seed using rng.
% rng sets the starting point (seed) of the random number generator.
% Resetting the same seed makes rand and randn repeat their sequence.

% 1 is the seed: it sets the generator's starting point.
rng(1);                     
first_set = randn(5000, 1);

rng(1);                     % Reset the same seed to repeat the sequence.
second_set = randn(5000, 1);
%% 4. Compare the two sets. Do they repeat?

% Check whether every number matches at the same position in both sets.
% Store 1 if they all match, or 0 if they do not.
same_values = isequal(first_set, second_set);

% Print answer:
fprintf('Do all 5,000 values repeat? %d (1 = yes, 0 = no)\n', same_values);

% They should all match because we reset the same seed before making each set.


%% Sources about pseudo-random numbers:
%  - Introduction to Randomness and Random Numbers.
% Dr Mads Haahr
% https://www.random.org/randomness/

%  - Pseudo Random Number Generator (PRNG)
% https://www.geeksforgeeks.org/dsa/pseudo-random-number-generator-prng/
