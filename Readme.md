# AR Cube Visualizer

An augmented reality application that detects a chessboard pattern and places a 3D cube on top of it using camera pose estimation.

## Description

This project uses OpenCV to detect a chessboard pattern in real-time through a webcam feed, estimates the camera pose relative to the chessboard, and renders a 3D cube on top of the pattern. The application leverages previously calibrated camera parameters to ensure accurate pose estimation and projection.

## Features

- Real-time camera pose estimation using chessboard pattern detection
- 3D cube visualization with different colored faces
- Uses camera calibration data from a previous calibration process

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

## How to Use

1. Make sure you have a `camera_calibration_data.npz` file that contains your camera's calibration data (camera matrix and distortion coefficients)
2. Run the script:
   ```
   python ar_cube_visualizer.py
   ```
3. Hold a 7×6 chessboard pattern in front of your camera
4. A colored 3D cube will appear on the chessboard when detected
5. Press ESC to exit the application

## Demo

![AR Cube Demo](Camera Pose Estimation and AR/Demo.png)

*The image above shows the AR cube being rendered on top of a detected chessboard pattern.*

## How It Works

1. **Camera Calibration Data Loading**: The script loads pre-computed camera calibration parameters from a `.npz` file.

2. **Chessboard Detection**: The application continuously captures frames from the webcam and searches for a 7×6 chessboard pattern.

3. **Pose Estimation**: When a chessboard is detected, the script uses the `cv.solvePnP()` function to determine the camera's position and orientation relative to the chessboard.

4. **3D Cube Rendering**: A virtual 3D cube is defined and projected onto the image plane using the estimated pose.

5. **Visualization**: The cube is drawn with colored edges (red for the bottom face, green for the top face, and blue for vertical edges).

## Technical Implementation

The camera pose estimation is performed using the Perspective-n-Point (PnP) algorithm implemented in OpenCV's `solvePnP()` function. The 3D coordinates of the chessboard corners are known, and when matched with their detected 2D image coordinates, the algorithm can determine the camera's position and orientation.

The 3D cube is then projected onto the 2D image plane using the estimated pose and the camera's intrinsic parameters (focal length, principal point, etc.) obtained from the calibration data.
