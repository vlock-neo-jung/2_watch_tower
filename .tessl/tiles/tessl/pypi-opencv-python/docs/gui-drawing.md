# GUI and Drawing

OpenCV provides high-level GUI capabilities for displaying images, creating interactive windows, and drawing shapes on images. These features are essential for debugging, visualization, and creating interactive computer vision applications.

**Important Note**: GUI functions are not available in headless packages (`opencv-python-headless`). If you're running OpenCV in a server environment or headless system, these functions will not work. Use the standard `opencv-python` package if you need GUI functionality.

## Capabilities

### Window Management

OpenCV provides a complete set of functions for creating and managing display windows.

```python { .api }
# Display image in a window
cv2.imshow(winname, mat) -> None
```

Shows an image in the specified window. If the window doesn't exist, it will be created with `WINDOW_AUTOSIZE` flag. The window will automatically fit the image size.

**Parameters**:
- `winname` (str): Name of the window
- `mat` (np.ndarray): Image to display

**Example**:
```python
import cv2
import numpy as np

img = cv2.imread('image.jpg')
cv2.imshow('My Image', img)
cv2.waitKey(0)  # Wait for key press
cv2.destroyAllWindows()
```

---

```python { .api }
# Create a named window
cv2.namedWindow(winname, flags=cv2.WINDOW_AUTOSIZE) -> None
```

Creates a window that can be used as a placeholder for images and trackbars. Created windows are referred to by their names.

**Parameters**:
- `winname` (str): Name of the window
- `flags` (int): Window flags (see Window Flags section)

**Example**:
```python
# Create a resizable window
cv2.namedWindow('My Window', cv2.WINDOW_NORMAL)
cv2.imshow('My Window', img)
```

---

```python { .api }
# Destroy specific window
cv2.destroyWindow(winname) -> None
```

Destroys the specified window.

**Parameters**:
- `winname` (str): Name of the window to destroy

---

```python { .api }
# Destroy all windows
cv2.destroyAllWindows() -> None
```

Destroys all HighGUI windows. Should be called at the end of GUI applications.

---

```python { .api }
# Wait for key press
cv2.waitKey(delay=0) -> int
```

Waits for a key press for a specified number of milliseconds. This function is essential for GUI event processing.

**Parameters**:
- `delay` (int): Delay in milliseconds. 0 means wait indefinitely

**Returns**:
- Key code of the pressed key, or -1 if no key was pressed

**Example**:
```python
# Wait indefinitely for key press
key = cv2.waitKey(0)
if key == ord('q'):
    print("Q was pressed")
elif key == 27:  # ESC key
    print("ESC was pressed")

# Wait 30ms (useful for video playback)
key = cv2.waitKey(30)
```

---

```python { .api }
# Poll for key press (non-blocking)
cv2.pollKey() -> int
```

Polls for a key press without blocking. Similar to `waitKey(0)` but non-blocking.

**Returns**:
- Key code of the pressed key, or -1 if no key was pressed

---

```python { .api }
# Resize window
cv2.resizeWindow(winname, width, height) -> None
```

Resizes the window to the specified size. The window must have been created with `WINDOW_NORMAL` flag.

**Parameters**:
- `winname` (str): Name of the window
- `width` (int): New window width
- `height` (int): New window height

---

```python { .api }
# Move window
cv2.moveWindow(winname, x, y) -> None
```

Moves the window to the specified position.

**Parameters**:
- `winname` (str): Name of the window
- `x` (int): New x-coordinate of the top-left corner
- `y` (int): New y-coordinate of the top-left corner

---

```python { .api }
# Get window property
cv2.getWindowProperty(winname, prop_id) -> float
```

Gets a property of the window.

**Parameters**:
- `winname` (str): Name of the window
- `prop_id` (int): Property identifier

**Returns**:
- Property value

---

```python { .api }
# Set window property
cv2.setWindowProperty(winname, prop_id, prop_value) -> None
```

Sets a property of the window.

**Parameters**:
- `winname` (str): Name of the window
- `prop_id` (int): Property identifier
- `prop_value` (float): New property value

---

```python { .api }
# Set window title
cv2.setWindowTitle(winname, title) -> None
```

Updates the window title.

**Parameters**:
- `winname` (str): Name of the window
- `title` (str): New window title

---

#### Window Flags

Constants for window creation:

