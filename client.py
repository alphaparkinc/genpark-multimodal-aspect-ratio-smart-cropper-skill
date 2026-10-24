import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class MultimodalAspectRatioSmartCropperClient:
    """
    Computes optimal crop bounding boxes for target aspect ratios (16:9, 1:1, 4:5, 9:16)
    anchored on focal saliency centroids to preserve core visual objects without distortion.
    """
    def __init__(self):
        self.standard_ratios = {
            "16:9": 16.0 / 9.0,
            "1:1":  1.0,
            "4:5":  4.0 / 5.0,
            "9:16": 9.0 / 16.0
        }

    def compute_smart_crop(self, orig_width, orig_height, focal_point_x=None, focal_point_y=None, target_ratio_name="1:1"):
        ratio = self.standard_ratios.get(target_ratio_name, 1.0)
        
        # Default focal point to visual center if not specified
        cx = focal_point_x if focal_point_x is not None else (orig_width / 2.0)
        cy = focal_point_y if focal_point_y is not None else (orig_height / 2.0)

        current_ratio = orig_width / float(orig_height)

        if current_ratio > ratio:
            # Source image is wider than target: fit height, crop width
            crop_h = orig_height
            crop_w = int(orig_height * ratio)
        else:
            # Source image is taller than target: fit width, crop height
            crop_w = orig_width
            crop_h = int(orig_width / ratio)

        # Center crop window around focal point (cx, cy)
        x_min = int(max(0, min(orig_width - crop_w, cx - (crop_w / 2.0))))
        y_min = int(max(0, min(orig_height - crop_h, cy - (crop_h / 2.0))))
        x_max = x_min + crop_w
        y_max = y_min + crop_h

        # Coverage percentage of original image
        area_coverage = (crop_w * crop_h) / float(orig_width * orig_height) * 100.0

        return {
            "target_aspect_ratio": target_ratio_name,
            "crop_dimensions": {"width": crop_w, "height": crop_h},
            "bounding_box": {"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max},
            "original_dimensions": {"width": orig_width, "height": orig_height},
            "focal_anchor": {"x": int(cx), "y": int(cy)},
            "area_coverage_pct": round(area_coverage, 2)
        }

    def generate_all_crops(self, orig_width, orig_height, focal_point_x=None, focal_point_y=None):
        crops = {}
        for r_name in self.standard_ratios:
            crops[r_name] = self.compute_smart_crop(orig_width, orig_height, focal_point_x, focal_point_y, r_name)
        return {
            "status": "success",
            "image_resolution": f"{orig_width}x{orig_height}",
            "crops": crops
        }
