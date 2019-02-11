function newTreeOnFire = fireSpread(BiomassAmount,treeOnFire)
% Function to spread the fire around the world

    max_tree_mass = 14385;

    % Matrix with only the currently on fire tree mass
    fireBiomass = BiomassAmount .* treeOnFire;
    
    % Gets all values bettwen 0 and 1
    normFireBiomass = fireBiomass/max_tree_mass;
    
    % Creates a nice little 5x5 gaussian
    weighted_matrix = fspecial('gaussian',5);
    
    fireCutOff = rand(size(normFireBiomass));
    
    weightedBiomassMatrix = conv2(normFireBiomass, weighted_matrix, 'same');

    %  weightedBiomassMatrix must be a bigger value then the fireCutOff
    newTreeOnFire = or(weightedBiomassMatrix > fireCutOff, treeOnFire);
    
end