```python { .api }
cv2.WINDOW_NORMAL      # User can resize the window
cv2.WINDOW_AUTOSIZE    # Window size automatically adjusted to fit image
cv2.WINDOW_FULLSCREEN  # Window is in fullscreen mode
cv2.WINDOW_FREERATIO   # Window can be resized without maintaining aspect ratio
cv2.WINDOW_KEEPRATIO   # Window maintains aspect ratio when resized
cv2.WINDOW_GUI_EXPANDED # Window with extended GUI features
cv2.WINDOW_GUI_NORMAL   # Window with basic GUI features
```

### Trackbars

Trackbars provide an interactive way to adjust parameters in real-time. They are useful for tuning algorithms and exploring parameter spaces.

```python { .api }
# Create trackbar
cv2.createTrackbar(trackbarname, winname, value, count, onChange) -> None
```

Creates a trackbar and attaches it to the specified window.

**Parameters**:
- `trackbarname` (str): Name of the trackbar
- `winname` (str): Name of the window that will be the parent of the trackbar
- `value` (int): Initial trackbar position
- `count` (int): Maximum trackbar position (minimum is always 0)
- `onChange` (callable): Callback function called when trackbar value changes. Signature: `onChange(value: int) -> None`

**Example**:
```python
def on_threshold_change(value):
    _, thresh = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    cv2.imshow('Threshold', thresh)

cv2.namedWindow('Threshold')
cv2.createTrackbar('Threshold', 'Threshold', 127, 255, on_threshold_change)
```

---

```python { .api }
# Get trackbar position
cv2.getTrackbarPos(trackbarname, winname) -> int
```

Gets the current position of the trackbar.

**Parameters**:
- `trackbarname` (str): Name of the trackbar
- `winname` (str): Name of the parent window

**Returns**:
- Current trackbar position

---

```python { .api }
# Set trackbar position
cv2.setTrackbarPos(trackbarname, winname, pos) -> None
```

Sets the trackbar position.

**Parameters**:
- `trackbarname` (str): Name of the trackbar
- `winname` (str): Name of the parent window
- `pos` (int): New trackbar position

---

```python { .api }
# Set trackbar minimum value
cv2.setTrackbarMin(trackbarname, winname, minval) -> None
```

Sets the minimum value of the trackbar.

**Parameters**:
- `trackbarname` (str): Name of the trackbar
- `winname` (str): Name of the parent window
- `minval` (int): New minimum value

---

```python { .api }
# Set trackbar maximum value
cv2.setTrackbarMax(trackbarname, winname, maxval) -> None
```

Sets the maximum value of the trackbar.

**Parameters**:
- `trackbarname` (str): Name of the trackbar
- `winname` (str): Name of the parent window
- `maxval` (int): New maximum value

**Example - Multiple Trackbars**:
```python
import cv2
import numpy as np

def nothing(x):
    pass

# Create window and trackbars
cv2.namedWindow('Color Picker')
cv2.createTrackbar('R', 'Color Picker', 0, 255, nothing)
cv2.createTrackbar('G', 'Color Picker', 0, 255, nothing)
cv2.createTrackbar('B', 'Color Picker', 0, 255, nothing)

while True:
    # Get current trackbar positions
    r = cv2.getTrackbarPos('R', 'Color Picker')
    g = cv2.getTrackbarPos('G', 'Color Picker')
    b = cv2.getTrackbarPos('B', 'Color Picker')

    # Create image with selected color
    img = np.zeros((300, 512, 3), np.uint8)
    img[:] = [b, g, r]

    cv2.imshow('Color Picker', img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
```

### Mouse Events

OpenCV allows you to capture and handle mouse events in windows, enabling interactive applications.

```python { .api }
# Set mouse callback function
cv2.setMouseCallback(windowName, onMouse, param=None) -> None
```

Sets a mouse event callback function for the specified window.

**Parameters**:
- `windowName` (str): Name of the window
- `onMouse` (callable): Callback function with signature: `onMouse(event, x, y, flags, param)`
  - `event` (int): Mouse event type (see Mouse Event Constants)
  - `x` (int): X-coordinate of the mouse event
  - `y` (int): Y-coordinate of the mouse event
  - `flags` (int): Event flags (see Mouse Event Flags)
  - `param`: User data passed to the callback
- `param`: Optional user data to pass to the callback

