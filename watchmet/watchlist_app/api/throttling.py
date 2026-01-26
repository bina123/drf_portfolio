from rest_framework.throttling import UserRateThrottle

class ReviewDetailThrottle(UserRateThrottle):
    scope = 'review-detail'
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'