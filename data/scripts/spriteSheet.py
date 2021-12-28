import pygame

def spriteSheet(surface,cellSize):
    surfSize = surface.get_size()
    cellsx = surfSize[0]//cellSize[0]
    cellsy = surfSize[1]//cellSize[1]
    
    cellSurfs = []
    

    
    for celly in range(cellsy):
        for cellx in range(cellsx):
            cellSurf = pygame.Surface((cellSize[0],cellSize[1]),pygame.SRCALPHA)
            cellSurf.blit(surface,(-cellx*cellSize[0],-celly*cellSize[1]))

            cellSurfs.append(cellSurf)

    return cellSurfs
