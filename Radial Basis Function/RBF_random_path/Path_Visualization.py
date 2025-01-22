import matplotlib.pyplot as plt
import pandas as pd

def plot_grid_path(path_UAV, path_target):
    # Create the grid
    length = 62
    width = 57
    grid = [[0] * width for _ in range(length)]
    
    # Mark the path in the grid
    #for coord in path_UAV:
    #    y, x = coord
    #   grid[x][y] = 1
      
    # Plot the grid
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap='Greys', origin='lower',)
    
    # Add gridlines
    ax.set_xticks(range(width))
    ax.set_yticks(range(length))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Draw lines for the path_UAV
    for i in range(len(path_UAV) - 1):
        x1, y1 = path_UAV.loc[i,:]
        x2, y2 = path_UAV.loc[i + 1,:]
        ax.plot([x1, x2], [y1, y2], color='red')  
     
    # Draw lines for the path_target
    for j in range(len(path_target) - 1):
        x1, y1 = path_target.loc[j,:]
        x2, y2 = path_target.loc[j + 1,:]
        ax.plot([x1, x2], [y1, y2], color='green')      
    
    plt.grid(color='grey', lw=1)
    plt.show()
        
# Example usage
path_UAV = pd.read_excel("path_UAV.xlsx")
path_target = pd.read_excel("path_target.xlsx")
plot_grid_path(path_UAV, path_target)
