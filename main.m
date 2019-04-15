% To make sure all files are in the path
setup

world = World(100);
world.initRandomBiomass()

start_time = datetime('now');
% Step by x days
sim_stop_time = 24*365*1000;

while world.simTime <= sim_stop_time
    world.step();
    
    % Should of made a function to start a fire rather then man doing it
    if world.isOnFire == false
        [shouldStartFire, fireLocation] = fightFireAlgorithm(world.world_data.BiomassAmount);
        if shouldStartFire
            world.isOnFire = true;
            world.world_data.treeOnFire(fireLocation) = true;
        end
    end
end

end_time = datetime('now');
total_time = end_time-start_time;

disp(total_time)

% Sound when done
beep