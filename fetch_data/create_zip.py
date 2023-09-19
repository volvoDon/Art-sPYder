import os
from PIL import Image
from io import BytesIO
import shutil
from get_by_search import LabelListPair
import config
import requests

class BuildPkg ():
    def __init__(
            self,
            label_list_data: list,
            output_format: str = "dir",
            test_size: float = None,
            dir_name: str = './pkg',
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
        elif test_size < 0:
            raise ValueError(f'test_size must be greater than/ equal to zero less than .9: {test_size}')
        else:
            self.test_size = test_size
            self.dir_name = dir_name
            self.output_format = output_format
        if self.label_list_data is not None:
            #logic
            x= 3

    def create_pkg(self):
        assert self.label_list_data is not None
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
        if self.test_size > 0:
            if not os.path.exists(f'{self.dir_name}/test'):
                os.mkdir(f'{self.dir_name}/test')
            if not os.path.exists(f'{self.dir_name}/train'):
                os.mkdir(f'{self.dir_name}/train')
        else:
            for obj in self.label_list_data:
                p = f'{self.dir_name}/{obj.data["label"]}'
                if not os.path.exists(p):  # Check if directory exists before creating it
                    os.mkdir(p)
                name = obj.data["label"]
                for i, imglnk in enumerate(obj.data['links']):
                    n = name+str(i)
                    self.__save_image_from_url(imglnk, p, n)


                    

    def __save_image_from_url(self, url, path_to_save, name):
        # Fetch the image
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Determine file extension from content type or from the URL
        content_type = response.headers.get('content-type')
        if 'jpeg' in content_type or 'jpg' in content_type:
            file_extension = '.jpg'
        elif 'png' in content_type:
            file_extension = '.png'
        # Add more extensions as needed, or use a more sophisticated method
        else:
            # Fallback method: Extract from URL
            file_extension = os.path.splitext(url)[1]
    
        # Convert to a PIL Image
        img = Image.open(BytesIO(response.content))

        # Save the image to the specified path with the appropriate file extension
        img.save(f'{path_to_save}/{name}{file_extension}')
   

if __name__ == "__main__":
    Bird = LabelListPair("Bird")
    Dog = LabelListPair("Dog")
    Build = BuildPkg([Bird,Dog],test_size=0)
    Build.create_pkg()   
        