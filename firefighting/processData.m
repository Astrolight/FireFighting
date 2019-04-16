function processedData = processData(h5_File)
% Takes in the location of the h5 dataset file and outputs a struct of
% processed data

    sim_time = h5read(h5_File, '/simTime');
    fire_sim_time = h5read(h5_File, '/isOnFire');

    bio_history = h5read(h5_File, '/world_data/BiomassAmount');
    fire_array = h5read(h5_File, '/world_data/treeOnFire');

    start_fire = strfind(fire_sim_time, [0,1]);
    end_fire = strfind(fire_sim_time, [1,0]);

    all_anaylsis = [];
    
    if length(start_fire) ~= length(end_fire)
        end_fire(end+1) = start_fire(end);
    end

    for time_pair = [start_fire; end_fire]
        start_fire_time = time_pair(1);
        end_fire_time = time_pair(2);

        % Get all frames during a single fire
        current_chunk = fire_array(:,:,start_fire_time:end_fire_time);

        total_fire_tiles = sum(current_chunk, 3);
        bool_fire_tiles = logical(total_fire_tiles);

        total_tiles_burned = sum(bool_fire_tiles, 'all');
        total_burned_biomass = sum(total_fire_tiles.*bool_fire_tiles, 'all');

        curr_anal_struct = struct(...
            'fire_start',start_fire_time,'fire_end',end_fire_time,...
            'total_burned_hours', end_fire_time-start_fire_time,...
            'tiles_burned', bool_fire_tiles, 'total_burned_biomass', total_burned_biomass);

        all_anaylsis = [all_anaylsis, curr_anal_struct];
    end
    
    processedData = all_anaylsis;
end

