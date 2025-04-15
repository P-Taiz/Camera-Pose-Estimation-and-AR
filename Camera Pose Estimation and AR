import cv2 as cv
import numpy as np

# Load calibration results from .npz
with np.load("camera_calibration_data.npz") as data:
    camera_matrix = data["camera_matrix"]
    dist_coeffs = data["dist_coeffs"]

# Chessboard size (number of inner corners)
pattern_size = (7, 6)

# Prepare object points (0,0,0), (1,0,0), ... (6,5,0)
objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

# Start webcam
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    found, corners = cv.findChessboardCorners(gray, pattern_size)

    if found:
        # Refine corners
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                   (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001))

        # Solve for pose (R, t)
        ret, rvec, tvec = cv.solvePnP(objp, corners2, camera_matrix, dist_coeffs)

        # Draw chessboard corners
        cv.drawChessboardCorners(frame, pattern_size, corners2, found)

        # Define 3D cube points
        cube_points = np.float32([
            [0, 0, 0], [0, 4, 0], [4, 4, 0], [4, 0, 0],  # bottom
            [0, 0, -4], [0, 4, -4], [4, 4, -4], [4, 0, -4]  # top
        ])

        # Project 3D points to 2D image plane
        imgpts, _ = cv.projectPoints(cube_points, rvec, tvec, camera_matrix, dist_coeffs)
        imgpts = np.int32(imgpts).reshape(-1, 2)

        # Draw cube
        # Bottom square
        frame = cv.drawContours(frame, [imgpts[:4]], -1, (0, 0, 255), 3)
        # Top square
        frame = cv.drawContours(frame, [imgpts[4:]], -1, (0, 255, 0), 3)
        # Vertical edges
        for i in range(4):
            frame = cv.line(frame, tuple(imgpts[i]), tuple(imgpts[i + 4]), (255, 0, 0), 2)

    # Show result
    cv.imshow("AR Cube", frame)
    key = cv.waitKey(1)
    if key == 27:  # ESC key to exit
        break

cap.release()
cv.destroyAllWindows()
