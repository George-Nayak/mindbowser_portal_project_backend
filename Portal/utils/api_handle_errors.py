# from user.models import PlatformUser

def handle_errors(serializer_errors):
    response = {}
    response['errors'] = [{}]
    for key,value in serializer_errors.items():
        response["errors"][0] = value[0]
    return response


# def check_platform_user(mobile):
# 	response = {}
# 	platform_user = ''
# 	try:
# 		platform_user = PlatformUser.objects.get(user__username = mobile, user__is_active = True)
# 	except PlatformUser.DoesNotExist:
# 		response['result'] = 0
# 		response['errors'] = ['mobile number not registered']
# 	finally:
# 		return platform_user, response