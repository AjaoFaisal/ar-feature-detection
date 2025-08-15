import cv2
import numpy


# --- Resize each image in a row to the specified new_size ---
def resize_image(row, new_size):
    resized_row = []
    for image in row:
        resized_image = cv2.resize(src=image, dsize=new_size)
        resized_row.append(resized_image)
    return resized_row


# --- Ensure all images are in BGR color format ---
def ensure_color(resized_row):
    colored_resized_row = []
    for image in resized_row:
        # Convert grayscale images to BGR
        if len(image.shape) == 2:
            colored_image = cv2.cvtColor(src=image, code=cv2.COLOR_GRAY2BGR)
        else:
            colored_image = image
        colored_resized_row.append(colored_image)
    return colored_resized_row


# --- Stack multiple rows of images into a single image ---
def stack_images(rows, new_size):
    resized_rows = []
    for row in rows:
        # Resize all images in the current row
        resized_row = resize_image(row, new_size)
        resized_rows.append(resized_row)

    colored_resized_rows = []
    for resized_row in resized_rows:
        # Ensure all images are in color (BGR)
        colored_resized_row = ensure_color(resized_row)
        colored_resized_rows.append(colored_resized_row)

    horizontally_stacked_rows = []
    for colored_resized_row in colored_resized_rows:
        # Stack images horizontally within the row
        horizontally_stacked_row = numpy.hstack(tup=colored_resized_row)
        horizontally_stacked_rows.append(horizontally_stacked_row)

    # Stack all rows vertically to form the final image
    vertically_stacked_image = numpy.vstack(tup=horizontally_stacked_rows)

    return vertically_stacked_image
