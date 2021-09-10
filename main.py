__author__ = 'Junghwan Kim'
__copyright__ = 'Copyright 2016-2018 Junghwan Kim. All Rights Reserved.'
__version__ = '1.0.0'

import os
import shutil
import cv2


def main():

    # Set input path
    path = '/home/jkim/NAS/raw_dicom/brain/_3_infarction/FROM/NCCT'

    # Output information
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nGround Truth %s' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\nYou set path: %s' % (__version__, path)

    # Set variables
    result = 0
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Recur load input directories
    for dir in sorted(dirs):

        # Check folder
        if not dir.isdigit():
            continue

        # Output loaded folder
        print '\n[LOAD]', path + '/' + dir

        # Set path
        path_target = path + '/' + dir + '/gtruth'

        # New folder
        if not os.path.exists(path_target):
            os.makedirs(path_target)
        else:
            shutil.rmtree(path_target)
            os.makedirs(path_target)

        # Get png list
        list_png = []
        for paths, dirs, files in sorted(os.walk(path + '/' + dir + '/images')):
            for name in sorted(files):
                if name.endswith('.png'):
                    list_png.append(name)

        # Get tif list
        list_tif = []
        for paths, dirs, files in sorted(os.walk(path + '/' + dir)):
            for name in sorted(files):
                if name.endswith('.tif'):
                    list_tif.append(name)

        # Count tif list and png list
        if len(list_tif) != len(list_png):
            print '[ERROR] The number of tif and the number of png are different.', path + dir
            exit(1)

        # Overlay images
        files = 0
        for png, tif in zip(sorted(list_png), sorted(list_tif)):

            img_1 = cv2.imread(path + '/' + dir + '/images/' + png)
            img_1_height, img_1_width, img_1_channels = img_1.shape

            img_2 = cv2.imread(path + '/' + dir + '/' + tif)
            img_2_height, img_2_width, img_2_channels = img_2.shape

            # Check image size
            if img_1_height != img_2_height or img_1_width != img_2_width or img_1_channels != img_2_channels:
                print '[ERROR] The size of PNG file and the size of TIF file are different: ' + png + ', ' + tif
                exit(1)

            img = cv2.addWeighted(img_1, 1, img_2, 1, 0)
            cv2.imwrite(path_target + '/' + png, img)
            files += 1

        # Complete every process
        result += 1
        print '[SUCCESS]', files, 'images are created.'

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\n', result, 'Folders are processed successfully.'

    return None


if __name__ == '__main__':
    main()
