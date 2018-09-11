classdef World < handle
    %Class containg information and functions for simulating forest fires.
    
    properties
        %Simulation Properties
        deltaT = 0.1 %Seconds
        simulationTime = 0 %Time since simulation began
        
        %World data storage cells
        dataCells
        %Structure to store data in
        cellData=struct(...
                'Temprature', [], ...
                'Water_Level', [], ...
                'Tree_Age', [], ...
                'Biomass', [] ...
                )
        
        %World information
        worldTemprature = 20 %Deg c
        worldSize
        
        %Plant proprties
        typicalTreeAge = 150 %Years
    end
    
    methods
        function obj = World(World_Size)
            if size(World_Size, 2) == 1
                World_Size = [World_Size,World_Size];
            end
            
            obj.worldSize = World_Size;
            
            obj.dataCells(obj.worldSize(:)) = obj.cellData;
        end
        
        function obj = step(obj)
            %Updates simulation time
            obj.simulationTime = obj.simulationTime + obj.deltaT;
        end
        
        function tempratureArray = getTempratureArray(obj)
            tempratureArray = obj.dataCells{:,:}.Temprature;
        end
    end
    
end