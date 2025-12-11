app_name = "technical_store_system"
app_title = "Technical Store System"
app_publisher = "Nadeem"
app_description = "Advanced multi-store inventory management system with analytics, mobile integration, vendor management, compliance, and audit trails"
app_email = "zahid_printers@yahoo.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Includes in <head>
# ------------------

# app_include_css = "/assets/technical_store_system/css/technical_store_system.css"
# app_include_js = "/assets/technical_store_system/js/technical_store_system.js"

# web_include_css = "/assets/technical_store_system/css/technical_store_system.css"
# web_include_js = "/assets/technical_store_system/js/technical_store_system.js"

# website_theme_scss = "technical_store_system/public/scss/website"

# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# page_js = {"page" : "public/js/file.js"}

# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# home_page = "login"

# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# website_generators = ["Web Page"]

# Jinja
# ----------

# jinja = {
# 	"methods": "technical_store_system.utils.jinja_methods",
# 	"filters": "technical_store_system.utils.jinja_filters"
# }

# Installation
# ------------

after_install = "technical_store_system.installer.after_install"

# Uninstallation
# ------------

after_uninstall = "technical_store_system.installer.after_uninstall"

# Migration
# ---------

after_migrate = "technical_store_system.installer.after_migrate"

# Desk Notifications
# ------------------

# notification_config = "technical_store_system.notifications.get_notification_config"

# Permissions
# -----------

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------

# Override document class for controllers
override_doctype_class = {
	"Store Settings": "technical_store_system.utils.controllers.store_settings_controller.StoreSettings",
	"Store Location": "technical_store_system.utils.controllers.store_location_controller.StoreLocationController"
}

# Document Events - Auto-generate location code and name
doc_events = {
	"Store Location": {
		"before_insert": "technical_store_system.utils.controllers.store_location_controller.before_insert_event",
		"before_save": "technical_store_system.utils.controllers.store_location_controller.before_save_event",
	},
	"Store Item Group": {
		"before_insert": "technical_store_system.utils.controllers.item_group_controller.before_insert_event",
		"before_save": "technical_store_system.utils.controllers.item_group_controller.before_save_event",
		"on_update": "technical_store_system.utils.controllers.item_group_controller.on_update_event",
		"before_delete": "technical_store_system.utils.controllers.item_group_controller.before_delete_event",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"technical_store_system.tasks.all"
# 	],
# 	"daily": [
# 		"technical_store_system.tasks.daily"
# 	],
# 	"hourly": [
# 		"technical_store_system.tasks.hourly"
# 	],
# 	"weekly": [
# 		"technical_store_system.tasks.weekly"
# 	],
# 	"monthly": [
# 		"technical_store_system.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "technical_store_system.install.before_tests"

# Overriding Methods
# ------------------------------

# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "technical_store_system.event.get_events"
# }

# override_doctype_dashboards = {
# 	"Task": "technical_store_system.task.get_dashboard_data"
# }

# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------

# before_request = ["technical_store_system.utils.before_request"]
# after_request = ["technical_store_system.utils.after_request"]

# Job Events
# ----------

# before_job = ["technical_store_system.utils.before_job"]
# after_job = ["technical_store_system.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"technical_store_system.auth.validate"
# ]

# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30
# }

