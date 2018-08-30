classdef World
    %Class containg information and functions for simulating forest fires.
    
    properties
        %Simulation Properties
        deltaT = 0.1 %Seconds
        simulationTime = 0 %Time since simulation began
        
        %World information
        tempratureCells
        biomassCells
        
        worldTemprature
    end
    
    methods
        function obj = World(Size)
            obj.tempratureCells = obj.worldTemprature * ones(Size);
        end
    end
    
end