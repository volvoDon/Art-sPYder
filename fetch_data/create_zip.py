import os
import PIL
import shutil
from get_by_search import LabelListPair
import config

class BuildPkg ():
    def __init__(
            self,
            label_list_data: list,
            output_format: str = "dir",
            test_size: float = None,
            dir_name: str = '../pkg',
            ):
        if type(label_list_data) == LabelListPair:
            self.label_list_data = [label_list_data]
        elif type(label_list_data) == list and all([type(x) == LabelListPair for x in label_list_data]):
            self.label_list_data = label_list_data
        elif label_list_data == None: self.label_list_data = None
        else:
            raise ValueError(f'{type(label_list_data)} is not a valid dtype')
        if test_size is not None and test_size > .9:
            raise ValueError(f'test size must be a fraction less than .9, you entered{test_size}')
        elif test_size < 1 and test_size > 0:
            self.test_size = test_size
        elif test_size <= 0:
            raise ValueError(f'test_size must be greater than zero less than 1: {test_size}')
        else:
            self.test_size = test_size
        if self.label_list_data is not None:
            #logic
            x= 3

    def create_pkg(self):
        assert self.label_list_data is not None
        

if __name__ == "__main__":
    print(os.listdir('./'))
        
        