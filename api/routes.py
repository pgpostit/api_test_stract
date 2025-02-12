def register_routes(app):

    DEVELOPER_NAME = "Paulo S. Garcia"
    DEVELOPER_EMAIL = "pgarciapydev@gmail.com"
    DEVELOPER_LINKEDIN = "https://linkedin.com/in/paulogarcia01"

    @app.route('/')
    @app.route('/index')
    def index():
        return f"Hello, world! I'm {DEVELOPER_NAME}. This is my e-mail: {DEVELOPER_EMAIL}. Here is my LinkedIn profile {DEVELOPER_LINKEDIN}"
