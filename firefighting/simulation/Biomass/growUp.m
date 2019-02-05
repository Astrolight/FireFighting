function newBiomass = growUp(biomass_ammount, age, dage)
%     
%     Simulates the growth of a tree with a biomass and a specific age
% 
%     Parameters
%     ----------
%     biomass_ammount: matrix of float
%         Defines the ammount of biomass that is being dealt with
% 
%     age: matrix of integer
%         Defines the age of the tree in hours
% 
%     dage: float
%         Defines the change of age

    % The ideal mass of an adult tree
    OPTIMUM_TREE_MASS = 14385;  % Or 14.385 tonns
    TREELIFETIME = 120*365*24;  % AKA 120 years

    newBiomass = zeros(size(biomass_ammount));

    newBiomass(age <= TREELIFETIME) =  0.0136834094368 * age(age <= TREELIFETIME);
    % Linear line bettwen age=0, biomass=0 to age=TREELIFETIME, biomass=OPTIMUM_TREE_MASS

    newBiomass(TREELIFETIME < age) = -0.082100456621 * age(TREELIFETIME < age) + 100688;
end

