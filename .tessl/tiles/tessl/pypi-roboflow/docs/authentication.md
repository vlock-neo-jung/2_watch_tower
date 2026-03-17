# Authentication

Authentication and initialization functionality for accessing the Roboflow platform. This includes API key validation, workspace configuration, and CLI-based login flows.

## Capabilities

### Roboflow Client Class

The main entry point for the Roboflow SDK that handles authentication and provides access to workspaces and projects.

```python { .api }
class Roboflow:
    def __init__(self, api_key=None, model_format="undefined", notebook="undefined"):
        """
        Initialize Roboflow client with API credentials.
        
        Parameters:
        - api_key: str, optional - Your Roboflow API key. If not provided, loads from environment or config
        - model_format: str - Model format preference for downloads (default: "undefined")
        - notebook: str - Notebook environment identifier (default: "undefined")
        """
    
    def workspace(self, the_workspace=None):
        """
        Access a workspace.
        
        Parameters:
        - the_workspace: str, optional - Workspace name/ID. Uses default if not specified
        
        Returns:
        Workspace object for the specified workspace
        """
    
    def project(self, project_name, the_workspace=None):
        """
        Access a project directly without going through workspace.
        
        Parameters:
        - project_name: str - Name of the project or "workspace/project" format
        - the_workspace: str, optional - Workspace name if not in project_name
        
        Returns:
        Project object for the specified project
        """
```

### CLI Authentication

Functions for authenticating via command line interface and configuring persistent access.

```python { .api }
def login(workspace=None, force=False):
    """
    Authenticate via CLI with interactive token entry.
    
    Parameters:
    - workspace: str, optional - Specific workspace to authenticate for
    - force: bool - Force re-authentication even if already logged in
    
    Returns:
    None - Saves authentication to config file
    """
```

### High-Level Initialization

Convenience function for initializing workspace access.

```python { .api }
def initialize_roboflow(the_workspace=None):
    """
    High-level function to initialize Roboflow workspace.
    
    Parameters:
    - the_workspace: str, optional - Workspace URL/name to initialize
    
    Returns:
    Workspace object for the initialized workspace
    """
```

### API Key Validation

Internal function for validating API keys with the Roboflow server.

```python { .api }
def check_key(api_key, model, notebook, num_retries=0):
    """
    Validates API key with Roboflow server.
    
    Parameters:
    - api_key: str - The API key to validate
    - model: str - Model format context
    - notebook: str - Notebook environment context  
    - num_retries: int - Number of retry attempts on failure
    
    Returns:
    dict or str - Validation response or "onboarding" for demo keys
    
    Raises:
    RuntimeError - If API key is invalid or server validation fails
    """
```

## Usage Examples

### Basic Authentication

```python
import roboflow

# Authenticate with API key
rf = roboflow.Roboflow(api_key="your_api_key_here")

# Or use environment variable/config file
rf = roboflow.Roboflow()  # Loads from ROBOFLOW_API_KEY env var or config
```

### CLI Authentication

```python
import roboflow

# Interactive CLI login
roboflow.login()

# Force re-authentication
roboflow.login(force=True)

# Login for specific workspace
roboflow.login(workspace="my-workspace")
```

### Workspace Access Patterns

```python
# Access default workspace
workspace = rf.workspace()

# Access specific workspace
workspace = rf.workspace("my-workspace-name")

# Direct project access
project = rf.project("my-project")

# Project with specific workspace
project = rf.project("my-project", "my-workspace")
```

## Configuration

The SDK supports multiple authentication methods:

1. **API Key Parameter**: Pass directly to `Roboflow()` constructor
2. **Environment Variable**: Set `ROBOFLOW_API_KEY` environment variable
3. **Config File**: Use `roboflow.login()` to save authentication token
4. **Demo Keys**: Built-in demo keys for public dataset access

Config files are stored at:
- **Linux/macOS**: `~/.config/roboflow/config.json`
- **Windows**: `%USERPROFILE%/roboflow/config.json`

## Error Handling

Authentication failures raise `RuntimeError` with descriptive messages. Common scenarios:

```python
try:
    rf = roboflow.Roboflow(api_key="invalid_key")
    workspace = rf.workspace()
except RuntimeError as e:
    print(f"Authentication failed: {e}")
```