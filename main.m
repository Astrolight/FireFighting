% To make sure all files are in the path
setup

world = World(100);
world.initRandomBiomass()

f = waitbar(0, 'Running...');

start_time = datetime('now');
% Step by x days
sim_stop_time = 24*365*1000;
while world.simTime <= sim_stop_time
    world.step();
    waitbar(world.simTime/sim_stop_time, f)
end
close(f)
end_time = datetime('now');
total_time = end_time-start_time;

disp(total_time)

Datasets = dir('Datasets');
last_dataset = Datasets(end);
last_dataset = fullfile( last_dataset.folder, last_dataset.name);

bio_history = h5read(last_dataset, '/world_data/BiomassAmount');

implay(mat2gray(bio_history), 60);