**Example**:
```python
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left button clicked at ({x}, {y})")
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print(f"Drawing at ({x}, {y})")
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(f"Right button clicked at ({x}, {y})")

img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('Mouse Events')
cv2.setMouseCallback('Mouse Events', mouse_callback)

while True:
    cv2.imshow('Mouse Events', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

---

#### Mouse Event Constants

Constants representing different mouse events:

```python { .api }
cv2.EVENT_MOUSEMOVE      # Mouse moved
cv2.EVENT_LBUTTONDOWN    # Left button pressed
cv2.EVENT_RBUTTONDOWN    # Right button pressed
cv2.EVENT_MBUTTONDOWN    # Middle button pressed
cv2.EVENT_LBUTTONUP      # Left button released
cv2.EVENT_RBUTTONUP      # Right button released
cv2.EVENT_MBUTTONUP      # Middle button released
cv2.EVENT_LBUTTONDBLCLK  # Left button double-clicked
cv2.EVENT_RBUTTONDBLCLK  # Right button double-clicked
cv2.EVENT_MBUTTONDBLCLK  # Middle button double-clicked
cv2.EVENT_MOUSEWHEEL     # Mouse wheel scrolled (vertical)
cv2.EVENT_MOUSEHWHEEL    # Mouse wheel scrolled (horizontal)
```

---

#### Mouse Event Flags

Constants representing modifier keys and button states during mouse events:

```python { .api }
cv2.EVENT_FLAG_LBUTTON   # Left button is pressed
cv2.EVENT_FLAG_RBUTTON   # Right button is pressed
cv2.EVENT_FLAG_MBUTTON   # Middle button is pressed
cv2.EVENT_FLAG_CTRLKEY   # Ctrl key is pressed
cv2.EVENT_FLAG_SHIFTKEY  # Shift key is pressed
cv2.EVENT_FLAG_ALTKEY    # Alt key is pressed
```

**Example - Drawing Application**:
```python
import cv2
import numpy as np

drawing = False  # True if mouse is pressed
mode = True      # True for rectangle, False for circle
ix, iy = -1, -1

