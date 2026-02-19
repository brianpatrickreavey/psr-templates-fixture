"""Hello World Module - Example Kodi addon functionality"""


def hello_world():
    """Print hello world message.
    
    Returns:
        str: A greeting message
    """
    return "Hello from Kodi addon!"


def greet(name):
    """Generate a personalized greeting.
    
    Args:
        name (str): Name to greet
        
    Returns:
        str: Personalized greeting message
    """
    return f"Hello {name}, welcome to the Kodi addon module!"


if __name__ == '__main__':
    print(hello_world())
