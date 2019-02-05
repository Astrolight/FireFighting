classdef World < handle
    %Class containg information and functions for simulating forest fires.
    
    properties
        simTime = 0;  % Hours
        deltaTime = 24;  % Hours

        % Sets the world size
        fullWorldSize

        % Creates a struct containg world elements
        world

        isOnFire = false;

        % Veribles to make sure simulation is steped only when needed
        lastSpreadTime = -100
        lastSaveTime = -100
        
        % H5 file pointer
        fp
    end
    
    methods
        function obj = World(worldSize)
            
            obj.fullWorldSize = [worldSize, worldSize];
            
            obj.world = struct('WaterLevel', zeros(obj.fullWorldSize),...
                      'BiomassAmount', zeros(obj.fullWorldSize),...
                      'DiffTemprature', zeros(obj.fullWorldSize),...
                      'treeAge', zeros(obj.fullWorldSize),...
                      'hasFire', zeros(obj.fullWorldSize, 'logical'));
            
            % Stuff for creating h5 file
            % Returns the current time in ISO 8601 UTC Format (yyyyMMddHHmmss)
            current_time = char(datetime('now', 'Format', 'yyyyMMddHHmmSS'));

            obj.create_h5(current_time);
        end
    end
    
    % Methods that should only be used by the class itself, not the user
    methods (Access = protected)
        function obj = create_h5(obj, filename)
            obj.fp = H5F.create(filename);
        end
    end
end