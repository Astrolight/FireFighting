function [startFire, fireLocation] = fightFireAlgorithm(Biomass_Ammount, Crit_Mass)
% Alogrithm for deciding if it is best to start a fire

    % 100 max grown trees min
    if nargin == 1
        Crit_Mass = 14385 * 100;
    end
        
    Orig_Biomass_Ammount = Biomass_Ammount;

    % Normalize the values to 0 to 1
    Biomass_Ammount = mat2gray(Biomass_Ammount);

    BW = imbinarize(Biomass_Ammount, 'adaptive');

    s = regionprops(BW,Orig_Biomass_Ammount, 'centroid', 'BoundingBox', 'PixelValues');
    
    biomass_per_region = zeros(length(s),1);
    
    for i = 1:length(s)
        current_cent_val = s(i).PixelValues;
        biomass_per_region(i) = sum(current_cent_val);
    end
    
    [max_biomass, max_index] = max(biomass_per_region);
    
    OnEdge = [s(max_index).BoundingBox <= 1, s(max_index).BoundingBox >= size(Biomass_Ammount,1)];
    
    if max_biomass >= Crit_Mass && ~any(OnEdge)
        startFire = 1;
        fireLocation = s(max_index).Centroid;
    else
        startFire = 0;
        fireLocation = [-1,-1];
    end
end

