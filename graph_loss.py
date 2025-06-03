import re
import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    # Read in the data from the txt file
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def get_loss_data(data):
    # Parse the data from the txt file
    loss_data = pd.DataFrame(columns=["Step", "Unaveraged Loss", "Averaged Loss"])
    for line in data.split("\n"):
        # Split each line into a list of strings
        split_str = re.split(' |: |\t', line)

        # If the line is too short, skip it
        if len(split_str) < 2:
            continue

        # Extract numerical values from the line
        nums = []
        for s in split_str:
            try:
                nums.append(float(s))
            except ValueError:
                continue
        
        # If the line has 3 numbers, then the third number is the averaged loss
        avg_loss = nums[2] if len(nums) == 3 else None

        # Add the loss data to the dataframe
        loss_data.loc[len(loss_data)] = [nums[0], nums[1], avg_loss]
    return loss_data

def main():
    # Generate loss plots for each config
    for i in range(8):
        # Get loss data from txt file
        file_path = f"logs/{i+1}_loss_results.txt"
        data = read_data(file_path)
        loss_data = get_loss_data(data)
    
        # Plot loss data
        ax = loss_data.plot(x="Step", y="Unaveraged Loss", kind="line", label="Unaveraged Loss")
        loss_data.plot(x="Step", y="Averaged Loss", kind="line", ax=ax, label="Averaged Loss")
        plt.ylabel("Loss")
        plt.title("Unaveraged and Averaged Loss over Steps")
        plt.legend()
        plt.savefig(f"logs/plot_{i+1}_loss.png")
        plt.close()

if __name__ == "__main__":
    main()