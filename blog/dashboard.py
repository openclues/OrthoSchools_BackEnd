# your_app_name/dashboard.py

from admin_tools.dashboard import modules, Dashboard

class CustomDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.ModelList(
            title='Your Models',
            models=('blog.Blog', ),
        ))

        self.available_children.append(modules.AppList(
            title='Applications',
        ))

        # Add more modules as needed
