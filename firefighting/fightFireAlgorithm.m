function [startFire, fireLocation] = fightFireAlgorithm(Biomass_Ammount, Crit_Mass)
% Alogrithm for deciding if it is best to start a fire

    % 100 max grown trees min
    if nargin == 1
        Crit_Mass = 14385 * 10;
    end
        
    Orig_Biomass_Ammount = Biomass_Ammount;

    % Normalize the values to 0 to 1
    Biomass_Ammount = mat2gray(Biomass_Ammount);

    BW = Biomass_Ammount > 0.2;

    s = regionprops(BW,Orig_Biomass_Ammount, 'WeightedCentroid', 'BoundingBox', 'PixelValues');
    
    if isempty(s)
        startFire = 0;
        fireLocation = [-1,-1];
        return
    end
    
    biomass_per_region = zeros(length(s),1);
    
    for i = 1:length(s)
        current_cent_val = s(i).PixelValues;
        biomass_per_region(i) = sum(current_cent_val);
    end
    
    [max_biomass, max_index] = max(biomass_per_region);
    
    DeadZone = 5;
    
    OnEdge = [s(max_index).BoundingBox(1:2) <= DeadZone, (s(max_index).BoundingBox(1:2)+s(max_index).BoundingBox(3:4)) >= size(Biomass_Ammount,1)-DeadZone];
    
    if max_biomass >= Crit_Mass && ~any(OnEdge)
        startFire = 1;
        
        pos = round(s(max_index).WeightedCentroid);
        
        fireLocation = pos;
    else
        startFire = 0;
        fireLocation = [-1,-1];
    end
end