def draw_shape(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('Drawing')
cv2.setMouseCallback('Drawing', draw_shape)

while True:
    cv2.imshow('Drawing', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode  # Toggle mode
    elif k == 27:
        break

cv2.destroyAllWindows()
```

### ROI Selection

OpenCV provides built-in functions for selecting regions of interest interactively.

```python { .api }
# Select single ROI
cv2.selectROI(windowName, img, showCrosshair=True, fromCenter=False) -> tuple
```

Allows the user to select a region of interest in the image.

**Parameters**:
- `windowName` (str): Name of the window where selection is performed
- `img` (np.ndarray): Image to select ROI from
- `showCrosshair` (bool): If True, show crosshair in the center of selection
- `fromCenter` (bool): If True, selection starts from center

**Returns**:
- Tuple `(x, y, w, h)` representing the selected rectangle, or `(0, 0, 0, 0)` if cancelled

**Controls**:
- Click and drag to select ROI
- Press SPACE or ENTER to confirm selection
- Press C to cancel

**Example**:
```python
import cv2

img = cv2.imread('image.jpg')
roi = cv2.selectROI('Select ROI', img, showCrosshair=True)
x, y, w, h = roi

if w > 0 and h > 0:
    # Crop selected region
    cropped = img[y:y+h, x:x+w]
    cv2.imshow('Cropped', cropped)
    cv2.waitKey(0)

cv2.destroyAllWindows()
```

---

```python { .api }
# Select multiple ROIs
cv2.selectROIs(windowName, img, showCrosshair=True, fromCenter=False) -> tuple
```

Allows the user to select multiple regions of interest in the image.

**Parameters**:
- `windowName` (str): Name of the window where selection is performed
- `img` (np.ndarray): Image to select ROIs from
- `showCrosshair` (bool): If True, show crosshair in the center of selection
- `fromCenter` (bool): If True, selection starts from center

**Returns**:
- Tuple of rectangles, each in format `(x, y, w, h)`

**Controls**:
- Click and drag to select each ROI
- Press SPACE or ENTER after each selection
- Press ESC to finish selecting

**Example**:
```python
import cv2

img = cv2.imread('image.jpg')
rois = cv2.selectROIs('Select Multiple ROIs', img, showCrosshair=True)

# Process each selected ROI
for i, roi in enumerate(rois):
    x, y, w, h = roi
    if w > 0 and h > 0:
        cropped = img[y:y+h, x:x+w]
        cv2.imshow(f'ROI {i+1}', cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Drawing Functions

OpenCV provides comprehensive drawing functions for visualizing results and creating graphics.

```python { .api }
# Draw line
cv2.line(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```

Draws a line segment connecting two points.

**Parameters**:
- `img` (np.ndarray): Image to draw on (modified in-place)
- `pt1` (tuple): First point (x, y)
- `pt2` (tuple): Second point (x, y)
- `color` (tuple): Line color (B, G, R) for color images or intensity for grayscale
- `thickness` (int): Line thickness in pixels
- `lineType` (int): Line type (see Line Types)
- `shift` (int): Number of fractional bits in point coordinates

**Returns**:
- Modified image

**Example**:
```python
import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
# Draw red line from (0,0) to (511,511)
cv2.line(img, (0, 0), (511, 511), (0, 0, 255), 5)
```

---

```python { .api }
# Draw arrowed line
cv2.arrowedLine(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0, tipLength=0.1) -> img
```

Draws an arrow segment pointing from the first point to the second.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `pt1` (tuple): Starting point (x, y)
- `pt2` (tuple): End point (x, y) - arrow points here
- `color` (tuple): Line color
- `thickness` (int): Line thickness
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits
- `tipLength` (float): Length of arrow tip relative to arrow length

**Example**:
```python
cv2.arrowedLine(img, (50, 50), (200, 200), (255, 0, 0), 3, tipLength=0.3)
```

---

```python { .api }
# Draw rectangle
cv2.rectangle(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```

Draws a rectangle.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `pt1` (tuple): Top-left corner (x, y)
- `pt2` (tuple): Bottom-right corner (x, y)
- `color` (tuple): Rectangle color
- `thickness` (int): Line thickness. Use -1 for filled rectangle
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits

**Alternative signature**:
```python
cv2.rectangle(img, rec, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```
Where `rec` is a tuple `(x, y, w, h)`.

**Example**:
```python
# Outline rectangle
cv2.rectangle(img, (50, 50), (200, 200), (0, 255, 0), 3)

# Filled rectangle
cv2.rectangle(img, (250, 50), (400, 200), (255, 0, 0), -1)
```

---

```python { .api }
# Draw circle
cv2.circle(img, center, radius, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```

Draws a circle.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `center` (tuple): Center of the circle (x, y)
- `radius` (int): Radius of the circle
- `color` (tuple): Circle color
- `thickness` (int): Circle outline thickness. Use -1 for filled circle
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits

**Example**:
```python
# Outline circle
cv2.circle(img, (256, 256), 50, (0, 255, 255), 2)

# Filled circle
cv2.circle(img, (400, 400), 30, (255, 255, 0), -1)
```

---

```python { .api }
# Draw ellipse
cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```

Draws an ellipse or elliptic arc.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `center` (tuple): Center of the ellipse (x, y)
- `axes` (tuple): Half of the size of the ellipse main axes (width, height)
- `angle` (float): Ellipse rotation angle in degrees
- `startAngle` (float): Starting angle of the elliptic arc in degrees
- `endAngle` (float): Ending angle of the elliptic arc in degrees
- `color` (tuple): Ellipse color
- `thickness` (int): Line thickness. Use -1 for filled ellipse
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits

**Alternative signature using RotatedRect**:
```python
cv2.ellipse(img, box, color, thickness=1, lineType=cv2.LINE_8) -> img
```

**Example**:
```python
# Full ellipse
cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 360, (255, 0, 255), 2)

# Elliptic arc (quarter circle)
cv2.ellipse(img, (256, 256), (100, 50), 45, 0, 90, (0, 255, 0), 3)

# Filled ellipse
cv2.ellipse(img, (400, 100), (80, 40), 30, 0, 360, (128, 128, 255), -1)
```

---

```python { .api }
# Draw polylines
cv2.polylines(img, pts, isClosed, color, thickness=1, lineType=cv2.LINE_8, shift=0) -> img
```

Draws one or more polygonal curves.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `pts` (list): Array of polygonal curves. Each curve is represented by an array of points
- `isClosed` (bool): If True, draw closed polylines (connect last point to first)
- `color` (tuple): Polyline color
- `thickness` (int): Line thickness
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits

**Example**:
```python
import numpy as np

# Triangle
pts = np.array([[100, 50], [50, 150], [150, 150]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], True, (0, 255, 0), 3)

# Multiple polylines
pts1 = np.array([[200, 200], [250, 250], [300, 200]], np.int32).reshape((-1, 1, 2))
pts2 = np.array([[350, 200], [400, 250], [450, 200]], np.int32).reshape((-1, 1, 2))
cv2.polylines(img, [pts1, pts2], False, (255, 255, 0), 2)
```

---

```python { .api }
# Fill polygon
cv2.fillPoly(img, pts, color, lineType=cv2.LINE_8, shift=0, offset=(0, 0)) -> img
```

Fills the area bounded by one or more polygons.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `pts` (list): Array of polygons. Each polygon is represented by an array of points
- `color` (tuple): Polygon fill color
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits
- `offset` (tuple): Optional offset for all points

**Example**:
```python
import numpy as np

# Filled triangle
pts = np.array([[100, 50], [50, 150], [150, 150]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.fillPoly(img, [pts], (0, 255, 0))

# Multiple filled polygons
pts1 = np.array([[200, 200], [250, 250], [300, 200]], np.int32).reshape((-1, 1, 2))
pts2 = np.array([[350, 200], [400, 250], [450, 200], [425, 150]], np.int32).reshape((-1, 1, 2))
cv2.fillPoly(img, [pts1, pts2], (255, 0, 255))
```

---

```python { .api }
# Fill convex polygon (faster alternative for convex polygons)
cv2.fillConvexPoly(img, points, color, lineType=cv2.LINE_8, shift=0) -> img
```

Fills a convex polygon. This function is faster than `fillPoly` but only works with convex polygons.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `points` (np.ndarray): Array of polygon vertices
- `color` (tuple): Polygon fill color
- `lineType` (int): Line type
- `shift` (int): Number of fractional bits

---

```python { .api }
# Draw text
cv2.putText(img, text, org, fontFace, fontScale, color, thickness=1, lineType=cv2.LINE_8, bottomLeftOrigin=False) -> img
```

Draws a text string on the image.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `text` (str): Text string to draw
- `org` (tuple): Bottom-left corner of the text string in the image (x, y)
- `fontFace` (int): Font type (see Font Types)
- `fontScale` (float): Font scale factor (multiplied by font-specific base size)
- `color` (tuple): Text color
- `thickness` (int): Thickness of the lines used to draw text
- `lineType` (int): Line type
- `bottomLeftOrigin` (bool): If True, image data origin is at bottom-left corner

**Example**:
```python
# Simple text
cv2.putText(img, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)

# Larger, thicker text
cv2.putText(img, 'Hello World!', (100, 150), cv2.FONT_HERSHEY_DUPLEX,
            2, (0, 255, 0), 3)

# Italic text
cv2.putText(img, 'Italic', (50, 250),
            cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC,
            1.5, (255, 0, 255), 2)
```

---

```python { .api }
# Get text size
cv2.getTextSize(text, fontFace, fontScale, thickness) -> (text_size, baseline)
```

Calculates the width and height of a text string. Useful for positioning text.

**Parameters**:
- `text` (str): Text string
- `fontFace` (int): Font type
- `fontScale` (float): Font scale factor
- `thickness` (int): Text thickness

**Returns**:
- `text_size` (tuple): Size of text box (width, height)
- `baseline` (int): y-coordinate of baseline relative to bottom-most text point

**Example**:
```python
text = 'OpenCV'
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

(text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)

# Center text in image
x = (img.shape[1] - text_width) // 2
y = (img.shape[0] + text_height) // 2
cv2.putText(img, text, (x, y), font, scale, (255, 255, 255), thickness)
```

---

```python { .api }
# Draw marker
cv2.drawMarker(img, position, color, markerType=cv2.MARKER_CROSS, markerSize=20, thickness=1, lineType=cv2.LINE_8) -> img
```

Draws a marker at the specified position.

**Parameters**:
- `img` (np.ndarray): Image to draw on
- `position` (tuple): Marker position (x, y)
- `color` (tuple): Marker color
- `markerType` (int): Marker type (see Marker Types)
- `markerSize` (int): Marker size
- `thickness` (int): Line thickness
- `lineType` (int): Line type

**Example**:
```python
# Different marker types
cv2.drawMarker(img, (100, 100), (255, 0, 0), cv2.MARKER_CROSS, 20, 2)
cv2.drawMarker(img, (200, 100), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 20, 2)
cv2.drawMarker(img, (300, 100), (0, 0, 255), cv2.MARKER_STAR, 20, 2)
cv2.drawMarker(img, (400, 100), (255, 255, 0), cv2.MARKER_DIAMOND, 20, 2)
```

---

#### Marker Types

Constants for marker shapes:

```python { .api }
cv2.MARKER_CROSS          # Cross marker (+)
cv2.MARKER_TILTED_CROSS   # Tilted cross marker (x)
cv2.MARKER_STAR           # Star marker (*)
cv2.MARKER_DIAMOND        # Diamond marker (◇)
cv2.MARKER_SQUARE         # Square marker (□)
cv2.MARKER_TRIANGLE_UP    # Upward triangle marker (△)
cv2.MARKER_TRIANGLE_DOWN  # Downward triangle marker (▽)
```

---

#### Line Types

Constants for line rendering:

```python { .api }
cv2.LINE_4   # 4-connected line
cv2.LINE_8   # 8-connected line (default)
cv2.LINE_AA  # Anti-aliased line (smooth)
```

**Note**: `LINE_AA` produces smooth, anti-aliased lines but is computationally more expensive.

---

#### Font Types

Constants for text rendering:

```python { .api }
cv2.FONT_HERSHEY_SIMPLEX        # Normal sans-serif font
cv2.FONT_HERSHEY_PLAIN          # Small sans-serif font
cv2.FONT_HERSHEY_DUPLEX         # Normal sans-serif font (more complex than SIMPLEX)
cv2.FONT_HERSHEY_COMPLEX        # Normal serif font
cv2.FONT_HERSHEY_TRIPLEX        # Normal serif font (more complex than COMPLEX)
cv2.FONT_HERSHEY_COMPLEX_SMALL  # Smaller version of COMPLEX
cv2.FONT_HERSHEY_SCRIPT_SIMPLEX # Hand-writing style font
cv2.FONT_HERSHEY_SCRIPT_COMPLEX # More complex hand-writing style font
cv2.FONT_ITALIC                 # Flag for italic font (combine with OR)
```

**Example - Font Comparison**:
```python
import cv2
import numpy as np

img = np.zeros((600, 800, 3), np.uint8)
fonts = [
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX
]
font_names = [
    'HERSHEY_SIMPLEX',
    'HERSHEY_PLAIN',
    'HERSHEY_DUPLEX',
    'HERSHEY_COMPLEX',
    'HERSHEY_TRIPLEX',
    'SCRIPT_SIMPLEX',
    'SCRIPT_COMPLEX'
]

for i, (font, name) in enumerate(zip(fonts, font_names)):
    y = 50 + i * 70
    cv2.putText(img, name, (50, y), font, 1, (255, 255, 255), 2)

cv2.imshow('Font Comparison', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

**Complete Drawing Example**:
```python
import cv2
import numpy as np

# Create blank image
img = np.zeros((512, 512, 3), np.uint8)

# Draw various shapes
cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)
cv2.circle(img, (447, 63), 63, (0, 0, 255), -1)
cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 180, (255, 255, 0), -1)

# Draw polygon
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], True, (0, 255, 255), 3)

