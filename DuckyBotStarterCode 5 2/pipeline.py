import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import math
# The pipeline function takes in a numpy array of dimensions:
#   "height, width, color-space" 
# and MUST return an image of the SAME dimensions
#
# The pipeline function also takes a motorq. To make the motors move
# add messages to the queue of the form:
#   motorq.put( [ left-motor-speed , right-motor-speed ] )
# i.e.  motorq.put([32768,32768]) # make the motors go full-speed forward

        
    # THINGS YOU SHOULD DO...
    # 1. Copy the code INSIDE your pipeline function here.
    # 2. Ensure the pipeline function takes BOTH the image and motorq.


# ARE YOU CURIOUS HOW THIS ANSWER DIFFERS FROM THE CODE PROVIDED?
# SCROLL DOWN....
def Intersect(line1pt1, line1pt2, line2pt1, line2pt2):
     x1 = line1pt1[0]
     y1 = line1pt1[1]
     x2 = line1pt2[0]
     y2 = line1pt2[1]
     x3 = line2pt1[0]
     y3 = line2pt1[1]
     x4 = line2pt2[0]
     y4 = line2pt2[1]
     denom = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
     if denom == 0:
          return None
     else:
          px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/denom
          py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/denom
          return [px,py]

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8
    )
    img = np.copy(img)
    if lines is None:
        return

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)

    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

    return img

def pipeline(image,motorq):
    
    """
    An image processing pipeline which will output
    an image with the lane lines annotated.
    """

    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (0, height),
        (width / 2, 0),
        (width, height),
    ]
    blur = cv2.blur(image,(5,5))
    gray_image = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

    cannyed_image = cv2.Canny(gray_image, 100, 200)
 
    # cropped_image = region_of_interest(
    #     cannyed_image,
    #     np.array(
    #         [region_of_interest_vertices],
    #         np.int32
    #     ),
    # )
 
    lines = cv2.HoughLinesP(
        cannyed_image,
        rho=6,
        theta=np.pi / 60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
 
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    #print(lines)
    if not np.any(lines):
        return image
        
    for line in lines:
        for x1, y1, x2, y2 in line:
            #print line
            if (x2-x1) == 0:
                break
            slope = float(y2 - y1) / (x2 - x1)
            if math.fabs(slope) < 0.5:
                continue
            if slope <= 0:
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else:
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])

    if len(left_line_x)==0 or len(right_line_x)==0:
        return image

    min_y = int(image.shape[0] * (3 / 5))
    max_y = int(image.shape[0])

    poly_left = np.poly1d(np.polyfit(
        left_line_y,
        left_line_x,
        deg=1
    ))
 
    left_x_start = int(poly_left(max_y))
    left_x_end = int(poly_left(min_y))
 
    poly_right = np.poly1d(np.polyfit(
        right_line_y,
        right_line_x,
        deg=1
    ))
 
    right_x_start = int(poly_right(max_y))
    right_x_end = int(poly_right(min_y))

    line_image = draw_lines(
        image,
        [[
            [left_x_start, max_y, left_x_end, min_y],
            [right_x_start, max_y, right_x_end, min_y],
        ]],
        thickness=5,
    )

    x_int = Intersect([left_x_start, max_y], [left_x_end, min_y], [right_x_start, max_y], [right_x_end, min_y])[0]
    #print(line_image.shape()[0])
    middle = line_image.shape[0]/2
    if x_int < middle-140:
        motorq.put( [ -13000 , 0 ] )
    elif x_int > middle+140:
        motorq.put( [ 0, -13000 ] )
    else:
        motorq.put( [ -13000, -13000 ] )

    


    return line_image








# speed = -32768 to 32768
# motor.setSpeed(mspd), mspd 0 to 255
# motor.run(dir), dir BACKWARD, FORWARD, RELEASE, BRAKE

    #motorq.put([32768,32768]) # make the motors go full-speed forwarD