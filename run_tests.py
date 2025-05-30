from inf_gan import fire_main
import pandas as pd

CONFIG_FILE = "brian_testing/configs.csv"  # or configs.json

def load_configs(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path).to_dict(orient="records")
    else:
        raise ValueError("Only CSV config files are supported.")


def main():
    configs = pd.read_csv(CONFIG_FILE).to_dict(orient="records")

    for i, config in enumerate(configs):
        fire_main(config=config, config_num=i+1)

if __name__ == "__main__":
    main()