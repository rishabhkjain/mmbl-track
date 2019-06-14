% Analysis script
% this script should take csv files and analyze the data to return: 
% histogram of average velocities 
% histogram of net displacement
% average net displacement for this test

%% Metadata
% NEED A WAY TO PULL THIS DATA FROM VIDEO OR CSV FILES? 

% video duration (s)
dur = 34 ; 

% total # frames
frames = 106 ; 

%% Histogram of Average Velocities

filename = uigetfile('*.csv') ; 

% col 1 = swimmer #
% col 2 = total disp (px)
% col 3 = total # frames tracked
% col 4 = direction list (rad)
% col 5 = frames list

A = readmatrix(filename) ; 

names = A(:,1) ; 
totaldisp = A(:,2) ; 
avgvel = totaldisp / dur ; 

figure(1) 
histogram(avgvel) ; 
xlabel('Bin (px/s)') ; ylabel('Count') ; title(sprintf('Histogram of Average Velocities for %s',filename)) ; 
% 
% figure(2)
% plot(sumx,sumy)
% xlabel('X disp (px)'); ylabel('Y disp (px)') ; title(sprintf('Trajectory of %s',filename)) ; 

%% Histogram of Net Displacements

selpath = uigetdir ; 
names = dir(sprintf('%s/*.csv',selpath)); 
list = {names.name} ; 
numfiles = length(list);

% col 1 = frame #
% col 2 = dx (px)
% col 3 = dy (px)
% col 4 = total disp (px)
% col 5 = dtheta (rad)

% create vectors to save data
netx = zeros(numfiles,1) ; 
nety = zeros(numfiles,1) ; 
netdisp = zeros(numfiles,1) ; 

% process all the files
for n = 1:numfiles
    
    filename = names(n).name ; 
    B = readmatrix(filename) ; 

    dx = B(:,2) ; 
    sumx = zeros(length(dx),1) ; 
    sumx(1,1) = dx(1,1) ; 

    for i = 2:length(sumx(:,1)) 
        sum = dx(i, 1) + sumx(i-1,1) ; 
        sumx(i,1) = sum ; 
    end 

    dy = B(:,3) ; 
    sumy = zeros(length(dy),1) ; 
    sumy(1,1) = dy(1,1) ; 

    for i = 2:length(sumy(:,1)) 
        sum = dy(i, 1) + sumy(i-1,1) ; 
        sumy(i,1) = sum ; 
    end 

    netx(n) = abs(sumx(end,1) - sumx(1,1)) ; 
    nety(n) = abs(sumy(end,1) - sumy(1,1)) ; 
    netdisp(n) = sqrt((netx(n)^2) + (nety(n)^2)) ; 
    
end

figure(2) 
subplot(3,1,1) ; 
histogram(netx) ; 
xlabel('Bin (px)') ; ylabel('Count') ; title('Histogram of Net X Disp') ; 

subplot(3,1,2) ; 
histogram(nety) ; 
xlabel('Bin (px)') ; ylabel('Count') ; title('Histogram of Net Y Disp') ; 

subplot(3,1,3) ; 
histogram(netdisp) ; 
xlabel('Bin (px)') ; ylabel('Count') ; title('Histogram of Net Disp') ; 

%% Average Net Displacement

avg_netx = mean(netx) ; 
avg_nety = mean(nety) ; 
avg_netdisp = mean(netdisp) ; 