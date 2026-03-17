# Drawing and Colors

Low-level drawing utilities and color management for creating custom visualizations and annotations.

## Capabilities

### Color Management

```python { .api }
class Color:
    """RGB color representation with predefined colors."""
    WHITE: Color
    BLACK: Color  
    RED: Color
    GREEN: Color
    BLUE: Color
    # Additional predefined colors...

class ColorPalette:
    """Collection of colors for consistent theming."""
    DEFAULT: ColorPalette
    
    @classmethod
    def from_hex(cls, colors: list[str]) -> ColorPalette: ...
```

### Drawing Functions

```python { .api }
def draw_polygon(image: np.ndarray, polygon: np.ndarray, color: Color, thickness: int = 2) -> np.ndarray:
    """Draw polygon outline on image."""

def draw_filled_polygon(image: np.ndarray, polygon: np.ndarray, color: Color) -> np.ndarray:
    """Draw filled polygon on image."""

def draw_rectangle(image: np.ndarray, rect: Rect, color: Color, thickness: int = 2) -> np.ndarray:
    """Draw rectangle outline."""

def draw_filled_rectangle(image: np.ndarray, rect: Rect, color: Color) -> np.ndarray:
    """Draw filled rectangle."""

def draw_text(image: np.ndarray, text: str, anchor: Point, color: Color, scale: float = 0.5) -> np.ndarray:
    """Draw text on image."""
```