# import os
# import shutil
#
# from old.json_handler import JSONFileHandler
#
# settings = JSONFileHandler(
#     "C:\\Users\danil\OneDrive\Coding\Projects\Python\Os\settings.json"
# )


def index():
    return ["project"]


def project(lib):
    pass


# def is_project_directory(files):
#     project_extensions = settings.load("project_extensions")
#
#     for file in files:
#         if any(file.endswith(extension) for extension in project_extensions):
#             return True
#     return False
#
#
# def check_projects(main_folder):
#     projects = []
#
#     for root, dirs, files in os.walk(main_folder):
#         if is_project_directory(files):
#             if any(project in root for project in projects):
#                 continue
#             projects.append(root)
#     return projects
#
#
# def open_project(project_path):
#     os.system(f'code "{project_path}"')
#
#
# def project(lib, option="list", selected_project=None):
#     projects_directory = settings.load("projects_directory")
#     projects = check_projects(projects_directory)
#
#     match option:
#         case "list":
#             print("\tProjects:")
#             last_category = False
#             for project in projects:
#                 relative_project = project.replace(projects_directory, "")
#                 category, project_name = relative_project.split("\\")
#
#                 if category != last_category:
#                     print(category)
#                 last_category = category
#                 print("  -", project_name)
#         case "open":
#             relative_projects = [
#                 project.replace(projects_directory, "").lower() for project in projects
#             ]
#             selected_project = selected_project.lower().replace("/", "\\")
#             if selected_project in relative_projects:
#                 project_path = os.path.join(projects_directory, selected_project)
#                 open_project(project_path)
#             else:
#                 print("Unknown project")
#         case "create":
#             name = input("Name (Test): ").title()
#             name = name if name else "Test"
#             template = input("Type (Python): ").title()
#             template = template if template else "Python"
#             version = float(input("Version (0.1): ").title())
#             version = version if version else 0.1
#
#             template_path = os.path.join(
#                 settings.load("root"), "projects\\templates", template
#             )
#
#             project_path = os.path.join(
#                 settings.load("root"), "projects", template, version, name
#             )
#
#             if os.path.exists(project_path):
#                 print("Project already exists.")
#                 return
#
#             shutil.copytree(template_path, project_path)
#
#             project_info_handler = JSONFileHandler(
#                 os.path.join(
#                     settings.load("root"), "projects", template, version, "project.json"
#                 )
#             )
#
#             project_info = project_info_handler.load()
#             project_info["latest"] = version
#             project_info["versions"] = [version]
#             project_info_handler.save(project_info)
#
#             # # Modify the project structure, update configuration files, etc.
#             # # Add your custom logic here to customize the project as needed
#
#             print(
#                 f"Project created successfully at 'D:\\Projects\\{template}\\{name}'."
#             )
#         case "delete":
#             path = os.path.join(settings.load("root"), "projects", selected_project)
#
#             if os.path.exists(path):
#                 if input("Are you 100% sure? (Type YES to confirm) ") == "YES":
#                     shutil.rmtree(path)
#                     print("Project deleted.")
#                 else:
#                     print("Project not deleted.")
#             else:
#                 print("Project does not exist.")
#         case _:
#             print("Unknown subcommand. (list / open)")
