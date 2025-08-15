import cv2
import numpy as np
from stack import stack_images


# Initialize ORB feature detector with 1000 features
orb = cv2.ORB.create(nfeatures=1000)

# Initialize Brute-Force Matcher
bf = cv2.BFMatcher.create()

# Initialize webcam capture
webcam = cv2.VideoCapture(0)

# Load video file
video = cv2.VideoCapture("video.mp4")

# Flag to choose between webcam or placeholder image
use_webcam = False

# Counter for video frames
frame_count = 0

# Load the reference image for AR detection
known_image = cv2.imread(filename="cards.png")

# Get dimensions of the reference image
image_height, image_width, no_channels = known_image.shape

# Detect keypoints and compute descriptors for the reference image
kp1, desc1 = orb.detectAndCompute(image=known_image, mask=None)

# Main loop
while True:
    # Capture frame from webcam if enabled, otherwise use placeholder image
    if use_webcam:
        is_successful, webcam_frame = webcam.read()
    else:
        webcam_frame = cv2.imread(filename="webcam_frame.jpg")

    # Detect keypoints and compute descriptors for the current frame
    kp2, desc2 = orb.detectAndCompute(image=webcam_frame, mask=None)

    # Make copies of the current frame for drawing and output
    webcam_frame_copy = webcam_frame.copy()
    output_frame2 = webcam_frame.copy()

    # Reset video if we reached the end
    if frame_count == video.get(propId=cv2.CAP_PROP_FRAME_COUNT):
        video.set(propId=cv2.CAP_PROP_POS_FRAMES, value=0)
        frame_count = 0

    try:
        # Match features between reference image and current frame
        matches = bf.knnMatch(queryDescriptors=desc1, trainDescriptors=desc2, k=2)

        # Filter good matches using Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if (m.distance / n.distance) < 0.75:
                good_matches.append(m)

        print(len(good_matches))  # Debug: print number of good matches

        # Draw matches between reference and current frame
        matches_image = cv2.drawMatches(
            img1=known_image,
            keypoints1=kp1,
            img2=webcam_frame,
            keypoints2=kp2,
            matches1to2=good_matches,
            outImg=None,
            flags=2,
        )

        # If enough good matches are found, overlay the video onto the frame
        if len(good_matches) > 20:

            # Read next frame from the video
            is_successful, video_frame = video.read()

            # Resize video frame to match reference image
            video_frame = cv2.resize(src=video_frame, dsize=(image_width, image_height))
            frame_count += 1

            # Get coordinates of matched keypoints
            src_points = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(
                -1, 1, 2
            )
            dst_points = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(
                -1, 1, 2
            )

            # Compute homography matrix
            matrix, _ = cv2.findHomography(
                srcPoints=src_points,
                dstPoints=dst_points,
                method=cv2.RANSAC,
                ransacReprojThreshold=5,
            )

            # Define corners of reference image
            points1 = np.float32(
                [
                    [0, 0],
                    [0, image_height],
                    [image_width, image_height],
                    [image_width, 0],
                ]
            ).reshape(-1, 1, 2)

            # Transform corners to current frame using homography
            points2 = cv2.perspectiveTransform(src=points1, m=matrix)

            # Draw polygon around detected area
            cv2.polylines(
                img=webcam_frame_copy,
                pts=[np.int32(points2)],
                isClosed=True,
                color=(255, 0, 255),
                thickness=4,
            )

            # Warp video frame to fit detected area
            warped_video_frame = cv2.warpPerspective(
                src=video_frame,
                M=matrix,
                dsize=(webcam_frame.shape[1], webcam_frame.shape[0]),
            )

            # Create mask for overlay
            mask = np.zeros(
                shape=(webcam_frame.shape[0], webcam_frame.shape[1]), dtype=np.uint8
            )
            cv2.fillPoly(img=mask, pts=[np.int32(points2)], color=(255, 255, 255))
            mask = cv2.bitwise_not(src=mask)

            # Apply mask to original frame
            output_frame1 = cv2.bitwise_and(
                src1=webcam_frame, src2=webcam_frame, mask=mask
            )

            # Combine masked frame and warped video
            output_frame2 = cv2.bitwise_or(src1=output_frame1, src2=warped_video_frame)

            # Stack images for debugging and visualization
            stacked_images = stack_images(
                rows=[
                    [known_image, webcam_frame, matches_image],
                    [webcam_frame_copy, video_frame, warped_video_frame],
                    [mask, output_frame1, output_frame2],
                ],
                new_size=(200, 150),
            )

            cv2.imshow(winname="stacked images", mat=stacked_images)

    except:
        # Skip frame if matching or homography fails
        pass

    # Show final output frame
    cv2.imshow(winname="output frame 2", mat=output_frame2)

    # Exit loop on ESC key
    key = cv2.waitKey(delay=1)
    if key == 27:
        break

# Release resources
webcam.release()
video.release()
cv2.destroyAllWindows()
