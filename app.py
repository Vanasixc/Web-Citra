from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import io
from PIL import Image
from skimage.morphology import skeletonize, thin, remove_small_objects # untuk morfologi lanjutan
from scipy.ndimage import binary_fill_holes # untuk region filling

app = Flask(__name__)

def get_binary_image(gray_image):
    """Helper function to convert grayscale to binary using Otsu's thresholding."""
    _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def process_image(image, method='original', params=None):
    if len(image.shape) == 3 and image.shape[2] == 3: # Check if it's a color image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 3 and image.shape[2] == 4: # Check if it's a color image with alpha
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        gray = image # Already grayscale
        
    result = None
    
    if params is None:
        params = {}
    
    if method == 'original':
        result = image # Return original color image if it was color
        if len(image.shape) == 2 : # If original was grayscale, ensure result is also grayscale for consistency
             result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


    # Threshold methods - Task 1
    elif method == 'threshold':
        threshold_value = params.get('threshold_value', 127)
        _, result_gray = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR) # Convert to BGR for display consistency
    
    # Edge detection methods - Task 2
    elif method == 'sobel':
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobelx_abs = np.uint8(np.absolute(sobelx))
        sobely_abs = np.uint8(np.absolute(sobely))
        result_gray = cv2.bitwise_or(sobelx_abs, sobely_abs)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)
    elif method == 'prewitt':
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        img_prewittx = cv2.filter2D(gray, -1, kernelx)
        img_prewitty = cv2.filter2D(gray, -1, kernely)
        result_gray = cv2.bitwise_or(img_prewittx, img_prewitty)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)
    elif method == 'roberts':
        roberts_cross_v = np.array([[1, 0], [0, -1]], dtype=np.float32)
        roberts_cross_h = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        # Apply filter, ensure output is also float for potential negative values before abs
        vertical_f = cv2.filter2D(gray.astype(np.float32), -1, roberts_cross_v)
        horizontal_f = cv2.filter2D(gray.astype(np.float32), -1, roberts_cross_h)
        # Convert to unsigned 8-bit after taking absolute
        vertical = np.uint8(np.absolute(vertical_f))
        horizontal = np.uint8(np.absolute(horizontal_f))
        result_gray = cv2.bitwise_or(vertical, horizontal)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)
    elif method == 'canny':
        result_gray = cv2.Canny(gray, 100, 200)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)
    
    # Morphological operations - Task 3
    elif method == 'erosion' or method == 'dilation':
        kernel_shape_str = params.get('kernel_shape', 'rect')
        kernel_size = params.get('kernel_size', 3)
        
        shape_map = {
            'rect': cv2.MORPH_RECT,
            'ellipse': cv2.MORPH_ELLIPSE,
            'cross': cv2.MORPH_CROSS
        }
        cv_kernel_shape = shape_map.get(kernel_shape_str, cv2.MORPH_RECT)
        kernel = cv2.getStructuringElement(cv_kernel_shape, (kernel_size, kernel_size))
        
        # Binarize the image first for morphology
        binary_img = get_binary_image(gray)

        if method == 'erosion':
            result_gray = cv2.erode(binary_img, kernel, iterations=1)
        else:  # dilation
            result_gray = cv2.dilate(binary_img, kernel, iterations=1)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    # Advanced Morphological Operations - Task 4
    elif method == 'boundary':
        binary_img = get_binary_image(gray)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        eroded_img = cv2.erode(binary_img, kernel, iterations=1)
        result_gray = binary_img - eroded_img
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    elif method == 'skeletonize':
        binary_img = get_binary_image(gray)
        # skimage.skeletonize expects boolean or 0/1 image
        skeleton = skeletonize(binary_img // 255) 
        result_gray = (skeleton * 255).astype(np.uint8)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    elif method == 'thickening':
        # Thickening can be complex. A common approach is to thin the inverted image.
        binary_img = get_binary_image(gray)
        inverted_binary_img = cv2.bitwise_not(binary_img)
        thinned_inverted = thin(inverted_binary_img // 255) # skimage.thin expects boolean or 0/1
        thickened_img = cv2.bitwise_not((thinned_inverted * 255).astype(np.uint8))
        result_gray = thickened_img
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    elif method == 'region_filling':
        binary_img = get_binary_image(gray)
        # scipy.ndimage.binary_fill_holes expects boolean array
        filled_img = binary_fill_holes(binary_img // 255)
        result_gray = (filled_img * 255).astype(np.uint8)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    elif method == 'convex_hull':
        binary_img = get_binary_image(gray)
        contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hull_img = np.zeros_like(binary_img) # Create a black image to draw hulls
        for contour in contours:
            hull = cv2.convexHull(contour)
            cv2.drawContours(hull_img, [hull], -1, (255), thickness=cv2.FILLED)
        result_gray = hull_img
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)
    
    elif method == 'pruning': # Using 'pruning' as method name from HTML
        # Pruning is often applied to skeletons.
        # First, get the skeleton
        binary_img_for_skeleton = get_binary_image(gray)
        skeleton = skeletonize(binary_img_for_skeleton // 255)
        # remove_small_objects can act as a form of pruning by removing small branches/components
        # Adjust min_size as needed. This is a simple form of pruning.
        pruned_skeleton = remove_small_objects(skeleton, min_size=10, connectivity=1)
        result_gray = (pruned_skeleton * 255).astype(np.uint8)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    elif method == 'thinning':
        binary_img = get_binary_image(gray)
        # skimage.thin expects boolean or 0/1 image
        thinned_img = thin(binary_img // 255)
        result_gray = (thinned_img * 255).astype(np.uint8)
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

    # Ensure result is not None, default to original gray if something went wrong
    if result is None:
        result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) # Convert original gray to BGR

    return result

def convert_image_to_base64(image_array):
    # Ensure the image is in BGR format for cv2.imencode
    # If it's grayscale, convert it. If it's already BGR, this won't change it.
    # If it's BGRA, imencode should handle it or convert to BGR first.
    if len(image_array.shape) == 2: # Grayscale
        img_to_encode = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
    elif len(image_array.shape) == 3 and image_array.shape[2] == 4: # BGRA
        img_to_encode = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)
    else: # Already BGR or other 3-channel format imencode can handle
        img_to_encode = image_array

    is_success, buffer = cv2.imencode(".png", img_to_encode)
    if not is_success:
        # Fallback for safety, though unlikely with PNG
        gray_fallback = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY) if len(image_array.shape) > 2 else image_array
        is_success, buffer = cv2.imencode(".png", gray_fallback)

    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_route(): # Renamed from 'process' to avoid conflict with any potential global 'process' variable
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'})
    
    try:
        img_pil = Image.open(file.stream)
        # Convert PIL Image to OpenCV format (NumPy array)
        # Handle different modes (e.g., RGBA, RGB, L)
        if img_pil.mode == 'RGBA':
            img_array_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGRA)
        elif img_pil.mode == 'RGB':
            img_array_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        elif img_pil.mode == 'L': # Grayscale
            img_array_cv = np.array(img_pil) # Already grayscale
            # process_image expects BGR or Grayscale, if original is L, convert to BGR for display consistency
            # img_array_cv = cv2.cvtColor(img_array_cv, cv2.COLOR_GRAY2BGR)
        else: # For other modes, try converting to RGB first
            img_pil = img_pil.convert('RGB')
            img_array_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    except Exception as e:
        return jsonify({'error': f'Could not read image: {str(e)}'})

    method = request.form.get('method', 'original')
    
    params = {}
    
    if method == 'threshold':
        threshold_value = request.form.get('threshold_value')
        if threshold_value:
            params['threshold_value'] = int(threshold_value)
    
    elif method in ['erosion', 'dilation']:
        kernel_shape = request.form.get('kernel_shape')
        kernel_size = request.form.get('kernel_size')
        
        if kernel_shape:
            params['kernel_shape'] = kernel_shape
        if kernel_size:
            params['kernel_size'] = int(kernel_size)
    
    # No specific params needed from frontend for advanced morphology yet
    
    processed_img_cv = process_image(img_array_cv.copy(), method, params) # Use .copy() to avoid modifying original
    
    # For original image display, ensure it's in a consistent format (BGR) for convert_image_to_base64
    if len(img_array_cv.shape) == 2: # If original was grayscale
        original_display_img = cv2.cvtColor(img_array_cv, cv2.COLOR_GRAY2BGR)
    elif img_array_cv.shape[2] == 4: # If original was BGRA
         original_display_img = cv2.cvtColor(img_array_cv, cv2.COLOR_BGRA2BGR)
    else: # Already BGR
        original_display_img = img_array_cv

    original_b64 = convert_image_to_base64(original_display_img)
    processed_b64 = convert_image_to_base64(processed_img_cv)
    
    return jsonify({
        'original': original_b64,
        'processed': processed_b64,
        'method': method
    })

if __name__ == '__main__':
    app.run(debug=True)
