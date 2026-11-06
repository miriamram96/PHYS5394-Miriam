% Miriam Ramos Arevalo
% Lab Topic 2.2 - Slide 13
% Simulate initial LIGO noise.

% Adapted from NOISE/colGaussNoiseDemo.m. 
% Uses the original files of: NOISE/statgaussnoisegen.m and iLIGOSensitivity.txt.

%% Sampling frequency and number of samples
% 2048 Hz so that 700 Hz is below the Nyquist frequency (1024 Hz)
sampFreq = 2048; %Hz
nSamples = 65536;
fltrOrdr = 500;

%% Target PSD
% First column is frequency, second column is the ASD = sqrt(one-sided PSD)
y = load('iLIGOSensitivity.txt','-ascii');
freqVec = y(:,1);
psdVec = y(:,2).^2;

% Keep the PSD constant below 50 Hz and above 700 Hz
psd50 = interp1(freqVec,psdVec,50);
psd700 = interp1(freqVec,psdVec,700);
inBand = freqVec > 50 & freqVec < 700;

% Add f=0 and f=sampFreq/2 for fir2
freqVec = [0; 50; freqVec(inBand); 700; sampFreq/2];
psdVec = [psd50; psd50; psdVec(inBand); psd700; psd700];

%% Generate noise realization
% statgaussnoisegen uses a two-sided PSD, so divide the one-sided PSD by 2
outNoise = statgaussnoisegen(nSamples,[freqVec,psdVec/2],fltrOrdr,sampFreq);

%% Estimate the PSD and plot the target on top
% pwelch gives a one-sided PSD, which is what the target is
[pxx,f] = pwelch(outNoise,1024,[],[],sampFreq);
figure;
semilogy(f,pxx);
hold on;
semilogy(freqVec,psdVec,'k--','LineWidth',1.5);
xlabel('Frequency (Hz)');
ylabel('PSD (1/Hz)');
title('Simulated initial LIGO noise');
legend('Estimated PSD','Target PSD');
xlim([0, sampFreq/2]);
grid on;

% Save the PSD comparison as a PNG in this script's folder.
exportgraphics(gcf, fullfile(fileparts(mfilename('fullpath')), ...
    'ligo_noise_psd.png'), 'Resolution', 150);
