% To make sure all files are in the path
setup

world = World(1000);
world.initRandomBiomass()

start_time = datetime('now');
% Step by x days
while world.simTime < 24*365
    world.step();
end
end_time = datetime('now');
total_time = end_time-start_time;

disp(total_time)
