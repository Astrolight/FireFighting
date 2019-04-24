clear;
clc;

% Each dataset should be in the folder
Datasets = dir('Datasets');
Datasets = Datasets([Datasets.isdir]);
Datasets = Datasets(3:end);

% Dataset, subdataset, Fire, (Edge, Mass)
% Hopping only 500 fires max
processed_data = NaN(length(Datasets), 10, 500, 2);

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

for i = 1:size(processed_data,1)
    for n=1:2
        new_processed_data(i,:,n) = reshape(processed_data(i,:,:,n),1,[]);
    end
end

for i = 1:size(processed_data,1)
    fig = figure;
    scatter(new_processed_data(i,:,2),new_processed_data(i,:,1))
    title(Datasets(i).name)
    xlabel('Mass Burned in Fire')
    ylabel('Fraction of Edges Burned')
    xlim([0,3E5])
    ylim([0,1])
    hold on
    plot(nanmean(new_processed_data(i,:,2)),nanmean(new_processed_data(i,:,1)),'r.','MarkerSize', 25)
    hold off
    saveas(fig, strcat(Datasets(i).name,'.png'))
end