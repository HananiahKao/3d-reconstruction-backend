import cv2
import os
import uuid
import numpy as np
import open3d as o3d
import tempfile

def process_video_to_mesh(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_interval = 10
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)
        frame_count += 1

    cap.release()

    # Fake 3D point cloud: Use image gradients for pseudo-depth (for demo only)
    points = []
    for img in frames:
        grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        depth = np.sqrt(grad_x**2 + grad_y**2)
        for y in range(0, img.shape[0], 10):
            for x in range(0, img.shape[1], 10):
                points.append([x, y, depth[y, x]])

    points = np.array(points, dtype=np.float32)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(point_cloud, 0.5)

    temp_dir = tempfile.gettempdir()
    mesh_path = os.path.join(temp_dir, f"{uuid.uuid4()}.ply")
    o3d.io.write_triangle_mesh(mesh_path, mesh)
    return mesh_path
