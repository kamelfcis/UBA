import pandas as pd
import matplotlib.pyplot as plt

def plot_user_data(user):
    # Load the data
    file_path = f'Data/{user}/feature/data_out.csv'
    data = pd.read_csv(file_path, header=None)

    # Plotting each feature
    plt.figure(figsize=(12, 8))
    for i in range(data.shape[1]):
        plt.plot(data[i], label=f'Feature {i+1}')
    
    plt.title(f'User Behavior Features for {user}')
    plt.xlabel('Time Periods')
    plt.ylabel('Feature Values')
    plt.legend()
    plt.grid()
    
    # Save the plot as an image file
    plt.savefig(f'User_Behavior_Features_{user}.png')
    plt.close()

# Example usage for EDB0714
plot_user_data('EDB0714')
