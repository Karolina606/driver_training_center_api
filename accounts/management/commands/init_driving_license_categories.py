
def add_driving_license_category():
	driving_license_category, created = DrivingLicenseCategory.objects.get_or_create(name='student')


add_driving_license_category()
