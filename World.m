classdef World < handle
    %Class containg information and functions for simulating forest fires.
    
    properties
        %Simulation Properties
        deltaT = 0.1 %Seconds
        simulationTime = 0 %Time since simulation began
        
        %Ver to store world data in
        dataCells
        
        %World information
        worldTemprature = 20 %Deg c
        worldSize
    end
    
    methods
        function obj = World(World_Size)
            if size(World_Size, 2) == 1
                World_Size = [World_Size,World_Size];
            end
            
            obj.worldSize = World_Size;
            
            obj.dataCells = cell(obj.worldSize);
            obj.dataCells(:) = {TreeCell(5,5)};
        end
        
        function obj = step(obj)
            %Updates simulation time
            obj.simulationTime = obj.simulationTime + obj.deltaT;
        end
        
        function tempratureArray = getTempratureArray(obj)
            tempratureArray = obj.dataCells{:,:}.Temprature;
        end
    end
    
        
    methods (Access=private, Static=true)
        function biomassMap = generateInitBiomass(World_Size)
            biomassMap = perlin2D(World_Size);
        end
    end
    
end