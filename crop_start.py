import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

out_crops = './crops/'
crop_height = 100

img = cv2.imread('board.png')
im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2 = img.copy()
# template3 = cv2.imread('assets/bar_lvl3.png', 0)
template_full = cv2.imread('assets/bar_lvl2.png', 0)
template2 = cv2.imread('assets/bar_lvl2_left.png', 0)
template1 = cv2.imread('assets/bar_lvl1_left.png', 0)
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]

# takes a list of selected points and their match values
# filters those that are neat each other
def filter_near(pt, ress, template_index, search_window = 20):
    pt = pt[::-1]
    score = ress[template_index][tuple(pt)]
    for res in ress:
        vert_search_range = range(max(0,pt[0] - search_window), min(res.shape[0] - 1, pt[0] + search_window))
        horiz_search_range = range(max(0,pt[1] - search_window), min(res.shape[1] - 1, pt[1] + search_window))
        for i in vert_search_range:
            for j in horiz_search_range:
                # if i == pt[0] and j == pt[1]:
                #     continue
                if res[(i,j)] > score:
                    return False
    return True

# Apply template Matching
# return a list of cropped images
def match_champs(img, templates, threshold = 0.6, method = 'cv2.TM_CCOEFF_NORMED'):
    method = eval(method)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ress = [cv2.matchTemplate(im_gray,template,method) for template in templates]    
    locs = [np.where( res >= threshold ) for res in ress]
    found_champs = []
    for i,loc in enumerate(locs):
        w, h = template_full.shape[::-1]#templates[i].shape[::-1]
        for pt in zip(*loc[::-1]):
            if filter_near(pt, ress, i):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255) if i else (0,255,0), 2)
                # cv2.imwrite(out_crops + '_' + str(pt[0]) + '_' + str(pt[1]) + '.png', img2[pt[1]:pt[1] + h + crop_height, pt[0]:pt[0]+w])
                found_champs += [(img[pt[1]:pt[1] + h + crop_height, pt[0]:pt[0]+w].copy(), i)]
    return found_champs

# apply template matching to each image in series of images
def process_frames(imgs, templates, threshold = 0.55, method = 'cv2.TM_CCOEFF_NORMED'):
    for i, img in enumerate(imgs):
        found_champs, template_matched = zip(*match_champs(img2, templates, threshold, method))
        for j, champ in enumerate(found_champs):
            cv2.imwrite(path.join(out_crops,'img_' + str(i) + 'template_' + str(template_matched[j]) + 'crop_' + str(j)+'.png') ,champ)

process_frames([img2], [template1, template2])

# plt.subplot(121),plt.imshow(res,cmap = 'gray')
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img2)
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle('cv2.TM_CCOEFF_NORMED')

plt.show()