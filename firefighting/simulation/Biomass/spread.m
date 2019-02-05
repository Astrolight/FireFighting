function spread_rand_binary_matrix = spread(biomass_ammount)
%     Does the spreading of trees to new areas
% 
%     Returns a binary array where 1 values are trees spreading

    binary_biomass = biomass_ammount ~= 0;

    b = 0.01*ones(3,3);
    
    conv_array = conv2(binary_biomass, b, 'same');

    % 1% chance of spreading from single ajacent cell
    spread_rand_binary_matrix = conv_array > rand(size(biomass_ammount));
end

