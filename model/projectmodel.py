
class ProjectModel(object):

    def __init__(self, project_dir, pkg_name):
        self.projectDir = project_dir
        self.packageName = pkg_name

    def __str__(self):
        print('projectDir = ' + self.projectDir + ', packageName = ' + self.packageName)
