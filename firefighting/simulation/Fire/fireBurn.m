function newBiomassAmount = fireBurn(BiomassAmount,treeOnFire)
% Function to decrement the amount of tree material (biomass) left after a
% fire step

    % Remove 10% of max tree mass each hour
    biomass_deduct = 0.1*14385;
    
    newBiomassAmount = BiomassAmount - biomass_deduct*treeOnFire;

end

