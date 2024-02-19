import os
import cv2


def detect_and_match(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Initialize FLANN matcher
    flann = cv2.FlannBasedMatcher()

    # Perform KNN matching
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Filter matches using ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Calculate percentage similarity
    similarity_percentage = len(good_matches) / min(len(keypoints1), len(keypoints2)) * 100

    return similarity_percentage


def find_similar_images(search_path, image_path):
    similar_images = []
    image_to_compare = cv2.imread(image_path)

    for filename in os.listdir(search_path):
        if filename.endswith(".jpg"):
            image = cv2.imread(os.path.join(search_path, filename))
            similarity_percentage = detect_and_match(image, image_to_compare)
            if similarity_percentage == 100:
                similar_images.append(filename)

    if search_path in image_path:
        image = image_path.split("/")[-1]
        similar_images.remove(image)
    return similar_images


if __name__ == "__main__":
    search_path = "/home/sadna/work/hiren_sir/image_matcher/"
    image_path = "/home/sadna/work/hiren_sir/image_matcher/mydog.jpg"
    similar_images = find_similar_images(search_path, image_path)

    if similar_images:
        print("Images with 100% similarity in", search_path, "with", image_path, ":")

        for img in similar_images:
            print(img)
    else:
        print("No images with 100% similarity found.")
