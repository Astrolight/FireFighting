clear;
clc;

% Each dataset should be in the folder
Datasets = dir('Datasets');
Datasets = Datasets([Datasets.isdir]);
Datasets = Datasets(3:end);

% Dataset, subdataset, Fire, (Edge, Mass)
% Hopping only 500 fires max
processed_data = zeros(length(Datasets), 10, 500, 2);

for i = 1:length(Datasets)
    folder = strcat('Datasets','/',Datasets(i).name);
    
    Data_files = dir(folder);
    Data_files = Data_files(3:end);
    
    for n = 1:length(Data_files)
        Data_file_loc = strcat(folder,'/',Data_files(n).name);
        test = processData(Data_file_loc);
        
        for k = 1:length(test)
            
            
            processed_data(i,n,k,1) = metricAnalysis(test(k).tiles_burned);
            processed_data(i,n,k,2) = test(k).total_burned_biomass;
        end
    end 
end