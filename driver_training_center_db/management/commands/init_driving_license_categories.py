from driver_training_center_db.models import DrivingLicenseCategory


def add_driving_license_category():
	driving_license_category, created = DrivingLicenseCategory.objects.get_or_create(
		name__iexact='B',
		practice_full_time=30,
		theory_full_time=30
	)
	# driving_license_category.practice_full_time = 30
	# driving_license_category.theory_full_time = 30


add_driving_license_category()
