% To make sure all files are in the path
setup

world = World(100);
world.initRandomBiomass()

start_time = datetime('now');
% Step by x days
sim_stop_time = 24*365*1000;

while world.simTime <= sim_stop_time
    world.step();
end

end_time = datetime('now');
total_time = end_time-start_time;

disp(total_time)