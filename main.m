% To make sure all files are in the path
setup

world = World(100);
world.initRandomBiomass()

world.fireChance = world.fireChance/5;

start_time = datetime('now');
% Step by x days
sim_stop_time = 24*365*1000;

time_since_last_man_fire = 0;

while world.simTime <= sim_stop_time
    world.step();
    
%     % Should of made a function to start a fire rather then man doing it
%     if world.isOnFire == false && (time_since_last_man_fire + 24*365*0.25) < world.simTime
%         [shouldStartFire, fireLocation] = fightFireAlgorithm(world.world_data.BiomassAmount);
%         if shouldStartFire
%             % Only try starting a fire every 365 days
%             time_since_last_man_fire = world.simTime;
%             
%             extra_box_width = 1;
%             for x = fireLocation(1)-extra_box_width:fireLocation(1)+extra_box_width
%                 for y = fireLocation(2)-extra_box_width:fireLocation(2)+extra_box_width
%                     world.world_data.BiomassAmount([y,x]) = 0;
%                     world.world_data.treeAge([y,x]) = 0;
%                 end
%             end
%         end
%     end
end

end_time = datetime('now');
total_time = end_time-start_time;

disp(total_time)

% Sound when done
beep