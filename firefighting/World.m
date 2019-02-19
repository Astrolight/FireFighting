classdef World < handle
    %Class containg information and functions for simulating forest fires.
    
    properties
        simTime = 0;  % Hours
        deltaTime = 24;  % Hours

        % Sets the world size
        fullWorldSize

        % Creates a struct containg world elements
        world_data

        isOnFire = false;

        % Veribles to make sure simulation is steped only when needed
        lastSpreadTime = -100
        lastSaveTime = -100
        
        % How often to autosave
        normalInterval
        fireInterval
        
        fireChance = 0.0005 % 1% every day to set on fire
    end
    
    properties (Access = protected)
        % H5 file id
        h5_file
        chunksize = 16
        
        h5_frame_num = 1
        
        % 1D data sets
        h51D = {'simTime', 'isOnFire'};
        
        % Caching to save data and processing time for writing data
        Cache1D = struct('simTime', [],...
                        'isOnFire', []);
        
        Cache2D = struct('WaterLevel', [],...
                      'BiomassAmount', [],...
                      'DiffTemprature', [],...
                      'treeAge', [],...
                      'treeOnFire', []);
        
        cache_level = 1;
        
        % 2D data sets
        h52D = {'BiomassAmount', 'treeAge', 'treeOnFire'};
    end
    
    methods
        function obj = World(worldSize)
            
            obj.fullWorldSize = [worldSize, worldSize];
            
            obj.world_data = struct('WaterLevel', zeros(obj.fullWorldSize),...
                      'BiomassAmount', zeros(obj.fullWorldSize),...
                      'DiffTemprature', zeros(obj.fullWorldSize),...
                      'treeAge', zeros(obj.fullWorldSize),...
                      'treeOnFire', zeros(obj.fullWorldSize, 'logical'));
            
            % Stuff for creating h5 file
            % Returns the current time in ISO 8601 UTC Format (yyyyMMddHHmmss)
            current_time = strcat(char(datetime('now', 'Format', 'yyyyMMddHHmmSS')), '.h5');

            obj.create_h5(current_time);
            obj.autoSaveState(720, 3);
        end
        
        function initRandomBiomass(obj)
            % Generates a random ammount of biomass and age
            randomAges = 120*365*24*rand(obj.fullWorldSize);

            randomBiomass = 14385*rand(obj.fullWorldSize);

            obj.world_data.treeAge = randomAges;

            obj.world_data.BiomassAmount = growUp(randomBiomass, randomAges, 24 * obj.deltaTime);
        end    
        
        function Info = getInfo(obj)
            % Returns
            % -------
            % out: struct
            %     Contains information on the current state of the simulation

            Info = struct('simTime', obj.simTime,...
                'onFire', obj.isOnFire,...
                'worldSize', obj.fullWorldSize,...
                'worldData', obj.world_data);
        end
        
        function step(obj)
            % Steps the simulation by deltaT time.
            % Simulates tree growth and other required processes. 
            
            obj.simTime = obj.simTime + obj.deltaTime;

            % Updates tree age
            current_tree_age = obj.world_data.treeAge;
            obj.world_data.treeAge(current_tree_age ~= 0) = ...
                obj.world_data.treeAge(current_tree_age ~= 0) + obj.deltaTime;

            % Temprature only changes when on fire
            if obj.isOnFire
                % Set simulation step speed to 1 hour
                obj.deltaTime = 1;

                % Spreads and burns the biomass
                obj.world_data.treeOnFire = fireSpread(...
                    obj.world_data.BiomassAmount,obj.world_data.treeOnFire);
                
                obj.world_data.BiomassAmount = fireBurn(...
                    obj.world_data.BiomassAmount,obj.world_data.treeOnFire);
                
                obj.killTrees();
                
                % Saves simulation if on fire during specified interval
                if obj.fireInterval ~= 0 && mod(obj.simTime, obj.fireInterval) == 0
                    obj.saveState()
                end
                
                % If no trees are left on fire, disable isOnFire
                if ~any(obj.world_data.treeOnFire)
                    obj.isOnFire = false;
                end
            else
                % Set simulation step to 24 hours just because no need for smaller timestep
                obj.deltaTime = 24;

                % If the forrest is not currently on fire and once per day
                if obj.simTime - obj.lastSpreadTime >= 24

                    obj.lastSpreadTime = obj.simTime;

                    obj.world_data.BiomassAmount = growUp(...
                        obj.world_data.BiomassAmount, obj.world_data.treeAge, 24 * obj.deltaTime);

                    biomass_spread = spread(obj.world_data.BiomassAmount);
                    obj.world_data.treeAge(biomass_spread) = obj.world_data.treeAge(biomass_spread) + 1;
                    
                    obj.killTrees();
                end

                % Saves simulation if not on fire during specified interval
                if obj.normalInterval ~= 0 && (obj.simTime - obj.lastSaveTime) > obj.normalInterval
                    obj.lastSaveTime = obj.simTime;

                    obj.saveState();
                end
                
                % If rand number is lower then 0.01, start fire
                if rand(1) < obj.fireChance
                    obj.isOnFire = true;
                    obj.world_data.treeOnFire(randsample(prod(obj.fullWorldSize),1)') = true;
                end
            end
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
        
        function saveState(obj)
            % Saves the file in a hdf5 file format
            
            % If ammount of data is not yet at min level, save for chunking
            % later
            if obj.cache_level <= obj.chunksize
                
                % Saves the 1d arrays
                for dataset = obj.h51D
                    % For some reason always default to 1x1 cell
                    char_dataset = char(dataset);

                    obj.Cache1D.(char_dataset)(obj.cache_level) = obj.(char_dataset);
                end

                % Saves the 2d arrays
                for dataset = obj.h52D
                    char_dataset = char(dataset);

                    obj.Cache2D.(char_dataset)(:, :, obj.cache_level) = double(obj.world_data.(char_dataset));
                end
                
                obj.cache_level = obj.cache_level + 1;
                return
            end

            % Disables warning about values being clampted when saved
            warning('off', 'MATLAB:imagesci:hdf5dataset:datatypeOutOfRange')
            
            % Saves the 1d arrays
            for dataset = obj.h51D
                % For some reason always default to 1x1 cell
                char_dataset = char(dataset);
                
                current_val = obj.Cache1D.(char_dataset);
                converted_val = uint32(current_val);
                
                h5write(obj.h5_file, char(strcat('/', dataset)), converted_val, [1, obj.h5_frame_num], [1,obj.chunksize])
            end

            % Saves the 2d arrays
            for dataset = obj.h52D
                char_dataset = char(dataset);
                
                current_val = double(obj.Cache2D.(char_dataset));
                
                h5write(obj.h5_file, char(strcat('/world_data/', dataset)),...
                    current_val, [1, 1, obj.h5_frame_num], [obj.fullWorldSize, obj.chunksize])
                
            end
            
            % Bump up increment
            obj.h5_frame_num = obj.h5_frame_num + obj.chunksize;
            obj.cache_level = 1;
        end
    end
    
    % Methods that should only be used by the class itself, not the user
    methods (Access = protected)
        function  create_h5(obj, filename) 
            obj.h5_file = fullfile(pwd, 'Datasets/', filename);
            
            % Initalize a blank h5 file
            H5F.create(obj.h5_file).close;
            
            % Init 1D datasets
            h5create(obj.h5_file, '/simTime', [1, Inf], 'ChunkSize', [1, obj.chunksize], 'Datatype', 'uint32');
            h5create(obj.h5_file, '/isOnFire', [1, Inf], 'ChunkSize', [1, obj.chunksize], 'Datatype', 'uint8');
            
            % Init 2D datasets
            for dataset = obj.h52D
                h5create(obj.h5_file, char(strcat('/world_data/' ,dataset)), [obj.fullWorldSize, Inf],...
                    'ChunkSize', [obj.fullWorldSize, obj.chunksize], 'Datatype', 'single');
            end
        end
        
        function killTrees(obj)
            DeadTrees = obj.world_data.BiomassAmount < 0;
            
            obj.world_data.treeAge(DeadTrees) = 0;
            obj.world_data.BiomassAmount(DeadTrees) = 0;
            obj.world_data.treeOnFire(DeadTrees) = 0;
        end
    end
end