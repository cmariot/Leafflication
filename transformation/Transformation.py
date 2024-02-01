# Open original file w/ plantcv

# Links :
# - Gaussian blur :
# - Mask :
# - ROI Objects :
# - Analyse Objects :     https://plantcv.readthedocs.io/en/stable/tutorials/morphology_tutorial/
# - Pseudolandmarks :

# Display a color histogram

import argparse
from plantcv import plantcv as pcv
import plantcv as pcv2


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the image to transform
    """
    parser = argparse.ArgumentParser(
        prog='Transformation',
        description="Transform an image",
    )
    parser.add_argument('image_path')
    args = parser.parse_args()
    return args.image_path


def gaussian_blur(image):
    grayscale_img = pcv.rgb2gray_cmyk(
        rgb_img=image,
        channel='C'
    )
    # inverted = pcv.invert(grayscale_img)
    gaussian_img = pcv.gaussian_blur(
        img=grayscale_img,
        ksize=(11, 11),
        sigma_x=0,
        sigma_y=None
    )
    return gaussian_img


def main():
    image_path = parse_argument()
    image, path, name = pcv.readimage(image_path)
    pcv.plot_image(image)

    transformations = {
        "Gaussian Blur": gaussian_blur,
    }

    # for key, value in transformations.items():
    #     print(key)
    #     transformed_image = value(image)
    #     pcv.plot_image(transformed_image)

    s = pcv.rgb2gray_hsv(rgb_img=image, channel='s')
    pcv.plot_image(s)
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, object_type='light')
    #pcv.plot_image(s_thresh)
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    #pcv.plot_image(s_mblur)
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(3, 3), sigma_x=0, sigma_y=None)
    #pcv.plot_image(gaussian_bluri)

    b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    #pcv.plot_image(b)

    b_thresh=pcv.threshold.binary(gray_img=b, threshold=135,object_type='light')

    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
    #pcv.plot_image(bs)

    masked = pcv.apply_mask(img=image, mask=bs, mask_color='white')
    #pcv.plot_image(masked)

    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    #pcv.plot_image(masked_a)
    #pcv.plot_image(masked_b)

    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=135, object_type='light')

    #pcv.plot_image(maskeda_thresh)
    #pcv.plot_image(maskeda_thresh1)
    #pcv.plot_image(maskedb_thresh)

    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # pcv.plot_image(ab1)
    # pcv.plot_image(ab)

    opened_ab = pcv.opening(gray_img=ab)
    #pcv.plot_image(opened_ab)

    xor_img = pcv.logical_xor(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    #pcv.plot_image(xor_img)

    ab_fill = pcv.fill(bin_img=ab, size=200)
    print("fill")
    pcv.plot_image(ab_fill)
    #pcv.plot_image(ab_fill)
    closed_ab = pcv.closing(gray_img=ab_fill)
    #pcv.plot_image(gray_img=ab_fill)
    masked2= pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    pcv.plot_image(masked2)

    #obj_hierachy= pcv.find_objects(img=masked2, mask=ab_fill)

    #roi1, roi_hierarchy = pcv.roi.rectangle(img=masked2, x=(image.shape[0] * 0.1), y=(image.shape[1] * 0.1), w=(image.shape[0] * 0.9), h=(image.shape[1] * 0.9))
    roi= pcv.roi.rectangle(img=masked2, x=0,y=0, w=image.shape[0], h=image.shape[1])
    kept_mask = pcv.roi.filter(mask=ab_fill, roi=roi, roi_type='partial')
    #pcv.plot_image(filtered)
    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)
    print("analysis")
    pcv.plot_image(analysis_image)

    color_histogram = pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=kept_mask,label="default")
    pcv.plot_image(color_histogram)
    pcv.print_image(img=color_histogram, filename="histo.png")





if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)