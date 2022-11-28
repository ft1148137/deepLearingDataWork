class_name_proj = {'Shoe':'shoe',
'Cable':'cable',
'Cheerios':'cheerios',
'Carpet fringe':'carpet_fringe',
'dock':'dock',
'carpet boundary':'carpet_boundary',
'cheerios':'cheerios', 
'furniture leg':'furniture_leg', 
'shoe':'shoe', 
'cable':'cable', 
'fringe':'carpet_fringe',
'Threshold':'threshold'
}

class_ids = {'shoe':0, 'cable':1, 'cheerios':2, 'fringe':3, 'furniture leg':4,
            'Shoe':0,'Cable':1, 'Cheerios':2, 'Carpet fringe':3,
            'dock':5,'carpet boundary':6,'Threshold':7}
data_augumentation_dir = r'../Classification/Data_Augmentation/'

###############将图片按label分类时的路径#########
annopath_classification = r'../data_d/data/label/'
img_path_classification = r'../data_d/data/Img/'
txt_label_path_classification = r'../data_d/data/label/'
dir_path_classification = r'../Classification/imgs_class/'

###############为图片标签计数时所使用的路径########
annopath_count = r'../datasetOrdered/labels/'
# annopath_count = r'../data_d/data/label/'
# annopath_count = r'../data/qfeel_detect/3_ikea/labels/'

###############图像旋转时的路径及旋转角度############

class_rotation_angle = {'cable':[90,180,270],
                        'carpet_boundary':[180],
                        'carpet_fringe':[90,180,270],
                        'cheerios':[90,180,270],
                        'dock':[90,180,270],
                        'furniture_leg':[],
                        'shoe':[180],
                        'threshold':[90,180,270]}

img_path_rotation = dir_path_classification
img_path_rotated = data_augumentation_dir

###############图像翻转时的路径及旋转角度############

class_mirror_mode = {'cable':[True,False,False],
                    'carpet_boundary':[True,False,False],
                    'carpet_fringe':[True,False,False],
                    'cheerios':[True,False,False],
                    'dock':[True,False,False],
                    'furniture_leg':[True,False,False],
                    'shoe':[True,False,False],
                    'threshold':[True,False,False]
                    }

img_path_mirror = dir_path_classification
img_path_mirrored = data_augumentation_dir

###############图片颜色增强时使用的参数#############
img_path_color_transform = dir_path_classification
img_path_color_transformed = data_augumentation_dir
### [historgramColor, clahe, brightness] #####
class_color_transform_mode = {'cable':[False,True,True],
                    'carpet_boundary':[False,True,True],
                    'carpet_fringe':[False,True,True],
                    'cheerios':[False,True,True],
                    'dock':[False,True,True],
                    'furniture_leg':[False,True,True],
                    'shoe':[False,True,True],
                    'threshold':[False,True,True]
                    }

clahe_img_ksize = 8
brightness_diff = 40
