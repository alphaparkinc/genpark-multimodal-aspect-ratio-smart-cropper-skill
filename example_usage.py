from client import MultimodalAspectRatioSmartCropperClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    cropper = MultimodalAspectRatioSmartCropperClient()
    print("=== MULTIMODAL ASPECT RATIO SMART CROPPER ===")
    
    # 4K Landscape Photo (3840x2160) with primary subject at (1200, 1000)
    res = cropper.generate_all_crops(3840, 2160, focal_point_x=1200, focal_point_y=1000)
    print(f"Source Resolution: {res['image_resolution']}")
    print("Computed Optimal Crop Windows for All Standards:")
    print()
    for name, c in res['crops'].items():
        bbox = c['bounding_box']
        print(f"  [{name:>5}] Box: ({bbox['x_min']}, {bbox['y_min']}) to ({bbox['x_max']}, {bbox['y_max']}) | Size: {c['crop_dimensions']['width']}x{c['crop_dimensions']['height']} (Coverage: {c['area_coverage_pct']}%)")

if __name__ == "__main__":
    main()
