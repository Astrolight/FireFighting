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
    end
    
    properties (Access = protected)
        % H5 file id
        h5_file
        chunksize = 16
        
        h5_frame_num = 1
        
        % 1D data sets
        h51D = {'simTime', 'isOnFire'};
        
        % 2D data sets
        h52D = {'WaterLevel', 'BiomassAmount', 'DiffTemprature', 'treeAge', 'hasFire'};
    end
    
    methods
        function obj = World(worldSize)
            
            obj.fullWorldSize = [worldSize, worldSize];
            
            obj.world_data = struct('WaterLevel', zeros(obj.fullWorldSize),...
                      'BiomassAmount', zeros(obj.fullWorldSize),...
                      'DiffTemprature', zeros(obj.fullWorldSize),...
                      'treeAge', zeros(obj.fullWorldSize),...
                      'hasFire', zeros(obj.fullWorldSize, 'logical'));
            
            % Stuff for creating h5 file
            % Returns the current time in ISO 8601 UTC Format (yyyyMMddHHmmss)
            current_time = strcat(char(datetime('now', 'Format', 'yyyyMMddHHmmSS')), '.h5');

            obj.create_h5(current_time);
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

            % Disables warning about values being clampted when saved
            warning('off', 'MATLAB:imagesci:hdf5dataset:datatypeOutOfRange')
            
            % Saves the 1d arrays
            for dataset = obj.h51D
                % For some reason always default to 1x1 cell
                char_dataset = char(dataset);
                
                current_val = obj.(char_dataset);
                converted_val = uint32(current_val);
                
                h5write(obj.h5_file, char(strcat('/', dataset)), converted_val, [1, obj.h5_frame_num], [1,1])
            end

            % Saves the 2d arrays
            for dataset = obj.h52D
                char_dataset = char(dataset);
                
                current_val = double(obj.world_data.(char_dataset));
                
                h5write(obj.h5_file, char(strcat('/world_data/', dataset)),...
                    current_val, [1, 1, obj.h5_frame_num], [obj.fullWorldSize, 1])
                
            end
            
            % Bump up increment
            obj.h5_frame_num = obj.h5_frame_num + 1;
        end
    end
    
    % Methods that should only be used by the class itself, not the user
    methods (Access = protected)
        function obj = create_h5(obj, filename) 
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
    end
end