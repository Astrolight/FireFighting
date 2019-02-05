% To make sure all files are in the path
setup

world = World(1000);
world.initRandomBiomass()

start_time = now;
% Step by x days
while world.simTime < 24*365
    world.step();
end
end_time = now;
total_time = end_time-start_time;

sprintf('Simulation took %.2f seconds', total_time)
