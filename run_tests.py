from inf_gan import run_main
import pandas as pd

CONFIG_FILE = "configs.csv"  # or configs.json

def main():
    configs = pd.read_csv(CONFIG_FILE).to_dict(orient="records")

    for i, config in enumerate(configs):
        print(f"Running config {i+1} of {len(configs)}")

        run_main(config_num=i+1, optimiser=config['optimiser'],
                       initial_noise_size=config['initial_noise_size'], noise_size=config['noise_size'])
        
        print(f"Config {i+1} of {len(configs)} complete")

if __name__ == "__main__":
    main()