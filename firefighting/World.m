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
            current_time = strcat(char(datetime('now', 'Format', 'yyyyMMddHHmmSS')), '.h5');

            obj.create_h5(current_time);
        end
        
        function obj = initRandomBiomass(obj)
            % Generates a random ammount of biomass and age
            randomAges = 120*365*24*rand(obj.fullWorldSize);

            randomBiomass = 14385*rand(obj.fullWorldSize);

            obj.world.treeAge = randomAges;

            obj.world.BiomassAmount = growUp(randomBiomass, randomAges, 24 * obj.deltaTime);
        end    
        
        function Info = getInfo(obj)
            % Returns
            % -------
            % out: dict
            %     Contains information on the current state of the simulation

            Info = struct('simTime', obj.simTime,...
                'onFire', obj.isOnFire,...
                'worldSize', obj.fullWorldSize,...
                'worldData', obj.world);
        end
        
        function obj = step(obj)
            
        end
        
        function autoSaveState(obj, normalInterval, fireInterval)
            % Autosaves data to the h5 file every x timesteps.
            %
            % Set to 0 to disable auto save
            %
            % Default is to save every simulation 720 steps and every 3 steps during a fire
            obj.normalInterval = normalInterval;
            obj.fireInterval = fireInterval;
        end
    end
    
    % Methods that should only be used by the class itself, not the user
    methods (Access = protected)
        function obj = create_h5(obj, filename) 
            true_filename = strcat('Datasets/', filename);
            
            obj.fp = H5F.create(true_filename);
        end
    end
end