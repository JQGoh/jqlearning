% 
%     This Matlab script compares the efficiencies of different schemes
%     implementing the periodic boundary conditions for Ising model problem.
% 
%     Author: JQ e-mail: gohjingqiang [at] gmail.com
%     Date:   29-10-2014

clear all;
close all;

tstart = cputime;
tic
% Initialize the system
L = 1000
num = 100 % Total number of sweeps
spin = ones(L, L); % 2D square lattice, spin up
T = 300; % 300 K, for temperature

% Method 3, using if-else conditions
rng(10)
for k = 1:num
    for i = 1:L
        for j = 1:L   
            % Determine the displacement along i-dimension
            if i == 1
                di1 = L;
                di2 = 2;
            elseif i == L
                di1 = L - 1;
                di2 = 1;
            else
                di1 = i - 1;
                di2 = i + 1;
            end

            % Determine the displacement along j-dimension
            if j == 1
                dj1 = L;
                dj2 = 2;
            elseif j == L
                dj1 = L - 1;
                dj2 = 1;
            else
                dj1 = j - 1;
                dj2 = j + 1;
            end            
            
            % eflip, the change in the energy of system if we flip the
            % spin(i, j). eflip depends on the configuration of 4 neighboring
            % spins. For instance, with reference to spin(i, j), we should evaluate
            % eflip based on spin(i+1, j), spin(i-1, j), spin(i, j+1), spin(i, j-1)
            Eflip = 2*spin(i,j)*(...
                    spin(di1,j) + ...  % -1 in i-dimension 
                    spin(di2,j) + ...  % +1 in i-dimension 
                    spin(i,dj1) + ...  % -1 in j-dimension 
                    spin(i,dj2) ...    % +1 in j-dimension       
                    );
            if (Eflip <= 0)                    
                    spin(i,j) = -1*spin(i,j);                     
            else                    
                if (rand <= exp(-Eflip/T))                       
                    spin(i,j) = -1*spin(i,j);                    
                end
            end                    
        end
    end                                                  
end     
tend = cputime;
toc
spin;
time = tend - tstart
