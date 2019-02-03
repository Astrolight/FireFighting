import firefighting
import time

# Only run if this is the main file being ran
if __name__ == '__main__':

    world = firefighting.world.World(500)
    world.initRandomBiomass()

    start_time = time.time()
    # Step by x days
    for hour in range(24*365):
        world.step()
    end_time = time.time()
    total_time = end_time-start_time

    print('Simulation took {:.2f} seconds for {} steps at {:.2f} steps per second.'.format(total_time, hour, hour/total_time))
        
    world_Data = world.getInfo()['worldData']

    bioMass_Ammount = world_Data['BiomassAmount']