import re
import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def get_loss_data(data):
    loss_data = pd.DataFrame(columns=["Step", "Unaveraged Loss", "Averaged Loss"])
    for line in data.split("\n"):
        split_str = re.split(' |: |\t', line)
        if len(split_str) < 2:
            continue

        nums = []
        for s in split_str:
            try:
                nums.append(float(s))
            except ValueError:
                continue
        
        avg_loss = nums[2] if len(nums) == 3 else None
        loss_data.loc[len(loss_data)] = [nums[0], nums[1], avg_loss]
    return loss_data

def main():
    for i in range(8):
        file_path = f"logs/{i+1}_loss_results.txt"
        data = read_data(file_path)
        loss_data = get_loss_data(data)
        print(loss_data.tail())
    
        ax = loss_data.plot(x="Step", y="Unaveraged Loss", kind="line", label="Unaveraged Loss")
        loss_data.plot(x="Step", y="Averaged Loss", kind="line", ax=ax, label="Averaged Loss")
        plt.ylabel("Loss")
        plt.title("Unaveraged and Averaged Loss over Steps")
        plt.legend()
        plt.savefig(f"logs/plot_{i+1}_loss.png")
        plt.close()

if __name__ == "__main__":
    main()