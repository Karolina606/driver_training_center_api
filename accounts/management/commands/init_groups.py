from django.contrib.auth.models import Group, Permission, User


def add_admin_perm():
	admin_group, created = Group.objects.get_or_create(name='admin')
	proj_add_perm = Permission.objects.all()
	for perm in proj_add_perm:
		admin_group.permissions.add(perm)


def add_instructor_perm():
	instructor_group, created = Group.objects.get_or_create(name='instructor')
	# instructor_group.permissions.add(Permission.objects.get(name="Can view driving license category"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can view course"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can add lesson"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can change lesson"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can delete lesson"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can view lesson"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can add student course status"))
	# instructor_group.permissions.add(Permission.objects.get(name="Can view user"))


def add_student_perm():
	student_group, created = Group.objects.get_or_create(name='student')
	# student_group.permissions.add(Permission.objects.get(name="Can view driving license category"))
	# student_group.permissions.add(Permission.objects.get(name="Can view course"))
	# student_group.permissions.add(Permission.objects.get(name="Can view lesson"))
	# student_group.permissions.add(Permission.objects.get(name="Can add student course status"))
	# student_group.permissions.add(Permission.objects.get(name="Can view user"))
	# student_group.permissions.add(Permission.objects.get(name="Can change user"))


def add_admin_user():
	admin, created = User.objects.get_or_create(
		username='admin@admin.com',
		email='admin@admin.com',
		first_name='admin',
		last_name='admin'
	)
	admin.set_password('Admin!123')
	admin.groups.add(Group.objects.get(name='admin'))
	admin.is_superuser = True
	admin.is_staff = True
	admin.is_active = True
	admin.save()


add_admin_perm()
add_instructor_perm()
add_student_perm()
add_admin_user()
