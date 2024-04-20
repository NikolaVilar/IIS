
from src.constants.data_constants import train_data_path
from src.constants.data_constants import test_data_path
from src.constants.data_constants import reference_data_path
from src.models.utils import helper

def test_train_split(df):
    print('Test, train split in process.')
    
    split_index = int(len(df) * 0.9)  # 10% of the freshest data
    print(f"Total size: {len(df)}. Split index: {split_index}")
    
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    train_df.to_csv(train_data_path)
    test_df.to_csv(test_data_path)
    
    
def main():    
    df = helper.load_data(reference_data_path)
    test_train_split(df)


if __name__ == '__main__':
    main()    
    
    