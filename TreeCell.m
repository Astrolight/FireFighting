classdef TreeCell < handle
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here  
    
    properties
        cellTemprature %In C
        
        cellBiomass %In kg
    end
    
    %Properties that all classes share the same value of
    properties (Constant)
        %Plant proprties
        typicalTreeAge = 150; %Years
    end
    
    methods
        function obj = TreeCell(initTemp, initBiomass)
            %Initlizes the TreeCell object
            obj.cellTemprature = initTemp;
            obj.cellBiomass = initBiomass;
        end
    end
end