# Draw text
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV Drawing', (10, 450), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Draw markers
cv2.drawMarker(img, (100, 100), (255, 0, 255), cv2.MARKER_CROSS, 20, 2)
cv2.drawMarker(img, (150, 100), (255, 0, 255), cv2.MARKER_STAR, 20, 2)

# Display
cv2.imshow('Drawing Demo', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Best Practices

### Window Management
- Always call `cv2.waitKey()` after `cv2.imshow()` to allow the window to render
- Use `cv2.destroyAllWindows()` at the end of your program to clean up
- Create windows with `cv2.WINDOW_NORMAL` flag if you need to resize them

### Interactive Applications
- Use trackbars for real-time parameter adjustment
- Implement mouse callbacks for interactive selection and drawing
- Consider using `cv2.selectROI()` for user-friendly region selection

### Performance
- Drawing operations modify images in-place
- Use `img.copy()` if you need to preserve the original image
- Anti-aliased lines (`LINE_AA`) are slower than standard lines
- Filled shapes are faster than equivalent polylines

### Color Considerations
- Remember OpenCV uses BGR color order, not RGB
- For grayscale images, use single-value tuples: `(intensity,)` or just `intensity`
- Color values range from 0-255 for 8-bit images

### Text Rendering
- Use `cv2.getTextSize()` to calculate text dimensions for proper positioning
- Consider background rectangles for better text visibility
- Combine font types with `cv2.FONT_ITALIC` using bitwise OR: `cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC`

### Debugging and Visualization
- Use `cv2.imshow()` liberally during development for debugging
- Add text annotations to display algorithm parameters and results
- Use different colors for different types of features (e.g., green for correct, red for errors)
- Draw markers or circles to highlight key points
