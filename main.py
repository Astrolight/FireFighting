import firefighting

# Only run if this is the main file being ran
if __name__ == '__main__':
    world = firefighting.world.World(100)
    world.initRandomBiomass()

    # Step by 100 days
    for hour in range(24*100):
        world.step()
        world.saveState()
        
    world_Data = world.getInfo()['worldData']

    bioMass_Ammount = world_Data['BiomassAmount']

    fig = firefighting.rendering.generateHeatmap(bioMass_Ammount, maxValue=14385)
    
    #fig.show()