% Updated by: Miriam Ramos Arevalo; Lab Topic 2_2 - Slide 6.
% Date: November 2026.

%% Demo for colored Gaussian noise generation
%Sampling frequency for noise realization
sampFreq = 1024; %Hz
%Number of samples to generate
nSamples = 16384;
% Repeat the original demo with 1x, 2x, and 4x samples.
% Keep the sampling frequency, filter order, and Welch window the same as the original.
sampleCounts = nSamples*[1, 2, 4];
for runIndex = 1:numel(sampleCounts)
    nSamples = sampleCounts(runIndex);

    %Time samples
    timeVec = (0:(nSamples-1))/sampFreq;

    %Target two-sided PSD given by the inline function handle
    targetPSD = @(f) (f>=100 & f<=300).*(f-100).*(300-f)/10000;

    % Show the plots together for each sample count.
    figure('Name', sprintf('N = %d', nSamples), 'NumberTitle', 'off', ...
        'Position', [100, 100, 1100, 700]);
    subplot(2,2,1);
    
    %Plot PSD
    freqVec = 0:0.1:512;
    psdVec = targetPSD(freqVec);
    plot(freqVec,psdVec,'--','Color',[0.2,0.65,0.3],'LineWidth',1.5);
    hold on;

    %%
    % Design FIR filter with T(f)= square root of target PSD
    % sqrtPSD = sqrt(psdVec);
     fltrOrdr = 500;
    % b = fir2(fltrOrdr,freqVec/(sampFreq/2),sqrt(psdVec));
    % 
    % %%
    % % Generate a WGN realization and pass it through the designed filter
    % % (Comment out the line below if new realizations of WGN are needed in each run of this script)
    % rng('default'); 
    % inNoise = randn(1,nSamples);
    % outNoise = fftfilt(b,inNoise);

    %% Generate noise realization
    outNoise = statgaussnoisegen(nSamples,[freqVec(:),psdVec(:)],fltrOrdr,sampFreq);

    %%
    % Estimate the PSD
    % figure;
    % pwelch(outNoise, 512,[],[],sampFreq);
    % hold on;
    % pwelch(inNoise, 512, [], [], sampFreq);
    %Pwelch plots in dB (= 10*log10(x)); plot on a linear scale
    [pxx,f]=pwelch(outNoise, 256,[],[],sampFreq);
    plot(f,pxx);

    % Label the PSD plot.
    xlabel('Frequency (Hz)');
    ylabel('PSD');
    title(sprintf('Target and estimated PSD: N = %d', nSamples));
    legend('Target PSD', 'Estimated PSD');
    xlim([0, sampFreq/2]);
    grid on;

    % Plot noise realization
    % (or simulated noise)
    % Label the original time series.
    subplot(2,2,2);
    plot(timeVec,outNoise);
    xlabel('Time (s)');
    ylabel('Noise amplitude');
    title('Noise Realization');
    grid on;

    % Zoom in to see the oscillations in the noise.
    subplot(2,2,3);
    plot(timeVec,outNoise);
    xlim([1, 1.1]);
    xlabel('Time (s)');
    ylabel('Noise amplitude');
    title('Zoomed time series');
    grid on;

    % Inspect whether the noise values remain bell shaped.
    % PDF normalization makes the histogram heights comparable across runs.
    subplot(2,2,4);
    histogram(outNoise,50,'Normalization','pdf');
    xlabel('Noise amplitude');
    ylabel('Probability density');
    title('Noise histogram');
    grid on;

    % Add a title.
    sgtitle(sprintf('N = %d', nSamples));

    % Save each figure as a PNG.
    exportgraphics(gcf, fullfile(fileparts(mfilename('fullpath')), ...
        sprintf('noise_N_%d.png', nSamples)), 'Resolution', 150);
end


