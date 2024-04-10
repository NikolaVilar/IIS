from src.constants.data_constants import reference_data_path
from src.constants.data_constants import current_data_path
from src.models.utils import helper

def main():
    current_df = helper.load_data(current_data_path)
    current_df.to_csv(reference_data_path, index=False)

if __name__ == '__main__':
    main()