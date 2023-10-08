import cv2
import numpy as np
import math
import random
from sklearn.cluster import KMeans

def hough_transform(image, threshold, rho_resolution, theta_resolution):
    # Get image dimensions
    height, width = image.shape

    # Define the maximum possible distance in the image
    max_distance = int(math.sqrt(height ** 2 + width ** 2))

    # Define the accumulator array
    accumulator = np.zeros((2 * max_distance, theta_resolution), dtype=np.uint8)

    # Iterate over the image
    for y in range(height):
        for x in range(width):
            # Check if the pixel is an edge
            if image[y, x] != 0:
                # Iterate over all possible theta values
                for t_idx in range(theta_resolution):
                    theta = t_idx * (np.pi / theta_resolution)

                    # Calculate rho
                    rho = int(x * np.cos(theta) + y * np.sin(theta))

                    # Increment the accumulator cell
                    accumulator[rho + max_distance, t_idx] += 1

    # Find the lines based on the accumulator values
    lines = []
    for rho_idx in range(accumulator.shape[0]):
        for t_idx in range(accumulator.shape[1]):
            if accumulator[rho_idx, t_idx] > threshold:
                rho = rho_idx - max_distance
                theta = t_idx * (np.pi / theta_resolution)
                lines.append((rho, theta))

    return lines


def draw_lines(image, lines):
    for rho, theta in lines:
        # Convert polar coordinates to Cartesian coordinates
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        # Find two points on the line to draw a line segment
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # Draw the line on the image
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


#yo probability ko laagi try
def hough_lines_p(coordinates, min_line_length, max_line_gap):
    lines = []

    # Convert the coordinates to NumPy array
    coordinates = np.array(coordinates)

    # Calculate the differences in x and y coordinates
    dx = coordinates[:, 1] - coordinates[:, 0] #eta 1 ko thau ma 2
    dy = coordinates[:, 1] - coordinates[:, 0] #eta 1 ko thau ma 3

    # Calculate the lengths of the lines
    lengths = np.sqrt(dx ** 2 + dy ** 2)

    # Calculate the angles of the lines
    angles = np.arctan2(dy, dx)

    # Iterate over the lines
    for i in range(len(coordinates)):
        # Check if the line length is greater than the minimum line length
        if lengths[i] >= min_line_length:
            # Check if the gap between lines is less than the maximum line gap
            if i < len(coordinates) - 1 and coordinates[i+1][0] - coordinates[i][1] <= max_line_gap: #eta 1 ko thau ma 2 thiyo
                # Merge the current line with the next line
                coordinates[i+1][2] = coordinates[i][2]
                coordinates[i+1][3] = coordinates[i][3]
            else:
                # Add the line to the output list
                lines.append(coordinates[i])

    return lines


# Load the input image
image = cv2.imread('circuitimg.jpg', 0)  # Read the image as grayscale

# Apply Canny edge detection
edges = cv2.Canny(image, 50, 150, apertureSize=3)

# Perform Hough Transform
threshold = 100  # Minimum number of votes to consider a line
rho_resolution = 1
theta_resolution = 180  # 180 degrees (pi radians)
lines = hough_transform(edges, threshold, rho_resolution, theta_resolution)

#probability ko laagi try
# Assuming you have 'lines' as the output of your Hough Transform
min_line_length = 50  # Minimum length of a line
max_line_gap = 10  # Maximum allowed gap between line segments to treat them as a single line

# Merge and filter the lines
merged_lines = hough_lines_p(lines, min_line_length, max_line_gap)

# Print the merged lines
for line in merged_lines:
    x1, y1 = line #x2,y2 pani thiyo
    print(f"Line: ({x1}, {y1}))") #-{x2},{y2} thiyo

# Find the line intersection points
intersection_points = []
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        rho1, theta1 = lines[i]
        rho2, theta2 = lines[j]

        # Convert to Cartesian coordinates
        a1 = np.cos(theta1)
        b1 = np.sin(theta1)
        c1 = -rho1
        a2 = np.cos(theta2)
        b2 = np.sin(theta2)
        c2 = -rho2

        # Calculate the intersection point
        d = a1 * b2 - a2 * b1
        if d != 0:
            x = (b1 * c2 - b2 * c1) / d
            y = (a2 * c1 - a1 * c2) / d
            intersection_points.append((x, y))

# Extract points from lines for clustering
line_points = np.array([(rho * np.cos(theta),rho*np.sin(theta)) for rho, theta in lines])

# perfrom k-mean clustering to spearate lines
kmeans = KMeans(n_clusters = 2, random_state = 0, n_init="auto").fit(line_points)
cluster_centers = kmeans.cluster_centers_


# Create a copy of the original image to draw the lines and intersection points on it
result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# draw the lines detected bye k-means clustering
for center in cluster_centers:
    rhos, thetas = cv2.cartToPolar(center[0], center[1])
    for rho, theta1 in zip(rhos, thetas):
        rho = int(rho)
        theta_degrees = int(np.degrees(theta1))
        cv2.line(result, (0,rho), (image.shape[1], rho),(0,0,255),2)



# Draw the detected lines on the original image
result = draw_lines(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), lines)

# Draw the intersection points
for x, y in intersection_points:
    cv2.circle(result, (int(x), int(y)), 5, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), random.randint(1,10))

# perform k-means clustering to groupd intersection points
intersection_points_array = np.array(intersection_points)
kmeans = k=KMeans(n_clusters=4, random_state= 0).fit(intersection_points_array)
intersection_centers = kmeans.cluster_centers_


# draw the intersection points detected by k-means clustering
for center in intersection_centers:
    x, y = center
    cv2.circle(result, (int(x), int(y)), 5, (255,0,0), -1)

# Display the result
cv2.imshow('Lines Detected', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
