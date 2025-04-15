import cv2 as cv
import numpy as np

# Set the size of the chessboard (number of inner corners per row and column)
pattern_size = (7, 6)

# Prepare 3D real-world object points
objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Open the webcam
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

print("Press 'c' to capture chessboard image, 'q' to quit.")

captured = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('Calibration', frame)
    key = cv.waitKey(1)

    if key == ord('c'):
        found, corners = cv.findChessboardCorners(gray, pattern_size)
        if found:
            objpoints.append(objp)
            imgpoints.append(corners)
            captured += 1
            print(f"Captured image #{captured}")
            cv.drawChessboardCorners(frame, pattern_size, corners, found)
            cv.imshow('Corners', frame)
            cv.waitKey(500)
        else:
            print("Chessboard not found. Try again.")

    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

# Calibrate the camera
print("Starting calibration...")
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

# Save the calibration result
np.savez("camera_calibration_data.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
print("Calibration complete. Results saved to camera_calibration_data.npz")
print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)
