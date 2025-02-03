class AppSettings:
    # Window settings
    WINDOW_SIZE = {
        'login': '300x150',
        'dashboard': '400x300',
        'users': '600x400'
    }

    # Default padding and margins
    PADDING = {
        'small': 5,
        'medium': 10,
        'large': 20
    }

    # Font configurations
    FONTS = {
        'default': ('Arial', 10),
        'header': ('Arial', 12, 'bold'),
        'title': ('Arial', 14, 'bold')
    }

    # Application settings
    APP_NAME = "My Application"
    VERSION = "1.0.0"

    # Table settings
    TABLE_ROWS_PER_PAGE = 10

    # Timeout settings (in milliseconds)
    SESSION_TIMEOUT = 30 * 60 * 1000  # 30 minutes

    @classmethod
    def get_window_size(cls, window_type):
        return cls.WINDOW_SIZE.get(window_type, '400x300')

    @classmethod
    def get_font(cls, font_type):
        return cls.FONTS.get(font_type, cls.FONTS['default'])