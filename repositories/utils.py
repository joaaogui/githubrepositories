from allauth.socialaccount.models import SocialToken

# Uses the socialtoken model to get the user token
def get_token(request):
    return SocialToken.objects.get(account__user=request.user,
                                               account__provider='github')