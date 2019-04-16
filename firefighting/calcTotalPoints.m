function total_Points = calcTotalPoints(processed_Data_Struct)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

    total_Points = 0;
    for i = 1:length(processed_Data_Struct)
        total_Points = total_Points + ...
            metricAnalysis(processed_Data_Struct(i).tiles_burned);
    end
end

